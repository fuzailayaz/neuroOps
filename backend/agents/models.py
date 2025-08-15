"""
Models for the agents app.

This module defines the data models for managing AI agents in the NeuroOps platform.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.models import BaseModel, TimeStampedModel, StatusModel

User = get_user_model()


class AgentType(models.TextChoices):
    """Types of agents in the system."""
    RESEARCHER = 'researcher', _('Researcher')
    ANALYST = 'analyst', _('Analyst')
    CODER = 'coder', _('Coder')
    WRITER = 'writer', _('Writer')
    MANAGER = 'manager', _('Manager')
    CUSTOM = 'custom', _('Custom')


class AgentStatus(models.TextChoices):
    """Possible statuses for an agent."""
    OFFLINE = 'offline', _('Offline')
    IDLE = 'idle', _('Idle')
    THINKING = 'thinking', _('Thinking')
    EXECUTING = 'executing', _('Executing')
    ERROR = 'error', _('Error')
    UPDATING = 'updating', _('Updating')


class Agent(BaseModel):
    """
    Represents an AI agent in the system.
    
    Each agent has a specific role, capabilities, and can be assigned tasks.
    """
    name = models.CharField(
        max_length=100,
        help_text=_("Display name of the agent")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Description of the agent's purpose and capabilities")
    )
    agent_type = models.CharField(
        max_length=20,
        choices=AgentType.choices,
        default=AgentType.CUSTOM,
        help_text=_("Type of the agent")
    )
    status = models.CharField(
        max_length=20,
        choices=AgentStatus.choices,
        default=AgentStatus.OFFLINE,
        help_text=_("Current status of the agent")
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Configuration settings for the agent")
    )
    last_active = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the agent was last active")
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')
    
    def __str__(self):
        return f"{self.name} ({self.get_agent_type_display()})"
    
    def update_status(self, status, save=True):
        """Update the agent's status and last active time."""
        self.status = status
        self.last_active = timezone.now()
        if save:
            self.save(update_fields=['status', 'last_active', 'updated_at'])
    
    def get_absolute_url(self):
        """Get the URL for this agent's detail view."""
        from django.urls import reverse
        return reverse('agent-detail', kwargs={'pk': self.pk})


class AgentCapability(BaseModel):
    """
    Represents a capability that an agent can have.
    
    Capabilities define what actions an agent can perform.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Unique name for this capability")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Detailed description of the capability")
    )
    required_parameters = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Required parameters for this capability in JSON format")
    )
    
    class Meta:
        verbose_name = _('Agent Capability')
        verbose_name_plural = _('Agent Capabilities')
    
    def __str__(self):
        return self.name


class AgentCapabilityMapping(TimeStampedModel):
    """Mapping between agents and their capabilities."""
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='capability_mappings',
        help_text=_("The agent that has this capability")
    )
    capability = models.ForeignKey(
        AgentCapability,
        on_delete=models.CASCADE,
        related_name='agent_mappings',
        help_text=_("The capability being assigned to the agent")
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text=_("Whether this capability is currently enabled for the agent")
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Configuration specific to this agent's capability")
    )
    
    class Meta:
        unique_together = [['agent', 'capability']]
        verbose_name = _('Agent Capability Mapping')
        verbose_name_plural = _('Agent Capability Mappings')
        ordering = ['agent__name', 'capability__name']
    
    def __str__(self):
        return f"{self.agent.name} - {self.capability.name}"


class AgentMessage(TimeStampedModel):
    """
    Represents a message from or to an agent.
    
    Used for logging and maintaining conversation history between users and agents.
    """
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text=_("The agent this message is associated with")
    )
    content = models.TextField(
        help_text=_("The actual content of the message")
    )
    is_from_agent = models.BooleanField(
        default=False,
        help_text=_("Whether the message is from the agent (True) or to the agent (False)")
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Additional metadata about the message in JSON format")
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = _('Agent Message')
        verbose_name_plural = _('Agent Messages')
        indexes = [
            models.Index(fields=['agent', 'created_at']),
            models.Index(fields=['is_from_agent', 'created_at']),
        ]
    
    def __str__(self):
        direction = "From" if self.is_from_agent else "To"
        return f"{direction} {self.agent.name}: {self.content[:50]}{'...' if len(self.content) > 50 else ''}"
    
    def get_message_type(self):
        """Return a human-readable message type."""
        return 'agent' if self.is_from_agent else 'user'
