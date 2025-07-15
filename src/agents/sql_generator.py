from pydantic import BaseModel, Field
from pydantic_ai import Agent
from llama_index.core.base.base_retriever import BaseRetriever
from typing import List, Dict, Any


class SQLGeneration(BaseModel):
    sql: str = Field(..., description="The generated SQL query")
    explanation: str = Field(..., description="Explanation of the SQL query")


class SQLGenerator:
    def __init__(self, schema_info: Dict[str, Any], retriever: BaseRetriever) -> None:
        self.schema_info = schema_info
        self.retriever = retriever

    def generate_sql(
        self,
        query: str,
        workspaces: List[str],
        tables: List[str],
        pruned: Dict[str, List[str]],
        samples: List[str],
    ) -> SQLGeneration:
        schema_text = "\n".join(
            [f"Table '{t}': {', '.join(pruned.get(t, []))}" for t in tables]
        )
        samples_text = "\n\n".join(samples)
        prompt = f"""
You are an expert SQL generator. Convert the following natural language question into a syntactically correct SQL query.
Use the provided database schema to inform your query construction.
Instructions:
- Given an input question, first create a syntactically correct query to run.
- Never query for all the columns from a specific table; only ask for a few relevant columns given the question.
- Pay attention to use only the column names that you can see in the schema description.
- Be careful not to query columns that do not exist.
- Pay attention to which column belongs to which table.
- Qualify column names with the table name when needed.

- Database Schema:
{schema_text}

- Here are some examples of questions and their corresponding SQL queries:
{samples_text.strip()}

Now, generate an SQL query for the following question:
Question: {query}

Respond with a JSON object with the following structure:
{{
    "sql": "The SQL query",
    "explanation": "Step-by-step explanation of how the query works"
}}
"""
        agent: Agent[str, SQLGeneration] = Agent(
            model="gpt-4o-mini",
            system_prompt=prompt,
            output_type=SQLGeneration,
            retries=3,
        )
        result: SQLGeneration = agent.run_sync(query).output
        return result
