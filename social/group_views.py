from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Group, GroupMembership, GroupPost, Post
from .forms import GroupForm


@login_required
def groups_list(request):
    my_groups = request.user.joined_groups.all().select_related('creator').prefetch_related('members')
    
    public_groups = Group.objects.filter(is_private=False).exclude(
        id__in=my_groups.values_list('id', flat=True)
    ).select_related('creator').prefetch_related('members')[:20]
    
    context = {
        'my_groups': my_groups,
        'public_groups': public_groups
    }
    return render(request, 'social/groups_list.html', context)


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    is_member = group.members.filter(id=request.user.id).exists()
    
    if group.is_private and not is_member:
        messages.error(request, 'Questo gruppo è privato.')
        return redirect('groups_list')
    
    membership = None
    if is_member:
        membership = GroupMembership.objects.get(user=request.user, group=group)
    
    posts = GroupPost.objects.filter(group=group).select_related(
        'post__author', 'post__author__profile'
    ).prefetch_related('post__likes', 'post__reactions', 'post__comments').order_by('-pinned', '-created_at')[:20]
    
    members = group.members.select_related('profile')[:10]
    
    context = {
        'group': group,
        'is_member': is_member,
        'membership': membership,
        'posts': posts,
        'members': members,
        'is_admin': membership and membership.role == 'admin' if membership else False
    }
    return render(request, 'social/group_detail.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            
            GroupMembership.objects.create(
                user=request.user,
                group=group,
                role='admin'
            )
            
            messages.success(request, f'Gruppo "{group.name}" creato con successo!')
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    
    context = {'form': form}
    return render(request, 'social/create_group.html', context)


@login_required
@require_POST
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if group.is_private:
        return JsonResponse({'error': 'Gruppo privato - richiedi invito'}, status=403)
    
    membership, created = GroupMembership.objects.get_or_create(
        user=request.user,
        group=group,
        defaults={'role': 'member'}
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': f'Ti sei unito a {group.name}!',
            'members_count': group.members_count
        })
    else:
        return JsonResponse({'error': 'Sei già membro di questo gruppo'}, status=400)


@login_required
@require_POST
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if group.creator == request.user:
        return JsonResponse({'error': 'Il creatore non può lasciare il gruppo'}, status=403)
    
    try:
        membership = GroupMembership.objects.get(user=request.user, group=group)
        membership.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Hai lasciato {group.name}',
            'members_count': group.members_count
        })
    except GroupMembership.DoesNotExist:
        return JsonResponse({'error': 'Non sei membro di questo gruppo'}, status=400)


@login_required
@require_POST
def post_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if not group.members.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'Devi essere membro per postare'}, status=403)
    
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    group_post, created = GroupPost.objects.get_or_create(
        group=group,
        post=post
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': f'Post condiviso in {group.name}!'
        })
    else:
        return JsonResponse({'error': 'Post già condiviso in questo gruppo'}, status=400)


@login_required
@require_POST
def toggle_pin_post(request, group_id, post_id):
    group = get_object_or_404(Group, id=group_id)
    
    membership = GroupMembership.objects.filter(user=request.user, group=group).first()
    if not membership or membership.role not in ['admin', 'moderator']:
        return JsonResponse({'error': 'Permessi insufficienti'}, status=403)
    
    group_post = get_object_or_404(GroupPost, group=group, post_id=post_id)
    group_post.pinned = not group_post.pinned
    group_post.save()
    
    return JsonResponse({
        'success': True,
        'pinned': group_post.pinned
    })
