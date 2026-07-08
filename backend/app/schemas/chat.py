from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.hcp import HCPProfileOut
from app.schemas.tool import ToolDecision


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
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
