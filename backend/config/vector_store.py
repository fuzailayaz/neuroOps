"""
Configuration for Qdrant vector database.
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

class QdrantConfig:
    """Configuration class for Qdrant vector database."""
    
    def __init__(self):
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.api_key = os.getenv("QDRANT_API_KEY", None)
        self.collection_name = os.getenv("QDRANT_COLLECTION", "neuroops_embeddings")
        self.vector_size = int(os.getenv("VECTOR_SIZE", 384))  # Default to all-MiniLM-L6-v2 size
        
        # Initialize the client
        self.client = self._initialize_client()
        
        # Ensure collection exists
        self._ensure_collection()
    
    def _initialize_client(self):
        """Initialize and return Qdrant client."""
        return QdrantClient(
            url=f"http://{self.host}:{self.port}",
            api_key=self.api_key if self.api_key else None,
            prefer_grpc=True
        )
    
    def _ensure_collection(self):
        """Ensure the collection exists, create if it doesn't."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

# Create a singleton instance
qdrant_config = QdrantConfig()
