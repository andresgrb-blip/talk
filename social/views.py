from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import Post, Profile, Like, Comment, Follow, Notification
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from .hashtag_views import process_post_hashtags


def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'social/home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creato per {username}! Ora puoi effettuare il login.')
            login(request, user)
            return redirect('feed')
    else:
        form = UserRegisterForm()
    return render(request, 'social/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Username o password non validi.')
    return render(request, 'social/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def feed(request):
    following_profiles = request.user.profile.following.values_list('following', flat=True)
    posts = Post.objects.filter(
        Q(author__profile__in=following_profiles) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            process_post_hashtags(post)
            messages.success(request, 'Post pubblicato con successo!')
            return redirect('feed')
    else:
        form = PostForm()
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'social/feed.html', context)


@login_required
def explore(request):
    posts = Post.objects.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    context = {'posts': posts}
    return render(request, 'social/explore.html', context)


@login_required
def random_chat(request):
    return render(request, 'social/random_chat.html')


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user.profile,
            following=user.profile
        ).exists()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'social/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'social/edit_profile.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('author', 'author__profile')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Commento aggiunto!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'social/post_detail.html', context)


@login_required
@require_http_methods(["POST"])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post eliminato con successo!')
    return redirect('profile', username=request.user.username)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id
    comment.delete()
    messages.success(request, 'Commento eliminato!')
    return redirect('post_detail', post_id=post_id)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        messages.error(request, 'Non puoi seguire te stesso!')
        return redirect('profile', username=username)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user.profile,
        following=user_to_follow.profile
    )
    
    if not created:
        follow.delete()
        messages.info(request, f'Hai smesso di seguire {username}.')
    else:
        messages.success(request, f'Ora segui {username}!')
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow'
        )
    
    return redirect('profile', username=username)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all().select_related('follower__user')
    context = {
        'profile_user': user,
        'followers': followers,
    }
    return render(request, 'social/followers.html', context)


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = user.profile.following.all().select_related('following__user')
    context = {
        'profile_user': user,
        'following': following,
    }
    return render(request, 'social/following.html', context)


@login_required
def notifications(request):
    notifications = request.user.notifications.all().select_related('sender', 'post')
    unread_count = notifications.filter(is_read=False).count()
    
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'social/notifications.html', context)


@login_required
def search(request):
    query = request.GET.get('q', '')
    users = []
    groups = []
    posts = []
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
        
        # Cerca anche nei gruppi
        from .models import Group
        groups = Group.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).filter(
            Q(is_private=False) | Q(members=request.user)
        ).distinct()[:10]
        
        posts = Post.objects.filter(content__icontains=query).select_related('author', 'author__profile')[:20]
    
    context = {
        'query': query,
        'users': users,
        'groups': groups,
        'posts': posts,
    }
    return render(request, 'social/search.html', context)
