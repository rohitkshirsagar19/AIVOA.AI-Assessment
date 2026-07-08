from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FollowUpAction(Base):
    __tablename__ = "follow_up_actions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hcp_profile_id: Mapped[int] = mapped_column(ForeignKey("hcp_profiles.id"), index=True)
    interaction_id: Mapped[int | None] = mapped_column(ForeignKey("interactions.id"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(255))
    due_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    hcp_profile = relationship("HCPProfile", back_populates="follow_up_actions")
    interaction = relationship("Interaction", back_populates="follow_up_actions")
