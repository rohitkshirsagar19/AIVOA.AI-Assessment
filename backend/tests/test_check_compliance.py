from app.agent.graph import run_interaction_graph



def test_check_compliance_flags_risky_claims_and_adds_suggestion(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="check_compliance",
            rationale="The user is asking for a compliance review.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: "Use approved, evidence-based language and avoid absolute cure or safety claims.",
    )

    result = run_interaction_graph(
        user_message="Check compliance: CardioPlus guarantees complete cure, is 100% safe, and has no side effects.",
        current_interaction={},
    )

    assert result["tool_used"] == "check_compliance"
    assert result["updated_interaction"]["compliance_status"] == "flagged"
    assert result["updated_interaction"]["compliance_issues"] == [
        "Claims no side effects",
        "Claims 100% safe",
    ] or result["updated_interaction"]["compliance_issues"] == [
        "Claims 100% safe",
        "Claims no side effects",
    ]
    assert "evidence-based" in result["updated_interaction"]["compliance_suggestion"]
    assert result["fields_updated"] == [
        "compliance_status",
        "compliance_issues",
        "compliance_suggestion",
    ]



def test_check_compliance_returns_clear_when_no_rules_match(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="check_compliance",
            rationale="The user is asking for a compliance review.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)

    result = run_interaction_graph(
        user_message="Check compliance: We discussed approved clinical data and patient adherence.",
        current_interaction={},
    )

    assert result["updated_interaction"]["compliance_status"] == "clear"
    assert result["updated_interaction"]["compliance_issues"] == []
    assert result["updated_interaction"]["compliance_suggestion"] == "No risky compliance language detected."
