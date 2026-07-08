from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tool import ToolDecision


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    interaction_id: int | None = None

    model_config = ConfigDict(strict=True, extra="forbid")


class ChatResponse(BaseModel):
    message: str
    tool_calls: list[ToolDecision] = Field(default_factory=list)
    updated_fields: dict[str, str | int | float | bool | list[str] | None] = Field(
        default_factory=dict
    )
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(strict=True, extra="forbid")
