"""URL configuration for chat app."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet, MessageViewSet
from .redis_views import redis_manage, redis_delete, RedisManagementView

app_name = "chat"

router = DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chat")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    # Web interface
    path('redis/', RedisManagementView.as_view(), name='redis-management'),
    
    # API endpoints
    path('redis/keys/', redis_manage, name='redis-manage'),
    path('redis/keys/<str:key>/', redis_delete, name='redis-delete'),
] + router.urls
