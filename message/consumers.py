import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Message, GroupChat, Member


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
<<<<<<< HEAD
        try:
            self.group_name = self.scope['url_route']['kwargs']['group_name']
            self.group = await self.get_or_create_group(self.group_name)
        except Exception as e:
            print(str(e))
=======
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f"chat_{self.chat_id}"
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825

        # Validate the user and add them to the chat group
        user = self.scope["user"]
        if await self.is_member_of_chat(user):
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

<<<<<<< HEAD
        await self.accept()

=======
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.dumps(text_data)

<<<<<<< HEAD
        # Send message to group
=======
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

<<<<<<< HEAD
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def chat_message(self, event):
        message = event['message']

        # ارسال پیام به کلاینت‌ها
=======
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
        await self.send(text_data=json.dumps({
            'message': message
        }))

<<<<<<< HEAD
    @staticmethod
    async def get_or_create_group(group_name):
        group, _ = await GroupChat.objects.get_or_create(group_name=group_name)
        return group

    @staticmethod
    async def save_message(group, sender, message):
        chat_message = ChatMessage(group=group, sender=sender, message=message)
        await chat_message.save()
=======
    @database_sync_to_async
    def is_member_of_chat(self, user):
        return Member.objects.filter(chat__unique_code=self.chat_id, user=user).exists()
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
