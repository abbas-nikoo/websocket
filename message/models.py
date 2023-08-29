from django.db import models


class GroupChat(models.Model):
    group_name = models.CharField(max_length=255)


class ChatMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('connected', 'Connected'), ('disconnected', 'Disconnected')], default='')
