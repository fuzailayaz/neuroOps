from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

User = get_user_model()

# Constants for model fields and meta options
KNOWLEDGE_BASE_VERBOSE_NAME = 'knowledge base'
KNOWLEDGE_BASE_VERBOSE_NAME_PLURAL = 'knowledge bases'

class KnowledgeBase(TimeStampedModel):
    """Represents a collection of knowledge documents."""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(_('is public'), default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='knowledge_bases',
        verbose_name=_('owner')
    )
    
    class Meta:
        verbose_name = _(KNOWLEDGE_BASE_VERBOSE_NAME)
        verbose_name_plural = _(KNOWLEDGE_BASE_VERBOSE_NAME_PLURAL)
        ordering = ['-created']
        
    def __str__(self):
        return self.name


class Document(TimeStampedModel):
    """Represents a document in the knowledge base."""
    class DocumentType(models.TextChoices):
        PDF = 'pdf', _('PDF')
        DOCX = 'docx', _('Word Document')
        TXT = 'txt', _('Text File')
        URL = 'url', _('Web Page')
        MARKDOWN = 'md', _('Markdown')
        
    title = models.CharField(_('title'), max_length=255)
    content = models.TextField(_('content'), blank=True)
    file = models.FileField(
        _('file'),
        upload_to='documents/%Y/%m/%d/',
        blank=True,
        null=True
    )
    url = models.URLField(_('URL'), blank=True, null=True)
    doc_type = models.CharField(
        _('document type'),
        max_length=10,
        choices=DocumentType.choices,
        default=DocumentType.TXT
    )
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('knowledge base')
    )
    processed = models.BooleanField(_('processed'), default=False)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['-created']
        
    def __str__(self):
        return self.title


class DocumentChunk(TimeStampedModel):
    """Represents a chunk of a document for vector search."""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks',
        verbose_name=_('document')
    )
    content = models.TextField(_('content'))
    chunk_index = models.PositiveIntegerField(_('chunk index'))
    vector_id = models.CharField(_('vector ID'), max_length=255, blank=True)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('document chunk')
        verbose_name_plural = _('document chunks')
        ordering = ['document', 'chunk_index']
        unique_together = ['document', 'chunk_index']
        
    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"


class KnowledgeGraph(TimeStampedModel):
    """Represents a knowledge graph with nodes and relationships."""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    knowledge_base = models.OneToOneField(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='knowledge_graph',
        verbose_name=_('knowledge base')
    )
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('knowledge graph')
        verbose_name_plural = _('knowledge graphs')
        
    def __str__(self):
        return self.name


class KnowledgeNode(TimeStampedModel):
    """Represents a node in the knowledge graph."""
    graph = models.ForeignKey(
        KnowledgeGraph,
        on_delete=models.CASCADE,
        related_name='nodes',
        verbose_name=_('graph')
    )
    label = models.CharField(_('label'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    node_type = models.CharField(_('node type'), max_length=50)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('knowledge node')
        verbose_name_plural = _('knowledge nodes')
        ordering = ['label']
        
    def __str__(self):
        return self.label


class KnowledgeEdge(TimeStampedModel):
    """Represents a relationship between two knowledge nodes."""
    graph = models.ForeignKey(
        KnowledgeGraph,
        on_delete=models.CASCADE,
        related_name='edges',
        verbose_name=_('graph')
    )
    source = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name='outgoing_edges',
        verbose_name=_('source node')
    )
    target = models.ForeignKey(
        KnowledgeNode,
        on_delete=models.CASCADE,
        related_name='incoming_edges',
        verbose_name=_('target node')
    )
    relationship_type = models.CharField(_('relationship type'), max_length=100)
    weight = models.FloatField(_('weight'), default=1.0)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('knowledge edge')
        verbose_name_plural = _('knowledge edges')
        unique_together = ['source', 'target', 'relationship_type']
        
    def __str__(self):
        return f"{self.source} -[{self.relationship_type}]-> {self.target}"
