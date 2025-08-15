from django.contrib import admin
from django.utils.html import format_html
from .models import (
    KnowledgeBase, Document, DocumentChunk,
    KnowledgeGraph, KnowledgeNode, KnowledgeEdge
)


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_public', 'created', 'modified')
    list_filter = ('is_public', 'created', 'modified')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'owner', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


class DocumentChunkInline(admin.TabularInline):
    model = DocumentChunk
    extra = 0
    readonly_fields = ('chunk_index', 'created', 'modified')
    can_delete = False
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'knowledge_base', 'processed', 'created')
    list_filter = ('doc_type', 'processed', 'created', 'modified')
    search_fields = ('title', 'content', 'knowledge_base__name')
    readonly_fields = ('created', 'modified', 'preview_content')
    inlines = [DocumentChunkInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'doc_type', 'knowledge_base', 'file', 'url')
        }),
        ('Content', {
            'fields': ('content', 'preview_content'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'processed'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_content(self, obj):
        """Display a preview of the document content."""
        if not obj.content:
            return "No content available"
        preview = obj.content[:500] + '...' if len(obj.content) > 500 else obj.content
        return format_html('<div style="max-height: 200px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">{}</div>', preview)
    
    preview_content.short_description = 'Content Preview'


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index', 'created')
    list_filter = ('created', 'modified')
    search_fields = ('content', 'document__title')
    readonly_fields = ('created', 'modified', 'preview_content')
    
    fieldsets = (
        (None, {
            'fields': ('document', 'chunk_index', 'vector_id')
        }),
        ('Content', {
            'fields': ('preview_content',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_content(self, obj):
        """Display a preview of the chunk content."""
        preview = obj.content[:500] + '...' if len(obj.content) > 500 else obj.content
        return format_html('<div style="max-height: 200px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">{}</div>', preview)
    
    preview_content.short_description = 'Content Preview'


class KnowledgeNodeInline(admin.TabularInline):
    model = KnowledgeNode
    extra = 1
    show_change_link = True
    fields = ('label', 'node_type', 'description')


@admin.register(KnowledgeGraph)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ('name', 'knowledge_base', 'created')
    search_fields = ('name', 'description', 'knowledge_base__name')
    readonly_fields = ('created', 'modified')
    inlines = [KnowledgeNodeInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'knowledge_base')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


class KnowledgeEdgeInline(admin.TabularInline):
    model = KnowledgeEdge
    fk_name = 'source'
    extra = 1
    show_change_link = True
    fields = ('target', 'relationship_type', 'weight')


@admin.register(KnowledgeNode)
class KnowledgeNodeAdmin(admin.ModelAdmin):
    list_display = ('label', 'node_type', 'graph', 'created')
    list_filter = ('node_type', 'created', 'modified')
    search_fields = ('label', 'description', 'graph__name')
    readonly_fields = ('created', 'modified')
    inlines = [KnowledgeEdgeInline]
    
    fieldsets = (
        (None, {
            'fields': ('graph', 'label', 'node_type', 'description')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(KnowledgeEdge)
class KnowledgeEdgeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'relationship_type', 'weight', 'created')
    list_filter = ('relationship_type', 'created', 'modified')
    search_fields = (
        'source__label', 'target__label', 
        'relationship_type', 'graph__name'
    )
    readonly_fields = ('created', 'modified')
    
    fieldsets = (
        (None, {
            'fields': ('graph', 'source', 'target')
        }),
        ('Relationship', {
            'fields': ('relationship_type', 'weight')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )
