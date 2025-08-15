from django.apps import AppConfig


class KnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'knowledge'
    verbose_name = 'Knowledge Management'
    
    def ready(self):
        # Import signal handlers
        try:
            import knowledge.signals  # noqa F401
        except ImportError:
            pass
