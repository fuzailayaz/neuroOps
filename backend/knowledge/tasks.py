import logging
import io
import os
from typing import Optional, List, Dict, Any
from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Document, DocumentChunk
from .vector_store import get_vector_store
from .document_processors import get_document_processor

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_document(self, document_id: int):
    """
    Process a document by extracting text, chunking it, and generating embeddings.
    """
    try:
        document = Document.objects.get(id=document_id)
        logger.info(f"Processing document: {document.id} - {document.title}")
        
        # Get the appropriate document processor based on file type
        processor = get_document_processor(document)
        if not processor:
            logger.error(f"No processor found for document type: {document.doc_type}")
            return
        
        # Extract text content from the document
        content = processor.extract_text(document)
        if not content:
            logger.warning(f"No content extracted from document: {document.id}")
            return
        
        # Update document content
        document.content = content
        
        # Split content into chunks
        chunks = processor.chunk_content(content)
        
        # Delete existing chunks
        document.chunks.all().delete()
        
        # Create new chunks
        for i, chunk_text in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                content=chunk_text,
                chunk_index=i,
                metadata={
                    'source': document.title,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            )
        
        # Generate and store embeddings
        vector_store = get_vector_store()
        vector_store.add_document(document)
        
        # Mark document as processed
        document.processed = True
        document.save(update_fields=['content', 'processed', 'modified'])
        
        logger.info(f"Successfully processed document: {document.id} with {len(chunks)} chunks")
        return True
        
    except Document.DoesNotExist:
        logger.error(f"Document not found: {document_id}")
        return False
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {str(e)}", exc_info=True)
        # Retry the task with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

@shared_task
def delete_document_embeddings(document_id: int):
    """
    Delete all embeddings associated with a document.
    """
    try:
        vector_store = get_vector_store()
        vector_store.delete_document(document_id)
        logger.info(f"Deleted embeddings for document: {document_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting embeddings for document {document_id}: {str(e)}")
        return False

@shared_task
def process_knowledge_base(knowledge_base_id: int):
    """
    Process all documents in a knowledge base.
    """
    from .models import KnowledgeBase
    
    try:
        knowledge_base = KnowledgeBase.objects.get(id=knowledge_base_id)
        logger.info(f"Processing knowledge base: {knowledge_base.id} - {knowledge_base.name}")
        
        # Process each document in the knowledge base
        for document in knowledge_base.documents.all():
            process_document.delay(document.id)
        
        return True
    except KnowledgeBase.DoesNotExist:
        logger.error(f"Knowledge base not found: {knowledge_base_id}")
        return False
    except Exception as e:
        logger.error(f"Error processing knowledge base {knowledge_base_id}: {str(e)}")
        return False
