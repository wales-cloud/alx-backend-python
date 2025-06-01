from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom user model
class User(AbstractUser):
    # Add custom fields here if needed in the future
    pass


# Conversation model - a conversation can involve multiple users
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# Message model - belongs to a conversation and has a sender
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.id}"
