from django.contrib import admin
from .models import (Profile, Post, Like, Comment, Follow, Notification, ChatRoom, Message,
                     Story, StoryView, Reaction, Hashtag, PostHashtag, Achievement, 
                     UserAchievement, Group, GroupMembership, GroupPost, UserPreferences)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'location']
    list_filter = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at', 'likes_count', 'comments_count']
    search_fields = ['author__username', 'content']
    list_filter = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Content'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    search_fields = ['user__username']
    list_filter = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at']
    search_fields = ['author__username', 'content']
    list_filter = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Content'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__user__username', 'following__user__username']
    list_filter = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username']
    list_filter = ['notification_type', 'is_read', 'created_at']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'content_preview', 'created_at', 'is_read']
    search_fields = ['sender__username', 'content']
    list_filter = ['created_at', 'is_read']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Content'


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at', 'expires_at', 'is_expired', 'views_count']
    search_fields = ['author__username', 'text_content']
    list_filter = ['created_at']


@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ['story', 'viewer', 'viewed_at']
    search_fields = ['story__author__username', 'viewer__username']
    list_filter = ['viewed_at']


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'reaction_type', 'created_at']
    search_fields = ['user__username']
    list_filter = ['reaction_type', 'created_at']


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name', 'posts_count', 'trending_score', 'created_at']
    search_fields = ['name']


@admin.register(PostHashtag)
class PostHashtagAdmin(admin.ModelAdmin):
    list_display = ['post', 'hashtag', 'created_at']
    search_fields = ['hashtag__name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'points', 'description']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    search_fields = ['user__username']
    list_filter = ['earned_at']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'members_count', 'is_private', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_private', 'created_at']


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at']
    search_fields = ['user__username', 'group__name']
    list_filter = ['role', 'joined_at']


@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['group', 'post', 'pinned', 'created_at']
    list_filter = ['pinned', 'created_at']


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'dark_mode', 'email_notifications', 'push_notifications']
    search_fields = ['user__username']
    list_filter = ['dark_mode']
