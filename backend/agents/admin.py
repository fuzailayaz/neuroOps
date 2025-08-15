"""
Admin configuration for the agents app.

This module registers the Agent models with the Django admin interface.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Agent, AgentCapability, AgentCapabilityMapping, AgentMessage


class AgentCapabilityInline(admin.TabularInline):
    """Inline admin for AgentCapabilityMapping model."""
    model = AgentCapabilityMapping
    extra = 1
    fields = ('capability', 'is_enabled', 'config')
    autocomplete_fields = ('capability',)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """Admin interface for the Agent model."""
    list_display = (
        'name', 
        'agent_type', 
        'status', 
        'is_active',
        'created_by',
        'last_active',
        'created_at',
    )
    list_filter = ('agent_type', 'status', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'config')
    readonly_fields = ('created_at', 'updated_at', 'last_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'agent_type', 'is_active')
        }),
        ('Status', {
            'fields': ('status', 'last_active')
        }),
        ('Configuration', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [AgentCapabilityInline]
    autocomplete_fields = ('created_by',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

    def save_model(self, request, obj, form, change):
        """Set the created_by field to the current user if this is a new object."""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AgentCapability)
class AgentCapabilityAdmin(admin.ModelAdmin):
    """Admin interface for the AgentCapability model."""
    list_display = ('name', 'description', 'get_agent_count')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Annotate the queryset with the number of agents using each capability."""
        return super().get_queryset(request).prefetch_related('agent_mappings')
    
    def get_agent_count(self, obj):
        """Return the number of agents with this capability."""
        return obj.agent_mappings.count()
    get_agent_count.short_description = _('Agent Count')
    get_agent_count.admin_order_field = 'agent_mappings__count'


@admin.register(AgentMessage)
class AgentMessageAdmin(admin.ModelAdmin):
    """Admin interface for the AgentMessage model."""
    list_display = ('agent_link', 'short_content', 'is_from_agent', 'created_at', 'updated_at')
    list_filter = ('is_from_agent', 'created_at')
    search_fields = ('content', 'agent__name')
    readonly_fields = ('agent', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def agent_link(self, obj):
        """Create a link to the agent's admin page."""
        url = reverse('admin:agents_agent_change', args=[obj.agent_id])
        return format_html('<a href="{}">{}</a>', url, obj.agent)
    agent_link.short_description = _('Agent')
    agent_link.admin_order_field = 'agent__name'
    
    def short_content(self, obj):
        """Return a shortened version of the message content."""
        return obj.content[:100] + ('...' if len(obj.content) > 100 else '')
    short_content.short_description = _('Content')
    
    def has_add_permission(self, request):
        """Disable adding messages from the admin interface.
        
        Messages should only be created through the API.
        """
        return False
