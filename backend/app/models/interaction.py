from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hcp_profile_id: Mapped[int] = mapped_column(ForeignKey("hcp_profiles.id"), index=True)
    specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interaction_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    interaction_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product_discussed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    topics_discussed: Mapped[list[str]] = mapped_column(JSON, default=list)
    sentiment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    materials_shared: Mapped[list[str]] = mapped_column(JSON, default=list)
    samples_shared: Mapped[list[str]] = mapped_column(JSON, default=list)
    key_outcomes: Mapped[str | None] = mapped_column(Text(), nullable=True)
    follow_up_action: Mapped[str | None] = mapped_column(Text(), nullable=True)
    follow_up_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    compliance_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    compliance_issues: Mapped[list[str]] = mapped_column(JSON, default=list)
    compliance_suggestion: Mapped[str | None] = mapped_column(Text(), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    hcp_profile = relationship("HCPProfile", back_populates="interactions")
    follow_up_actions = relationship("FollowUpAction", back_populates="interaction", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="interaction", cascade="all, delete-orphan")
