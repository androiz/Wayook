from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name="user1")
    user2 = models.ForeignKey(User, related_name="user2")

class Message(models.Model):
    chat = models.ForeignKey(Chat)
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    message = models.CharField(max_length=255, blank=False, null=False)
