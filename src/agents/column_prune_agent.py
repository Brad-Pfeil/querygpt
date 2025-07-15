from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Dict, Any


class PrunedSchemaSelection(BaseModel):
    pruned_schema: Dict[str, List[str]] = Field(..., description="Pruned schema")
    explanation: str = Field(..., description="Explanation")


class ColumnPruneAgent:
    def __init__(self, schema_info: Dict[str, Any]) -> None:
        self.schema_info = schema_info

    def prune_columns(self, query: str, tables: List[str]) -> PrunedSchemaSelection:
        schema_text = "\n".join(
            [
                f"Table '{t}': {', '.join([c['name'] for c in self.schema_info[t]['columns']])}"
                for t in tables
            ]
        )
        prompt = f"""
        Based on the following user query and the tables that have been selected, determine which columns are relevant to answer the query.

        User Query: "{query}"

        Selected Tables Schema:
        {schema_text}

        For each table, return only the columns that are necessary to answer the query.
        Respond with a JSON object with the following structure:
        {{
            "pruned_schema": {{
                "table_name1": ["column1", "column2"],
                "table_name2": ["column1", "column3"]
            }},
            "explanation": "Brief explanation of why these columns were chosen"
        }}
        """
        agent = Agent(
            model="gpt-4o-mini",
            system_prompt=prompt,
            output_type=PrunedSchemaSelection,
            retries=3,
        )
        result: PrunedSchemaSelection = agent.run_sync(query).output
        return result
