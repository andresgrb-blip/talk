from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
import json
from .models import ChatRoom, Message


@login_required
def chat_list(request):
    chat_rooms = request.user.chat_rooms.all().order_by('-created_at')
    context = {'chat_rooms': chat_rooms}
    return render(request, 'social/chat_list.html', context)


@login_required
def chat_room(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    
    if request.user not in chat_room.participants.all():
        chat_room.participants.add(request.user)
    
    Message.objects.filter(room=chat_room).exclude(sender=request.user).filter(is_read=False).update(is_read=True)
    messages = chat_room.messages.all().order_by('created_at')
    
    context = {
        'room_name': room_name,
        'chat_room': chat_room,
        'messages': messages,
    }
    return render(request, 'social/chat_room.html', context)


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        return redirect('chat_list')
    
    users = sorted([request.user.username, other_user.username])
    room_name = f"{users[0]}_{users[1]}"
    
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    chat_room.participants.add(request.user, other_user)
    
    return redirect('chat_room', room_name=room_name)


@login_required
def call_room(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)

    if request.user not in chat_room.participants.all():
        chat_room.participants.add(request.user)

    context = {
        'room_name': room_name,
        'chat_room': chat_room,
        'ice_servers_json': json.dumps(getattr(settings, 'WEBRTC_ICE_SERVERS', [])),
    }
    return render(request, 'social/call_room.html', context)
