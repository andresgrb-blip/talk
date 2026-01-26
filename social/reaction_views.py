from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Reaction, Notification


@login_required
@require_POST
def react_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction_type')
    
    if reaction_type not in dict(Reaction.REACTION_TYPES).keys():
        return JsonResponse({'error': 'Tipo di reazione non valido'}, status=400)
    
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={'reaction_type': reaction_type}
    )
    
    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()
            removed = True
        else:
            reaction.reaction_type = reaction_type
            reaction.save()
            removed = False
    else:
        removed = False
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )
    
    reactions_count = {}
    for r_type, r_label in Reaction.REACTION_TYPES:
        count = post.reactions.filter(reaction_type=r_type).count()
        if count > 0:
            reactions_count[r_type] = count
    
    user_reaction = None
    if not removed:
        try:
            user_reaction = post.reactions.get(user=request.user).reaction_type
        except Reaction.DoesNotExist:
            pass
    
    return JsonResponse({
        'success': True,
        'reactions_count': reactions_count,
        'total_reactions': sum(reactions_count.values()),
        'user_reaction': user_reaction,
        'removed': removed
    })


@login_required
def post_reactions(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.GET.get('type')
    
    if reaction_type:
        reactions = post.reactions.filter(reaction_type=reaction_type).select_related('user', 'user__profile')
    else:
        reactions = post.reactions.select_related('user', 'user__profile')
    
    reactions_data = []
    for reaction in reactions:
        reactions_data.append({
            'user': {
                'id': reaction.user.id,
                'username': reaction.user.username,
                'profile_picture': reaction.user.profile.profile_picture.url
            },
            'reaction_type': reaction.reaction_type,
            'created_at': reaction.created_at.isoformat()
        })
    
    return JsonResponse({
        'reactions': reactions_data,
        'count': len(reactions_data)
    })
