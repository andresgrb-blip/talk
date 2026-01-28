from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Notification
from django.utils import timezone
from .models import Message, Story


@login_required
def search_users_api(request):
    """API endpoint per cercare utenti (usato per inviti gruppi)"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'users': []})
    
    users = User.objects.filter(
        Q(username__icontains=query) | 
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query)
    ).exclude(id=request.user.id)[:10]
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name() or user.username,
            'avatar': user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else '/media/profile_pics/default.jpg'
        })
    
    return JsonResponse({'users': users_data})


@login_required
def unread_notifications_count(request):
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})


@login_required
def unread_chat_count(request):
    unread_count = Message.objects.filter(
        room__participants=request.user,
        is_read=False,
    ).exclude(sender=request.user).count()
    return JsonResponse({'unread_count': unread_count})


@login_required
def unviewed_stories_count(request):
    following_ids = request.user.profile.following.values_list('following__user__id', flat=True)

    stories = Story.objects.filter(
        author__id__in=list(following_ids) + [request.user.id],
        expires_at__gt=timezone.now(),
    ).exclude(views__viewer=request.user)

    return JsonResponse({'unread_count': stories.count()})
