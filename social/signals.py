from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification, Post, Comment, Follow, Reaction, Message, Story
from . import achievement_checker


@receiver(post_save, sender=Notification)
def send_notification_to_websocket(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_data = {
            'id': instance.id,
            'type': instance.notification_type,
            'sender': instance.sender.username,
            'sender_id': instance.sender.id,
            'message': get_notification_message(instance),
            'created_at': instance.created_at.isoformat(),
        }
        
        async_to_sync(channel_layer.group_send)(
            f'notifications_{instance.recipient.id}',
            {
                'type': 'notification_message',
                'notification': notification_data
            }
        )


def get_notification_message(notification):
    if notification.notification_type == 'like':
        return f'{notification.sender.username} ha messo mi piace al tuo post'
    elif notification.notification_type == 'comment':
        return f'{notification.sender.username} ha commentato il tuo post'
    elif notification.notification_type == 'follow':
        return f'{notification.sender.username} ha iniziato a seguirti'
    return 'Nuova notifica'


@receiver(post_save, sender=Post)
def notify_followers_new_post(sender, instance, created, **kwargs):
    if created:
        # Controlla achievement per i post
        achievement_checker.check_post_achievements(instance.author)
        
        channel_layer = get_channel_layer()
        
        post_data = {
            'id': instance.id,
            'author': instance.author.username,
            'author_id': instance.author.id,
            'content': instance.content[:100] + '...' if len(instance.content) > 100 else instance.content,
            'has_image': bool(instance.image),
            'created_at': instance.created_at.isoformat(),
            'message': f'{instance.author.username} ha pubblicato un nuovo post'
        }
        
        for follow_relationship in instance.author.profile.followers.all():
            async_to_sync(channel_layer.group_send)(
                f'notifications_{follow_relationship.follower.user.id}',
                {
                    'type': 'new_post',
                    'post': post_data
                }
            )


@receiver(post_save, sender=Comment)
def notify_post_author_new_comment(sender, instance, created, **kwargs):
    if created:
        # Controlla achievement per i commenti
        achievement_checker.check_comment_achievements(instance.author)
        
        if instance.author != instance.post.author:
            channel_layer = get_channel_layer()
            
            comment_data = {
                'id': instance.id,
                'author': instance.author.username,
                'author_id': instance.author.id,
                'post_id': instance.post.id,
                'content': instance.content[:50] + '...' if len(instance.content) > 50 else instance.content,
                'created_at': instance.created_at.isoformat(),
                'message': f'{instance.author.username} ha commentato il tuo post'
            }
            
            async_to_sync(channel_layer.group_send)(
                f'notifications_{instance.post.author.id}',
                {
                    'type': 'new_comment',
                    'comment': comment_data
                }
            )


@receiver(post_save, sender=Follow)
def check_follower_achievement(sender, instance, created, **kwargs):
    if created:
        # Controlla achievement per i follower
        achievement_checker.check_follower_achievements(instance.following.user)


@receiver(post_save, sender=Reaction)
def check_popular_post_achievement(sender, instance, created, **kwargs):
    if created:
        # Controlla se il post è diventato virale
        achievement_checker.check_popular_post_achievement(instance.post)


@receiver(post_save, sender=Message)
def refresh_counters_on_new_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        participants = instance.room.participants.all()
        for participant in participants:
            if participant.id == instance.sender.id:
                continue
            async_to_sync(channel_layer.group_send)(
                f'notifications_{participant.id}',
                {
                    'type': 'refresh_counts'
                }
            )


@receiver(post_save, sender=Story)
def refresh_counters_on_new_story(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        for follow_relationship in instance.author.profile.followers.all():
            async_to_sync(channel_layer.group_send)(
                f'notifications_{follow_relationship.follower.user.id}',
                {
                    'type': 'refresh_counts'
                }
            )
