import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification, Message, ChatRoom


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.room_group_name = f'notifications_{self.user.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'mark_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_read(notification_id)

    async def notification_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    async def new_post(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_post',
            'post': event['post']
        }))
    
    async def new_comment(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'comment': event['comment']
        }))

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, recipient=self.user)
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        await self.load_chat_history()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        await self.save_message(message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'user_id': self.user.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    @database_sync_to_async
    def save_message(self, message_content):
        try:
            chat_room, created = ChatRoom.objects.get_or_create(name=self.room_name)
            Message.objects.create(
                room=chat_room,
                sender=self.user,
                content=message_content
            )
        except Exception as e:
            print(f"Error saving message: {e}")

    @database_sync_to_async
    def get_chat_history(self):
        try:
            chat_room = ChatRoom.objects.get(name=self.room_name)
            messages = Message.objects.filter(room=chat_room).order_by('-created_at')[:50]
            return [
                {
                    'message': msg.content,
                    'username': msg.sender.username,
                    'user_id': msg.sender.id,
                    'timestamp': msg.created_at.isoformat()
                }
                for msg in reversed(messages)
            ]
        except ChatRoom.DoesNotExist:
            return []

    async def load_chat_history(self):
        history = await self.get_chat_history()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': history
        }))


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        payload = data.get('payload', {})

        if message_type not in {'offer', 'answer', 'ice', 'hangup'}:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_message',
                'message_type': message_type,
                'payload': payload,
                'user_id': self.user.id,
                'username': self.user.username,
            }
        )

    async def call_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['message_type'],
            'payload': event.get('payload', {}),
            'user_id': event.get('user_id'),
            'username': event.get('username'),
        }))
