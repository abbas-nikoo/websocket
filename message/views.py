from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, render

from .serializers import *
from .models import *

import json


@api_view(['POST'])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat(request):
    current_user = request.user
    title = request.data.get('group_name')
    if title:
        chat = GroupChat.objects.create(creator=current_user, title=title)
        # member = Member.objects.create(chat=chat, user=current_user)
        serializer = GroupChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': 'Please provide a group name'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def chat(request, chat_id):
    current_user = request.user
    chat = get_object_or_404(GroupChat, unique_code=chat_id)

    if request.method == "GET":
        if not Member.objects.filter(chat=chat, user=current_user).exists():
            return Response({'detail': 'You are not a member of this chat'}, status=status.HTTP_403_FORBIDDEN)

        serializer = GroupChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if Member.objects.filter(chat=chat, user=current_user).exists():
            return Response({'detail': 'You are already a member of this chat'}, status=status.HTTP_400_BAD_REQUEST)

        member = Member(chat=chat, user=current_user)
        member.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "join", 'username': current_user.username})
            }
        )

        serializer = GroupChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def leave_chat(request, chat_id):
    current_user = request.user
    chat = get_object_or_404(GroupChat, unique_code=chat_id)

    if chat.creator == current_user:
        chat.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "delete"})
            }
        )
    else:
        Member.objects.filter(chat=chat, user=current_user).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "leave", 'username': current_user.username})
            }
        )

    return Response({'detail': 'You have left the chat'}, status=status.HTTP_200_OK)
