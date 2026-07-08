from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HCPProfile(Base):
    __tablename__ = "hcp_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    specialty: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    affiliation: Mapped[str] = mapped_column(String(255))
    preferred_channel: Mapped[str] = mapped_column(String(100))
    last_interaction_summary: Mapped[str | None] = mapped_column(Text(), nullable=True)

    interactions = relationship("Interaction", back_populates="hcp_profile", cascade="all, delete-orphan")
    follow_up_actions = relationship("FollowUpAction", back_populates="hcp_profile", cascade="all, delete-orphan")
