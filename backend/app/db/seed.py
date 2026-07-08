from sqlalchemy.orm import Session

from app.models.hcp_profile import HCPProfile
from app.repositories.hcp_repository import HCPRepository


SEED_HCPS = [
    {
        "name": "Dr. Amit Mehta",
        "specialty": "Cardiologist",
        "location": "Mumbai",
        "affiliation": "City Heart Clinic",
        "preferred_channel": "In-person visit",
        "last_interaction_summary": "Discussed CardioPlus efficacy and requested follow-up data.",
    },
    {
        "name": "Dr. Neha Sharma",
        "specialty": "Endocrinologist",
        "location": "Delhi",
        "affiliation": "Metro Care Hospital",
        "preferred_channel": "Video call",
        "last_interaction_summary": "Reviewed diabetes therapy adherence trends.",
    },
    {
        "name": "Dr. Rajiv Iyer",
        "specialty": "Pulmonologist",
        "location": "Bengaluru",
        "affiliation": "Lakeside Medical Center",
        "preferred_channel": "Email",
        "last_interaction_summary": "Asked for updated respiratory study materials.",
    },
    {
        "name": "Dr. Priya Nair",
        "specialty": "Neurologist",
        "location": "Chennai",
        "affiliation": "NeuroPlus Institute",
        "preferred_channel": "In-person visit",
        "last_interaction_summary": "Shared interest in recent migraine patient outcomes.",
    },
    {
        "name": "Dr. Sameer Khan",
        "specialty": "Oncologist",
        "location": "Hyderabad",
        "affiliation": "Care Oncology Partners",
        "preferred_channel": "Phone call",
        "last_interaction_summary": "Requested a pricing discussion for the next touchpoint.",
    },
]


def seed_hcp_profiles(db: Session) -> None:
    repository = HCPRepository(db)
    inserted = False

    for payload in SEED_HCPS:
        if repository.get_by_name(payload["name"]) is not None:
            continue
        db.add(HCPProfile(**payload))
        inserted = True

    if inserted:
        db.commit()
