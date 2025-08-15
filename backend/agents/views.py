"""
Views for the agents app.

This module contains the views for managing AI agents, including:
- Agent creation and management
- Agent configuration
- Agent status and monitoring
- Task assignment and tracking
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Agent
from .serializers import AgentSerializer, AgentConfigSerializer


class AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows agents to be viewed or edited.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter agents by status or type.
        """
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status', None)
        agent_type = self.request.query_params.get('type', None)
        
        if status_param:
            queryset = queryset.filter(status=status_param)
        if agent_type:
            queryset = queryset.filter(agent_type=agent_type)
            
        return queryset

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a specific agent."""
        _ = self.get_object()  # Get but don't use the agent object yet
        # Add agent start logic here
        return Response({'status': 'agent started'})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Stop a specific agent."""
        _ = self.get_object()  # Get but don't use the agent object yet
        # Add agent stop logic here
        return Response({'status': 'agent stopped'})

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get the status of a specific agent."""
        agent = self.get_object()
        return Response({'status': agent.status})


class AgentConfigViewSet(viewsets.ViewSet):
    """
    API endpoint for managing agent configurations.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, agent_pk=None):
        """List all configurations for an agent."""
        agent = get_object_or_404(Agent, pk=agent_pk)
        serializer = AgentConfigSerializer(agent.config)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, agent_pk=None):
        """Retrieve a specific configuration for an agent."""
        agent = get_object_or_404(Agent, pk=agent_pk)
        config = agent.config.get(pk)
        if not config:
            return Response(
                {'error': 'Configuration not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(config)

    def update(self, request, pk=None, agent_pk=None):
        """Update a specific configuration for an agent."""
        agent = get_object_or_404(Agent, pk=agent_pk)
        # Add configuration update logic here
        return Response({'status': 'configuration updated'})
