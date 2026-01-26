from django.contrib.auth.models import User
from .models import Achievement, UserAchievement, Post, Comment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def check_and_award_achievement(user, achievement_name):
    """
    Controlla e assegna un achievement all'utente se non lo ha già
    """
    try:
        achievement = Achievement.objects.get(name=achievement_name)
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=achievement
        )
        
        if created:
            # Invia notifica WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                {
                    'type': 'notification_message',
                    'notification': {
                        'id': 0,
                        'type': 'achievement',
                        'message': f'🏆 Achievement sbloccato: {achievement.icon} {achievement.get_name_display()}!',
                        'points': achievement.points,
                        'created_at': user_achievement.earned_at.isoformat()
                    }
                }
            )
            return True
    except Achievement.DoesNotExist:
        pass
    return False


def check_post_achievements(user):
    """
    Controlla gli achievement relativi ai post
    """
    post_count = Post.objects.filter(author=user).count()
    
    if post_count == 1:
        check_and_award_achievement(user, 'first_post')
    elif post_count == 10:
        check_and_award_achievement(user, 'ten_posts')
    elif post_count == 100:
        check_and_award_achievement(user, 'hundred_posts')


def check_follower_achievements(user):
    """
    Controlla gli achievement relativi ai follower
    """
    follower_count = user.profile.followers_count
    
    if follower_count == 1:
        check_and_award_achievement(user, 'first_follower')
    elif follower_count == 50:
        check_and_award_achievement(user, 'fifty_followers')
    elif follower_count == 100:
        check_and_award_achievement(user, 'hundred_followers')
    elif follower_count == 1000:
        check_and_award_achievement(user, 'influencer')


def check_comment_achievements(user):
    """
    Controlla gli achievement relativi ai commenti
    """
    comment_count = Comment.objects.filter(author=user).count()
    
    if comment_count == 100:
        check_and_award_achievement(user, 'social_butterfly')


def check_popular_post_achievement(post):
    """
    Controlla se un post ha raggiunto 100+ reazioni
    """
    reactions_count = post.reactions.count() + post.likes.count()
    
    if reactions_count >= 100:
        check_and_award_achievement(post.author, 'popular_post')
