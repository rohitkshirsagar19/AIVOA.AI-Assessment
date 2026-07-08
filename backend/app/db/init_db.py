from app.core.database import SessionLocal, engine
from app.db.base import Base
from app.db.seed import seed_hcp_profiles
from app.models import ComplianceCheck, FollowUpAction, HCPProfile, Interaction



def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        seed_hcp_profiles(db)
