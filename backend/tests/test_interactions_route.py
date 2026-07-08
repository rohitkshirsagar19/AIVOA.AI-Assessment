from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.interaction import Interaction


def test_post_interactions_saves_ai_filled_interaction() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/interactions",
            json={
                "current_interaction": {
                    "hcp_name": "Dr. Amit Mehta",
                    "specialty": "Cardiologist",
                    "location": "Mumbai",
                    "interaction_date": "2026-07-09",
                    "interaction_type": "in-person",
                    "product_discussed": "CardioPlus",
                    "topics_discussed": ["efficacy", "patient adherence"],
                    "sentiment": "positive",
                    "materials_shared": ["product brochure"],
                    "samples_shared": [],
                    "key_outcomes": "Doctor was receptive and asked for more data.",
                    "follow_up_action": "Send clinical study data",
                    "follow_up_date": "2026-07-17",
                    "compliance_status": "clear",
                    "compliance_issues": [],
                    "compliance_suggestion": "No risky language detected.",
                }
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["message"] == "Interaction saved for Dr. Amit Mehta."
    assert isinstance(payload["id"], int)

    with SessionLocal() as db:
        record = db.get(Interaction, payload["id"])
        assert record is not None
        assert record.product_discussed == "CardioPlus"
        assert record.topics_discussed == ["efficacy", "patient adherence"]
        assert record.follow_up_action == "Send clinical study data"
        assert record.compliance_status == "clear"


def test_post_interactions_rejects_incomplete_interaction() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/interactions",
            json={
                "current_interaction": {
                    "hcp_name": "Dr. Amit Mehta",
                    "topics_discussed": [],
                    "materials_shared": [],
                    "samples_shared": [],
                    "compliance_issues": [],
                }
            },
        )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "Interaction needs an HCP name and at least one meaningful detail before it can be saved."
    )
