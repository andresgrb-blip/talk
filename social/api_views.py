from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


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
            'avatar': user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else '/static/default-avatar.png'
        })
    
    return JsonResponse({'users': users_data})
