from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.hcp import HCPProfileOut
from app.schemas.tool import ToolDecision


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    interaction_id: int | None = None
    current_interaction: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(strict=True, extra="forbid")


class ChatResponse(BaseModel):
    message: str
    tool_calls: list[ToolDecision] = Field(default_factory=list)
    updated_fields: dict[str, Any] = Field(default_factory=dict)
    fields_updated: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    hcp_profile: HCPProfileOut | None = None

    model_config = ConfigDict(strict=True, extra="forbid")
