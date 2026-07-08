from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class InteractionPatch(BaseModel):
    hcp_name: str | None = None
    specialty: str | None = None
    location: str | None = None
    interaction_date: date | None = None
    interaction_type: str | None = None
    product_discussed: str | None = None
    topics_discussed: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    materials_shared: list[str] = Field(default_factory=list)
    samples_shared: list[str] = Field(default_factory=list)
    key_outcomes: str | None = None
    follow_up_action: str | None = None
    follow_up_date: date | None = None
    compliance_status: str | None = None
    compliance_issues: list[str] = Field(default_factory=list)
    compliance_suggestion: str | None = None

    model_config = ConfigDict(strict=True, extra="forbid")


class InteractionRecord(BaseModel):
    hcp_name: str | None = None
    specialty: str | None = None
    location: str | None = None
    interaction_date: date | None = None
    interaction_type: str | None = None
    product_discussed: str | None = None
    topics_discussed: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    materials_shared: list[str] = Field(default_factory=list)
    samples_shared: list[str] = Field(default_factory=list)
    key_outcomes: str | None = None
    follow_up_action: str | None = None
    follow_up_date: date | None = None
    compliance_status: str | None = None
    compliance_issues: list[str] = Field(default_factory=list)
    compliance_suggestion: str | None = None

    model_config = ConfigDict(extra="forbid")


class InteractionSaveRequest(BaseModel):
    current_interaction: InteractionRecord

    model_config = ConfigDict(extra="forbid")


class InteractionSaveResponse(BaseModel):
    id: int
    message: str

    model_config = ConfigDict(strict=True, extra="forbid")
