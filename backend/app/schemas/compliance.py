from pydantic import BaseModel, ConfigDict, Field


class ComplianceResult(BaseModel):
    compliance_status: str
    compliance_issues: list[str] = Field(default_factory=list)
    compliance_suggestion: str | None = None

    model_config = ConfigDict(strict=True, extra="forbid")
