import sqlite3
import polars as pl
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import TextNode
from .agents.intent_agent import IntentAgent
from .agents.table_agent import TableAgent
from .agents.column_prune_agent import ColumnPruneAgent
from .agents.sql_generator import SQLGenerator
from .config import LlamaIndexConfig, VectorStoreConfig
from .db.schema import get_database_schema
from .db.seed import create_sample_university_data
from .vector_store import setup_vector_store
from typing import Any, Dict, cast


def configure_llama_index(config: LlamaIndexConfig) -> None:
    Settings.llm = OpenAI(model=config.llm_model)
    Settings.embed_model = OpenAIEmbedding(model=config.embedding_model)


class QueryGPT:
    def __init__(
        self,
        llama_config: LlamaIndexConfig | None = None,
        vector_store_config: VectorStoreConfig | None = None,
    ) -> None:
        # Setup DB
        create_sample_university_data()
        self.schema_info = get_database_schema()

        # Setup LLM and Embeddings globally for all LlamaIndex components
        resolved_llama_config = llama_config or LlamaIndexConfig()
        configure_llama_index(resolved_llama_config)

        # Vector Store
        resolved_vector_config = vector_store_config or VectorStoreConfig.from_env()
        self.vector_store, self.retriever = setup_vector_store(
            self.schema_info, resolved_vector_config
        )

        # Agents
        self.intent_agent = IntentAgent()
        self.table_agent = TableAgent(self.schema_info)
        self.column_prune_agent = ColumnPruneAgent(self.schema_info)
        self.sql_generator = SQLGenerator(self.schema_info, self.retriever)

    def generate_query(self, user_query: str) -> Dict[str, Any]:
        try:
            intent = self.intent_agent.determine_intent(user_query)
            tables = self.table_agent.determine_tables(user_query, intent.workspaces)
            pruned = self.column_prune_agent.prune_columns(user_query, tables.tables)

            # Retrieve similar samples directly using the retriever
            results = self.retriever.retrieve(user_query)
            samples = [
                cast(TextNode, r.node).text
                for r in results
                if r.node and hasattr(r.node, "text")
            ]

            sql_out = self.sql_generator.generate_sql(
                user_query,
                intent.workspaces,
                tables.tables,
                pruned.pruned_schema,
                samples,
            )

            # Execute for validation
            with sqlite3.connect("sample_university.db") as conn:
                df = pl.read_database(sql_out.sql, conn)
            return {
                "sql_result": sql_out,
                "query_result": df.head().to_dict(as_series=False),
            }
        except Exception as e:
            print(f"An error occurred during query generation: {e}")
            return {"error": str(e)}
