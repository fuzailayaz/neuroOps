from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.contrib import admin

urlpatterns = [
    # Django Admin - Using default admin site
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Authentication
    path('api/auth/', include('accounts.urls')),
    
    # API v1
    path('api/v1/agents/', include('agents.urls')),
    path('api/v1/chat/', include('chat.urls')),
    path('api/v1/knowledge/', include('knowledge.urls')),
    
    # Health check
    path('health/', include('health_check.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
