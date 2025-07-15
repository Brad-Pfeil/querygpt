import json
from llama_index.core import Settings
from llama_index.core.schema import TextNode, BaseNode
from llama_index.core.vector_stores.types import VectorStore
from typing import Any, Dict, List


def initialize_embeddings(
    vector_store: VectorStore,
    schema_info: Dict[str, Any],
    sample_queries_path: str = "examples/sample_queries.json",
) -> None:
    """
    Load sample SQL queries from JSON, embed them using the globally configured
    embedding model, and add them to the provided vector_store.

    Args:
        vector_store: An instance of a LlamaIndex vector store (e.g., Neo4jVectorStore).
        schema_info: Schema metadata (unused here but kept for interface consistency).
        sample_queries_path: Path to the JSON file with sample queries.
    """
    # Use the globally configured embedding model
    embed_model = Settings.embed_model

    # Load sample queries
    try:
        with open(sample_queries_path, "r", encoding="utf-8") as f:
            samples: List[Dict[str, str]] = json.load(f)
    except Exception as e:
        print(f"Error loading sample queries: {e}")
        return

    nodes: List[BaseNode] = []
    # Embed each sample query as a TextNode
    for idx, sample in enumerate(samples):
        natural = sample.get("natural_language", "").strip()
        sql = sample.get("sql", "").strip()
        desc = sample.get("description", "").strip()
        # Construct the text for embedding
        text = f"Query: {natural}\nSQL: {sql}\nDescription: {desc}"
        try:
            embedding = embed_model.get_text_embedding(text)
            node = TextNode(
                text=text, embedding=embedding, id_=f"sample_query_{idx + 1}"
            )
            nodes.append(node)
        except Exception as e:
            print(f"Error embedding sample #{idx + 1}: {e}")

    # Push nodes into the vector store
    if nodes:
        vector_store.add(nodes)
        print(f"Embedded and added {len(nodes)} samples to vector store.")
    else:
        print("No nodes were created for embedding.")
