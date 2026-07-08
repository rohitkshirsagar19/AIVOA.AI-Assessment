from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class FollowUpActionOut(BaseModel):
    id: int
    hcp_profile_id: int
    interaction_id: int | None
    action: str
    due_date: date | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")
