# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.db import models


# class UserModelManager(BaseUserManager):
#     def create_user(self, username, password=None):
#
#         if not username:
#             raise ValueError("Users must have an email address")
#
#         else:
#             user = self.model(username=username)
#             user.set_password(password)
#             user.save()
#             return user
#
#
# class UserModel(AbstractBaseUser):
#     username = models.CharField(max_length=255, unique=True, )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     on_deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     modify_at = models.DateTimeField(auto_now=True)
#     objects = UserModelManager()
#
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["password"]
#
#     def __str__(self):
#         return self.username
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#

class GroupChat(models.Model):
    group_name = models.CharField(max_length=255)


class ChatMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
