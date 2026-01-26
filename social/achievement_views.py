from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Achievement, UserAchievement


@login_required
def user_achievements(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    all_achievements = Achievement.objects.all()
    earned_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    earned_ids = set(earned_achievements.values_list('achievement_id', flat=True))
    
    achievements_data = []
    for achievement in all_achievements:
        achievements_data.append({
            'achievement': achievement,
            'earned': achievement.id in earned_ids,
            'earned_at': next((ua.earned_at for ua in earned_achievements if ua.achievement_id == achievement.id), None)
        })
    
    total_points = earned_achievements.aggregate(total=Sum('achievement__points'))['total'] or 0
    
    context = {
        'profile_user': user,
        'achievements_data': achievements_data,
        'total_points': total_points,
        'earned_count': len(earned_ids),
        'total_count': all_achievements.count()
    }
    return render(request, 'social/achievements.html', context)


@login_required
def leaderboard(request):
    users = User.objects.annotate(
        total_points=Sum('user_achievements__achievement__points'),
        achievements_count=Count('user_achievements')
    ).filter(total_points__gt=0).select_related('profile').order_by('-total_points', '-achievements_count')[:50]
    
    user_rank = None
    for idx, user in enumerate(users, 1):
        if user.id == request.user.id:
            user_rank = idx
            break
    
    context = {
        'users': users,
        'user_rank': user_rank
    }
    return render(request, 'social/leaderboard.html', context)


@login_required
def achievement_progress(request):
    user = request.user
    
    from .models import Post, Comment
    
    progress = {
        'posts_count': Post.objects.filter(author=user).count(),
        'followers_count': user.profile.followers_count,
        'comments_count': Comment.objects.filter(author=user).count(),
        'popular_posts': Post.objects.filter(author=user).annotate(
            reactions_count=Count('reactions') + Count('likes')
        ).filter(reactions_count__gte=100).count()
    }
    
    return JsonResponse({'progress': progress})
