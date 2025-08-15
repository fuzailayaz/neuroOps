"""Views for the knowledge application."""

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Document, KnowledgeBase
from .serializers import DocumentSerializer, KnowledgeBaseSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Document instances."""
    
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only documents the current user has access to."""
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a document."""
        serializer.save(owner=self.request.user)


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing KnowledgeBase instances."""
    
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only knowledge bases the current user has access to."""
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a knowledge base."""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_document(self, request, pk=None):
        """Add a document to this knowledge base."""
        knowledge_base = self.get_object()
        document_id = request.data.get('document_id')
        try:
            document = Document.objects.get(id=document_id, owner=request.user)
            knowledge_base.documents.add(document)
            return Response({'status': 'document added'})
        except Document.DoesNotExist:
            return Response(
                {'error': 'Document not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_document(self, request, pk=None):
        """Remove a document from this knowledge base."""
        knowledge_base = self.get_object()
        document_id = request.data.get('document_id')
        try:
            document = Document.objects.get(id=document_id, owner=request.user)
            knowledge_base.documents.remove(document)
            return Response({'status': 'document removed'})
        except Document.DoesNotExist:
            return Response(
                {'error': 'Document not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )
