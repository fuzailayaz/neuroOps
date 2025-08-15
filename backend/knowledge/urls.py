from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'knowledge'

router = DefaultRouter()
# Register your viewsets here
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'knowledge-bases', views.KnowledgeBaseViewSet, basename='knowledgebase')

urlpatterns = [
    # API endpoints will be added here
] + router.urls
