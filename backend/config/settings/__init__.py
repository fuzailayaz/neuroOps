from .base import *  # noqa

# Import environment-specific settings
if os.getenv('ENVIRONMENT') == 'production':
    from .production import *  # noqa
else:
    from .local import *  # noqa
