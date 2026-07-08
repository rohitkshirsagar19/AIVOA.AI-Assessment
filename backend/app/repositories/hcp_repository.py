from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.hcp_profile import HCPProfile


class HCPRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_profiles(self) -> list[HCPProfile]:
        statement = select(HCPProfile).order_by(HCPProfile.name.asc())
        return list(self.db.scalars(statement).all())

    def get_by_name(self, name: str) -> HCPProfile | None:
        statement = select(HCPProfile).where(HCPProfile.name == name)
        return self.db.scalar(statement)

    def search_by_name(self, name: str) -> HCPProfile | None:
        normalized = name.strip().lower()
        if not normalized:
            return None

        exact_statement = select(HCPProfile).where(func.lower(HCPProfile.name) == normalized)
        exact_match = self.db.scalar(exact_statement)
        if exact_match is not None:
            return exact_match

        fragment = f"%{normalized}%"
        partial_statement = select(HCPProfile).where(
            or_(
                func.lower(HCPProfile.name).like(fragment),
                func.lower(HCPProfile.affiliation).like(fragment),
            )
        )
        return self.db.scalar(partial_statement)
