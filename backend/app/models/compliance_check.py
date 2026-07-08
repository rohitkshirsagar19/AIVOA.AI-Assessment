from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"), index=True)
    status: Mapped[str] = mapped_column(String(50))
    issues: Mapped[str | None] = mapped_column(Text(), nullable=True)
    suggestion: Mapped[str | None] = mapped_column(Text(), nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("Interaction", back_populates="compliance_checks")
