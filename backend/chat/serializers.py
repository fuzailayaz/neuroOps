"""Serializers for the chat application."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Chat, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for message objects."""
    
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'content', 'timestamp', 'is_read')
        read_only_fields = ('id', 'timestamp', 'is_read')


class ChatSerializer(serializers.ModelSerializer):
    """Serializer for chat objects."""
    
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ('id', 'participants', 'created_at', 'updated_at', 'messages', 'last_message', 'unread_count')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        """Get the last message in the chat."""
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        """Get the count of unread messages for the current user."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
