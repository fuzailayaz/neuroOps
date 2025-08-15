"""Models for the chat application."""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Chat(models.Model):
    """Model representing a chat conversation between users."""
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
        help_text='Users participating in the chat'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
    
    def __str__(self):
        return f'Chat {self.id} - {self.participants.count()} participants'
    
    def mark_messages_as_read(self, user):
        """Mark all messages in the chat as read for a specific user."""
        self.messages.exclude(sender=user).update(is_read=True)


class Message(models.Model):
    """Model representing a message in a chat."""
    
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='The chat this message belongs to'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='User who sent the message'
    )
    content = models.TextField(help_text='The message content')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text='Whether the message has been read')

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'message'
        verbose_name_plural = 'messages'
    
    def __str__(self):
        return f'Message {self.id} from {self.sender} in chat {self.chat_id}'
    
    def save(self, *args, **kwargs):
        """Update the chat's updated_at timestamp when a new message is sent."""
        self.chat.updated_at = timezone.now()
        self.chat.save()
        super().save(*args, **kwargs)
