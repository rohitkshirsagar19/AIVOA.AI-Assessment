from pydantic import BaseModel, ConfigDict


class HCPProfileRead(BaseModel):
    id: int
    name: str
    specialty: str
    location: str
    affiliation: str
    preferred_channel: str
    last_interaction_summary: str | None

    model_config = ConfigDict(from_attributes=True)
