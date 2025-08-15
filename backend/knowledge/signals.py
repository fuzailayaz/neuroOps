import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Document, KnowledgeBase, KnowledgeGraph
from .tasks import process_document, delete_document_embeddings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Document)
def document_post_save(sender, instance, created, **kwargs):
    """
    Trigger document processing when a new document is created or updated.
    """
    if created or instance.file and not instance.processed:
        logger.info(f"Queueing document for processing: {instance.id}")
        process_document.delay(instance.id)


@receiver(pre_delete, sender=Document)
def document_pre_delete(sender, instance, **kwargs):
    """
    Clean up document chunks and embeddings when a document is deleted.
    """
    if instance.chunks.exists():
        logger.info(f"Deleting embeddings for document: {instance.id}")
        delete_document_embeddings.delay(instance.id)


@receiver(post_save, sender=KnowledgeBase)
def knowledgebase_post_save(sender, instance, created, **kwargs):
    """
    Create a knowledge graph when a new knowledge base is created.
    """
    if created and not hasattr(instance, 'knowledge_graph'):
        KnowledgeGraph.objects.create(
            name=f"Graph for {instance.name}",
            description=f"Automatically created knowledge graph for {instance.name}",
            knowledge_base=instance
        )
        logger.info(f"Created knowledge graph for knowledge base: {instance.id}")
