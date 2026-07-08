from app.agent.graph import run_interaction_graph



def test_edit_interaction_updates_only_explicit_fields(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="edit_interaction",
            rationale="The user is correcting an existing interaction.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"sentiment":"neutral","key_outcomes":"HCP had concerns about pricing."}',
    )

    current_interaction = {
        "hcp_name": "Dr. Amit Mehta",
        "interaction_type": "in-person",
        "product_discussed": "CardioPlus",
        "sentiment": "positive",
        "topics_discussed": ["efficacy"],
    }

    result = run_interaction_graph(
        user_message="Actually, change the sentiment to neutral and add that he had concerns about pricing.",
        current_interaction=current_interaction,
    )

    assert result["tool_used"] == "edit_interaction"
    assert result["updated_interaction"] == {
        "hcp_name": "Dr. Amit Mehta",
        "interaction_type": "in-person",
        "product_discussed": "CardioPlus",
        "sentiment": "neutral",
        "topics_discussed": ["efficacy"],
        "key_outcomes": "HCP had concerns about pricing.",
    }
    assert result["fields_updated"] == ["sentiment", "key_outcomes"]
    assert "Updated interaction fields: sentiment, key_outcomes." in result["assistant_message"]



def test_edit_interaction_preserves_unrelated_fields_when_payload_is_empty(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="edit_interaction",
            rationale="The user is correcting an existing interaction.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr("app.agent.tools.send_groq_prompt", lambda _: '{}')

    current_interaction = {
        "hcp_name": "Dr. Amit Mehta",
        "interaction_type": "in-person",
        "sentiment": "positive",
    }

    result = run_interaction_graph(
        user_message="Actually, update it.",
        current_interaction=current_interaction,
    )

    assert result["updated_interaction"] == current_interaction
    assert result["fields_updated"] == []
    assert result["assistant_message"].startswith("No explicit interaction changes were identified")
