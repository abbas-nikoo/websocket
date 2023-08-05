from django.db import models


class GroupChat(models.Model):
    group_name = models.CharField(max_length=255)


class ChatMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
