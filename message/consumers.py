import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, ChatMessage
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_previous_messages = True

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group = await self.get_or_create_group(self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        if self.show_previous_messages:
            await self.send_previous_messages()
            self.show_previous_messages = False

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'sender' in data and 'message' in data:
            sender = data['sender']
            message = data['message']
            await self.save_message(sender, message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'sender': sender,
                    'message': message,
                }
            )

    @database_sync_to_async
    def save_message(self, sender, message):
        chat_message = ChatMessage(group=self.group, sender=sender, message=message)
        chat_message.save()

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def send_previous_messages(self):
        previous_messages = await self.get_previous_messages(self.group)
        for message in previous_messages:
            await self.send(text_data=json.dumps({
                'message': message.message,
                'sender': message.sender,
            }))

    @database_sync_to_async
    def get_or_create_group(self, group_name):
        group, _ = GroupChat.objects.get_or_create(group_name=group_name)
        return group

    @database_sync_to_async
    def get_previous_messages(self, group):
        previous_messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
        # previous_messages.save()
        return list(previous_messages)

