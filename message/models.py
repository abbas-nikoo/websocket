from django.db import models
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

class GroupChat(models.Model):
    group_name = models.CharField(max_length=255)


class ChatMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('connected', 'Connected'), ('disconnected', 'Disconnected')], default='')


class ImageMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.image:
    #         return
    #     img = Image.open(self.image)
    #     img.thumbnail((800, 800), Image.LANCZOS)
    #     output = BytesIO()
    #     img.save(output, format='JPEG', quality=70)
    #     output.seek(0)
    #     self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[
    #         0], 'image/jpeg', sys.getsizeof(output), None)
    #     super(ImageMessage, self).save(*args, **kwargs)