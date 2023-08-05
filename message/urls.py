from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/chat/<str:group_name>/messages/', views.get_messages),
    path('api/v1/chat/<str:group_name>/send/', views.send_message),
    path('login/', views.login_user),
    path('register/', views.user_registration_view),
]