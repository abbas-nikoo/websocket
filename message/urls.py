from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('api/chat/<str:chat_id>/', views.chat, name='chat'),
    path('api/chat/<str:chat_id>/leave', views.leave_chat, name='leave_chat'),
    path('login/', views.login_user, name='login'),
    path('register/', views.user_registration_view, name='register'),
]