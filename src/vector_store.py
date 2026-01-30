from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core.base.base_retriever import BaseRetriever
from typing import Tuple, Dict, Any

from .config import VectorStoreConfig


def setup_vector_store(
    schema_info: Dict[str, Any], config: VectorStoreConfig
) -> Tuple[VectorStore, BaseRetriever]:
    """
    Initialize a Neo4j vector store and return both the store and a retriever.

    Args:
        schema_info: Database schema metadata (unused here but kept for interface consistency).
        config: Explicit vector store configuration.
    """
    # Make sure your Neo4j instance has the vector plugin enabled!
    neo4j_store = Neo4jVectorStore(
        username=config.username,
        password=config.password,
        url=config.uri,
        embedding_dimension=config.embedding_dim,
        hybrid_search=True,
    )

    # Build an index on top of it and expose a retriever
    index = VectorStoreIndex.from_vector_store(neo4j_store)
    retriever = index.as_retriever(similarity_top_k=config.rag_k)

    return neo4j_store, retriever
