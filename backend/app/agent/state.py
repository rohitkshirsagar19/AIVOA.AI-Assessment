from typing import Any, TypedDict

from app.schemas.tool import ToolDecision


class AgentState(TypedDict):
    user_message: str
    current_interaction: dict[str, Any]
    assistant_message: str
    tool_decision: ToolDecision | None
    tool_used: str
    updated_interaction: dict[str, Any]
