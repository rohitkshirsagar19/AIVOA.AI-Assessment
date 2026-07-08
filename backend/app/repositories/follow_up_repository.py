from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.follow_up_action import FollowUpAction


class FollowUpActionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        hcp_profile_id: int,
        action: str,
        due_date: date | None,
        interaction_id: int | None = None,
        status: str = "pending",
    ) -> FollowUpAction:
        follow_up = FollowUpAction(
            hcp_profile_id=hcp_profile_id,
            interaction_id=interaction_id,
            action=action,
            due_date=due_date,
            status=status,
        )
        self.db.add(follow_up)
        self.db.commit()
        self.db.refresh(follow_up)
        return follow_up

    def list_for_hcp(self, hcp_profile_id: int) -> list[FollowUpAction]:
        statement = (
            select(FollowUpAction)
            .where(FollowUpAction.hcp_profile_id == hcp_profile_id)
            .order_by(FollowUpAction.created_at.desc())
        )
        return list(self.db.scalars(statement).all())
