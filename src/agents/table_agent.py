from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Dict, Any


class TableSelection(BaseModel):
    tables: List[str] = Field(..., description="List of selected tables")
    explanation: str = Field(..., description="Explanation for table selection")


class TableAgent:
    def __init__(self, schema_info: Dict[str, Any]) -> None:
        self.schema_info = schema_info

    def determine_tables(self, query: str, workspaces: List[str]) -> TableSelection:
        schema_text = "\n".join(
            [
                f"Table '{t}': {', '.join([c['name'] for c in info['columns']])}"
                for t, info in self.schema_info.items()
            ]
        )
        prompt = f"""
        Based on the following user query and database schema, determine which tables are needed to answer the query.

        User Query: "{query}"
        Workspaces: {workspaces}

        Database Schema:
        {schema_text}

        Respond with a JSON object with the following structure:
        {{
            "tables": ["table1", "table2"],
            "explanation": "Brief explanation of why these tables were chosen"
        }}
        """
        agent: Agent[str, TableSelection] = Agent(
            model="gpt-4o-mini",
            system_prompt=prompt,
            output_type=TableSelection,
            retries=3,
        )
        result: TableSelection = agent.run_sync(query).output
        return result
