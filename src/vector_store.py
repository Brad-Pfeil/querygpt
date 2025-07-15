import os
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core.base.base_retriever import BaseRetriever
from typing import Tuple, Dict, Any

from dotenv import load_dotenv

load_dotenv()


def setup_vector_store(
    schema_info: Dict[str, Any], k: int | None = None
) -> Tuple[VectorStore, BaseRetriever]:
    """
    Initialize a Neo4j vector store and return both the store and a retriever.

    Args:
        schema_info: Database schema metadata (unused here but kept for interface consistency).
        k: Number of similar examples to retrieve (overrides env var RAG_K).

    Environment Variables:
        NEO4J_URI      – e.g. "neo4j+s://<YOUR-HOST>.databases.neo4j.io:7687"
        NEO4J_USERNAME – your Neo4j username (default: "neo4j")
        NEO4J_PASSWORD – your Neo4j password
        EMBEDDING_DIM  – embedding dimension (default: 1536)
        RAG_K          – default few-shot k (default: 3)
    """
    # Load from environment (or fall back to placeholders)
    uri: str = os.getenv("NEO4J_URI", "")
    username: str = os.getenv("NEO4J_USERNAME", "")
    password: str = os.getenv("NEO4J_PASSWORD", "")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "1536"))

    # Make sure your Neo4j instance has the vector plugin enabled!
    neo4j_store = Neo4jVectorStore(
        username=username,
        password=password,
        url=uri,
        embedding_dimension=embedding_dim,
        hybrid_search=True,
    )

    # Build an index on top of it and expose a retriever
    index = VectorStoreIndex.from_vector_store(neo4j_store)
    top_k = k if k is not None else int(os.getenv("RAG_K", "3"))
    retriever = index.as_retriever(similarity_top_k=top_k)

    return neo4j_store, retriever
