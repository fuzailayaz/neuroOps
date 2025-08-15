from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    Configuration class for the chat application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = 'Chat Application'
    
    def ready(self):
        # Import and register signals
        import chat.signals  # noqa
