from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.user.username} follows {self.following.user.username}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} - {self.content[:50]}'

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.post.id}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} on {self.post.id}'


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type} notification for {self.recipient.username}'


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'


# ==================== FUNZIONALITÀ RIVOLUZIONARIE ====================

class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)
    text_content = models.CharField(max_length=200, blank=True)
    background_color = models.CharField(max_length=7, default='#FF69B4')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def views_count(self):
        return self.views.count()
    
    def __str__(self):
        return f'Story by {self.author.username} at {self.created_at}'


class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'viewer')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f'{self.viewer.username} viewed {self.story.author.username}\'s story'


class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', '❤️ Like'),
        ('love', '😍 Love'),
        ('haha', '😂 Haha'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
        ('angry', '😠 Angry'),
        ('fire', '🔥 Fire'),
        ('clap', '👏 Clap'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} reacted {self.reaction_type} to post {self.post.id}'


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    @property
    def posts_count(self):
        return self.post_hashtags.count()
    
    @property
    def trending_score(self):
        recent_posts = self.post_hashtags.filter(created_at__gte=timezone.now() - timedelta(hours=24))
        return recent_posts.count()
    
    def __str__(self):
        return f'#{self.name}'


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_hashtags')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='post_hashtags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'hashtag')
    
    def __str__(self):
        return f'{self.post.id} - #{self.hashtag.name}'


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('first_post', '🎉 Primo Post'),
        ('ten_posts', '📝 10 Post'),
        ('hundred_posts', '💯 100 Post'),
        ('first_follower', '👥 Primo Follower'),
        ('fifty_followers', '⭐ 50 Follower'),
        ('hundred_followers', '🌟 100 Follower'),
        ('popular_post', '🔥 Post Virale (100+ like)'),
        ('active_week', '📅 Attivo 7 giorni'),
        ('social_butterfly', '🦋 100 commenti'),
        ('influencer', '👑 1000 follower'),
    ]
    
    name = models.CharField(max_length=50, choices=ACHIEVEMENT_TYPES, unique=True)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    points = models.IntegerField(default=10)
    
    def __str__(self):
        return f'{self.icon} {self.get_name_display()}'


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f'{self.user.username} earned {self.achievement.name}'


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    cover_image = models.ImageField(upload_to='groups/covers/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMembership', related_name='joined_groups')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def members_count(self):
        return self.members.count()
    
    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderatore'),
        ('member', 'Membro'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'group')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f'{self.user.username} in {self.group.name} ({self.role})'


class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='in_groups')
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-pinned', '-created_at']
    
    def __str__(self):
        return f'Post {self.post.id} in {self.group.name}'


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    show_online_status = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='it')
    
    def __str__(self):
        return f'Preferences for {self.user.username}'


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, help_text='Breve descrizione per SEO e anteprima')
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
