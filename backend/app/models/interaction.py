from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hcp_profile_id: Mapped[int] = mapped_column(ForeignKey("hcp_profiles.id"), index=True)
    interaction_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    interaction_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product_discussed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    hcp_profile = relationship("HCPProfile", back_populates="interactions")
    follow_up_actions = relationship("FollowUpAction", back_populates="interaction", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="interaction", cascade="all, delete-orphan")
