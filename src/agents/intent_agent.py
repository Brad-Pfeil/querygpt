from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List


class WorkspaceClassification(BaseModel):
    workspaces: List[str] = Field(..., description="List of relevant workspaces")
    explanation: str = Field(..., description="Brief explanation")


class IntentAgent:
    def __init__(self) -> None:
        self.workspaces = [
            "student_management",
            "course_information",
            "academic_performance",
            "professor_workload",
            "department_statistics",
            "attendance_tracking",
        ]

    def determine_intent(self, user_query: str) -> WorkspaceClassification:
        prompt = f"""
        Based on the following user query, determine which workspace or workspaces it belongs to.
        The available workspaces are: {", ".join(self.workspaces)}

        User Query: "{user_query}"

        Respond with a JSON object with the following structure:
        {{
            "workspaces": ["workspace1", "workspace2"],
            "explanation": "Brief explanation of why these workspaces were chosen"
        }}
        """
        agent: Agent[str, WorkspaceClassification] = Agent(
            model="gpt-4o-mini",
            system_prompt=prompt,
            output_type=WorkspaceClassification,
            retries=3,
        )
        result: WorkspaceClassification = agent.run_sync(user_query).output
        return result
