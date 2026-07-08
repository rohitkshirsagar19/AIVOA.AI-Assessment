from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.db.base import Base
from app.db.seed import seed_hcp_profiles
from app.models import ComplianceCheck, FollowUpAction, HCPProfile, Interaction


INTERACTION_SCHEMA_PATCHES = [
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS specialty VARCHAR(255)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS location VARCHAR(255)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS topics_discussed JSON DEFAULT '[]'::json",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS sentiment VARCHAR(100)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS materials_shared JSON DEFAULT '[]'::json",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS samples_shared JSON DEFAULT '[]'::json",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS key_outcomes TEXT",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS follow_up_action TEXT",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS follow_up_date DATE",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS compliance_status VARCHAR(50)",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS compliance_issues JSON DEFAULT '[]'::json",
    "ALTER TABLE interactions ADD COLUMN IF NOT EXISTS compliance_suggestion TEXT",
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _sync_interaction_table()

    with SessionLocal() as db:
        seed_hcp_profiles(db)


def _sync_interaction_table() -> None:
    with engine.begin() as connection:
        for statement in INTERACTION_SCHEMA_PATCHES:
            connection.execute(text(statement))
