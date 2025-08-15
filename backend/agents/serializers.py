"""
Serializers for the agents app.

This module contains serializers for the Agent and AgentConfig models,
which handle the conversion of complex data types (like model instances)
to Python native datatypes that can be rendered into JSON, XML, etc.
"""

from rest_framework import serializers
from .models import Agent


class AgentConfigSerializer(serializers.Serializer):
    """Serializer for agent configuration."""
    model_name = serializers.CharField(required=False)
    temperature = serializers.FloatField(required=False, min_value=0, max_value=2)
    max_tokens = serializers.IntegerField(required=False, min_value=1)
    system_prompt = serializers.CharField(required=False)
    tools = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for the Agent model."""
    config = AgentConfigSerializer(required=False)
    
    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'description',
            'agent_type',
            'status',
            'config',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']
    
    def create(self, validated_data):
        """Create a new agent instance."""
        config_data = validated_data.pop('config', {})
        agent = Agent.objects.create(
            **validated_data,
            config=config_data
        )
        return agent
    
    def update(self, instance, validated_data):
        """Update an existing agent instance."""
        config_data = validated_data.pop('config', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update config if provided
        if config_data is not None:
            current_config = instance.config or {}
            current_config.update(config_data)
            instance.config = current_config
        
        instance.save()
        return instance
