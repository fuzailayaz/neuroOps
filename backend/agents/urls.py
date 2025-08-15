from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'agents'

# Create a router for our agents API
router = DefaultRouter()
router.register(r'agents', views.AgentViewSet, basename='agent')

# Create a nested router for agent configurations
agents_router = routers.NestedSimpleRouter(router, r'agents', lookup='agent')
agents_router.register(r'config', views.AgentConfigViewSet, basename='agent-config')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('', include(agents_router.urls)),
]
