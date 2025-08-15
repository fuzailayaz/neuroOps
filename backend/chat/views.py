"""Views for the chat application."""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Chat instances."""
    
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only chats where the current user is a participant."""
        return self.queryset.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        """Add the current user as a participant when creating a chat."""
        chat = serializer.save()
        chat.participants.add(self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a chat."""
        chat = self.get_object()
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Message instances."""
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only messages in chats where the current user is a participant."""
        return self.queryset.filter(chat__participants=self.request.user)
    
    def perform_create(self, serializer):
        """Set the sender to the current user when creating a message."""
        serializer.save(sender=self.request.user)
