from pydantic import BaseModel, ConfigDict, Field


class ToolDecision(BaseModel):
    tool_name: str
    rationale: str
    arguments: dict[str, str | int | float | bool | list[str] | None] = Field(
        default_factory=dict
    )

    model_config = ConfigDict(strict=True, extra="forbid")
