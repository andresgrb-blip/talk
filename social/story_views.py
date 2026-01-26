from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Story, StoryView
import re


@login_required
def stories_list(request):
    following_ids = request.user.profile.following.values_list('following__user__id', flat=True)
    
    stories = Story.objects.filter(
        author__id__in=list(following_ids) + [request.user.id],
        expires_at__gt=timezone.now()
    ).select_related('author', 'author__profile').prefetch_related('views')
    
    users_with_stories = {}
    for story in stories:
        if story.author.id not in users_with_stories:
            users_with_stories[story.author.id] = {
                'user': story.author,
                'stories': [],
                'has_unviewed': False
            }
        users_with_stories[story.author.id]['stories'].append(story)
        
        if not story.views.filter(viewer=request.user).exists():
            users_with_stories[story.author.id]['has_unviewed'] = True
    
    context = {
        'users_with_stories': users_with_stories.values()
    }
    return render(request, 'social/stories_list.html', context)


@login_required
def create_story(request):
    if request.method == 'POST':
        story = Story.objects.create(
            author=request.user,
            image=request.FILES.get('image'),
            video=request.FILES.get('video'),
            text_content=request.POST.get('text_content', ''),
            background_color=request.POST.get('background_color', '#FF69B4')
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'story_id': story.id,
                'message': 'Storia creata con successo!'
            })
        return redirect('stories_list')
    
    return render(request, 'social/create_story.html')


@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    if story.is_expired:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Storia scaduta'}, status=404)
        messages.error(request, 'Questa storia è scaduta.')
        return redirect('stories_list')
    
    # Registra visualizzazione
    StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    # Se è una richiesta AJAX, ritorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'views_count': story.views_count
        })
    
    # Altrimenti mostra il template
    context = {'story': story}
    return render(request, 'social/story_viewer.html', context)


@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    story.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('stories_list')


@login_required
def story_viewers(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    viewers = story.views.select_related('viewer', 'viewer__profile').order_by('-viewed_at')
    
    context = {
        'story': story,
        'viewers': viewers
    }
    return render(request, 'social/story_viewers.html', context)
