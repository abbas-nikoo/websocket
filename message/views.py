from .models import ChatMessage, GroupChat

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .serializers import UserRegistrationSerializer


@api_view(['POST'])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def login_user(request):
#     if request.method == 'POST':
#         serializer = LoginUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         user = User.objects.get(username=username, password=password)
#
#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh)
#         }
#
#         return Response(data=response_data, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, group_name):
    messages = ChatMessage.objects.filter(group__group_name=group_name).order_by('timestamp')
    data = [{'sender': msg.sender, 'message': msg.message} for msg in messages]
    return Response(data)


@api_view(['POST'])
def send_message(request, group_name):
    sender = request.user
    message = request.data.get('message', '')

    if sender and message:
        # ذخیره پیام در پایگاه داده
        group, created = GroupChat.objects.get_or_create(group_name=group_name)
        ChatMessage.objects.create(group=group, sender=sender, message=message)
        return Response({'status': 'success'})

    return Response({'status': 'error', 'message': 'Sender and message fields are required.'})