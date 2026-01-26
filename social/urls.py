from django.urls import path
from . import views, chat_views, story_views, reaction_views, hashtag_views, achievement_views, group_views, api_views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('explore/', views.explore, name='explore'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers'),
    path('profile/<str:username>/following/', views.following_list, name='following'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('notifications/', views.notifications, name='notifications'),
    path('search/', views.search, name='search'),
    
    # Chat
    path('chat/', chat_views.chat_list, name='chat_list'),
    path('chat/<str:room_name>/', chat_views.chat_room, name='chat_room'),
    path('chat/start/<str:username>/', chat_views.start_chat, name='start_chat'),
    
    # Stories
    path('stories/', story_views.stories_list, name='stories_list'),
    path('stories/create/', story_views.create_story, name='create_story'),
    path('stories/<int:story_id>/', story_views.view_story, name='view_story'),
    path('stories/<int:story_id>/delete/', story_views.delete_story, name='delete_story'),
    path('stories/<int:story_id>/viewers/', story_views.story_viewers, name='story_viewers'),
    
    # Reactions
    path('post/<int:post_id>/react/', reaction_views.react_to_post, name='react_to_post'),
    path('post/<int:post_id>/reactions/', reaction_views.post_reactions, name='post_reactions'),
    
    # Hashtags
    path('trending/', hashtag_views.trending_hashtags, name='trending'),
    path('hashtag/<str:hashtag_name>/', hashtag_views.hashtag_posts, name='hashtag_posts'),
    path('hashtags/search/', hashtag_views.search_hashtags, name='search_hashtags'),
    
    # Achievements
    path('achievements/', achievement_views.user_achievements, name='user_achievements'),
    path('achievements/<str:username>/', achievement_views.user_achievements, name='user_achievements_detail'),
    path('leaderboard/', achievement_views.leaderboard, name='leaderboard'),
    path('achievements/progress/', achievement_views.achievement_progress, name='achievement_progress'),
    
    # Groups
    path('groups/', group_views.groups_list, name='groups_list'),
    path('groups/create/', group_views.create_group, name='create_group'),
    path('groups/<int:group_id>/', group_views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', group_views.join_group, name='join_group'),
    path('groups/<int:group_id>/leave/', group_views.leave_group, name='leave_group'),
    path('groups/<int:group_id>/post/', group_views.post_to_group, name='post_to_group'),
    path('groups/<int:group_id>/post/<int:post_id>/pin/', group_views.toggle_pin_post, name='toggle_pin_post'),
    
    # API endpoints
    path('api/search/users/', api_views.search_users_api, name='api_search_users'),
]
