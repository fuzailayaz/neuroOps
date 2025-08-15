"""
Signal handlers for the chat application.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

# Example signal handler (uncomment and customize as needed)
# @receiver(post_save, sender=YourModel)
# def your_model_post_save(sender, instance, created, **kwargs):
#     """Handle post-save signals for YourModel."""
#     if created:
#         logger.info(f"New {sender.__name__} created: {instance}")
#     else:
#         logger.info(f"{sender.__name__} updated: {instance}")

# @receiver(post_delete, sender=YourModel)
# def your_model_post_delete(sender, instance, **kwargs):
#     """Handle post-delete signals for YourModel."""
#     logger.info(f"{sender.__name__} deleted: {instance}")
