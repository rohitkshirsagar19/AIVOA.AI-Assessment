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


def test_post_chat_returns_follow_up_patch(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.tools.send_groq_test_prompt",
        lambda _: '{"tool_name":"set_follow_up_action","reason":"The user is setting a follow-up task."}',
    )
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"follow_up_action":"Send clinical study data","follow_up_date":"2026-07-10"}',
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={
                "message": "Set a follow-up for next Friday to send clinical study data.",
                "current_interaction": {"hcp_name": "Dr. Amit Mehta"},
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tool_calls"][0]["tool_name"] == "set_follow_up_action"
    assert payload["updated_fields"] == {
        "follow_up_action": "Send clinical study data",
        "follow_up_date": "2026-07-10",
    }
    assert payload["fields_updated"] == ["follow_up_action", "follow_up_date"]


def test_post_chat_returns_compliance_result(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.agent.tools.send_groq_test_prompt",
        lambda _: '{"tool_name":"check_compliance","reason":"The message asks for a compliance review."}',
    )
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: 'Use approved, evidence-based language and avoid absolute cure or safety claims.',
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/chat",
            json={"message": "Check compliance: CardioPlus is 100% safe and has no side effects."},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tool_calls"][0]["tool_name"] == "check_compliance"
    assert payload["updated_fields"]["compliance_status"] == "flagged"
    assert "compliance_issues" in payload["updated_fields"]
    assert "compliance_suggestion" in payload["updated_fields"]
