"""Serializers for the knowledge application."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Document, KnowledgeBase

User = get_user_model()


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'content', 'file', 'file_type', 'file_size',
            'created_at', 'updated_at', 'owner', 'knowledge_bases'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'file_type', 'file_size']


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeBase model."""
    
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = KnowledgeBase
        fields = [
            'id', 'name', 'description', 'is_public',
            'created_at', 'updated_at', 'owner', 'documents'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
