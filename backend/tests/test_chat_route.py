from fastapi.testclient import TestClient

from app.main import app



def test_post_chat_returns_hcp_profile(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.tools.send_groq_test_prompt",
        lambda _: '{"tool_name":"search_hcp_profile","reason":"The user asked for profile lookup."}',
    )
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"hcp_name":"Dr. Amit Mehta"}',
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={"message": "Show me Dr. Amit Mehta's profile before I log the meeting."},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["hcp_profile"]["name"] == "Dr. Amit Mehta"
    assert payload["updated_fields"]["specialty"] == "Cardiologist"
    assert payload["fields_updated"] == ["hcp_name", "specialty", "location"]
    assert payload["tool_calls"][0]["tool_name"] == "search_hcp_profile"



def test_post_chat_returns_log_interaction_patch(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.tools.send_groq_test_prompt",
        lambda _: '{"tool_name":"log_interaction","reason":"The user is logging a meeting."}',
    )
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"hcp_name":"Dr. Amit Mehta","interaction_date":"2026-07-09","interaction_type":"in-person","product_discussed":"CardioPlus","topics_discussed":["efficacy"],"sentiment":"positive","materials_shared":["product brochure"],"key_outcomes":"HCP responded positively."}',
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={"message": "I met Dr. Amit Mehta today in person and shared a product brochure."},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tool_calls"][0]["tool_name"] == "log_interaction"
    assert payload["updated_fields"]["hcp_name"] == "Dr. Amit Mehta"
    assert payload["updated_fields"]["interaction_type"] == "in-person"
    assert "interaction_date" in payload["fields_updated"]


def test_post_chat_returns_edit_interaction_patch(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.tools.send_groq_test_prompt",
        lambda _: '{"tool_name":"edit_interaction","reason":"The user is correcting an existing interaction."}',
    )
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"sentiment":"neutral","key_outcomes":"HCP had concerns about pricing."}',
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={
                "message": "Actually, change the sentiment to neutral and add that he had concerns about pricing.",
                "current_interaction": {
                    "hcp_name": "Dr. Amit Mehta",
                    "sentiment": "positive",
                    "product_discussed": "CardioPlus"
                }
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tool_calls"][0]["tool_name"] == "edit_interaction"
    assert payload["updated_fields"] == {
        "sentiment": "neutral",
        "key_outcomes": "HCP had concerns about pricing.",
    }
    assert payload["fields_updated"] == ["sentiment", "key_outcomes"]
