from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class InteractionPatch(BaseModel):
    hcp_name: str | None = None
    interaction_date: date | None = None
    interaction_type: str | None = None
    product_discussed: str | None = None
    topics_discussed: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    materials_shared: list[str] = Field(default_factory=list)
    key_outcomes: str | None = None

    model_config = ConfigDict(strict=True, extra="forbid")
