from app.agent.graph import run_interaction_graph



def test_log_interaction_merges_validated_patch(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="log_interaction",
            rationale="The user is describing an HCP meeting.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"hcp_name":"Dr. Amit Mehta","interaction_date":"2026-07-09","interaction_type":"in-person","product_discussed":"CardioPlus","topics_discussed":["efficacy","patient adherence"],"sentiment":"positive","materials_shared":["product brochure"],"key_outcomes":"HCP responded positively."}',
    )

    result = run_interaction_graph(
        user_message="I met Dr. Amit Mehta today in person. We discussed CardioPlus efficacy and patient adherence. He was positive and I shared a product brochure.",
        current_interaction={"topics_discussed": ["pricing"]},
    )

    assert result["tool_used"] == "log_interaction"
    assert result["updated_interaction"]["hcp_name"] == "Dr. Amit Mehta"
    assert result["updated_interaction"]["topics_discussed"] == ["pricing", "efficacy", "patient adherence"]
    assert result["fields_updated"] == [
        "hcp_name",
        "interaction_date",
        "interaction_type",
        "product_discussed",
        "topics_discussed",
        "sentiment",
        "materials_shared",
        "key_outcomes",
    ]
    assert "Logged interaction details and updated:" in result["assistant_message"]



def test_log_interaction_returns_no_changes_for_invalid_payload(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="log_interaction",
            rationale="The user is describing an HCP meeting.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr("app.agent.tools.send_groq_prompt", lambda _: 'not valid json')

    result = run_interaction_graph(
        user_message="Met the doctor today.",
        current_interaction={"hcp_name": "Dr. Amit Mehta"},
    )

    assert result["updated_interaction"] == {"hcp_name": "Dr. Amit Mehta"}
    assert result["fields_updated"] == []
    assert result["assistant_message"].startswith("No interaction fields could be confirmed")
