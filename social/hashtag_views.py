from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Hashtag, PostHashtag, Post
import re


@login_required
def trending_hashtags(request):
    hashtags = Hashtag.objects.annotate(
        recent_posts=Count(
            'post_hashtags',
            filter=Q(post_hashtags__created_at__gte=timezone.now() - timedelta(hours=24))
        ),
        total_posts=Count('post_hashtags')
    ).filter(recent_posts__gt=0).order_by('-recent_posts', '-total_posts')[:20]
    
    context = {
        'hashtags': hashtags
    }
    return render(request, 'social/trending.html', context)


@login_required
def hashtag_posts(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    
    posts = Post.objects.filter(
        post_hashtags__hashtag=hashtag
    ).select_related('author', 'author__profile').prefetch_related(
        'likes', 'reactions', 'comments'
    ).distinct().order_by('-created_at')
    
    context = {
        'hashtag': hashtag,
        'posts': posts
    }
    return render(request, 'social/hashtag_posts.html', context)


def extract_hashtags(text):
    """
    Estrae hashtag dal testo
    """
    hashtag_pattern = r'#(\w+)'
    return re.findall(hashtag_pattern, text)


def process_post_hashtags(post):
    """
    Processa gli hashtag in un post e crea le relazioni
    """
    hashtags = extract_hashtags(post.content)
    
    for tag_name in hashtags:
        tag_name = tag_name.lower()
        hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
        PostHashtag.objects.get_or_create(post=post, hashtag=hashtag)


@login_required
def search_hashtags(request):
    query = request.GET.get('q', '').strip('#').lower()
    
    if not query:
        return JsonResponse({'hashtags': []})
    
    hashtags = Hashtag.objects.filter(
        name__icontains=query
    ).annotate(
        posts_count=Count('post_hashtags')
    ).order_by('-posts_count')[:10]
    
    hashtags_data = [{
        'name': tag.name,
        'posts_count': tag.posts_count
    } for tag in hashtags]
    
    return JsonResponse({'hashtags': hashtags_data})
