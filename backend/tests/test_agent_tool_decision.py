from app.agent.graph import run_interaction_graph
from app.agent.tools import parse_tool_decision


def test_parse_tool_decision_accepts_valid_json() -> None:
    result = parse_tool_decision(
        '{"tool_name":"search_hcp_profile","reason":"The user wants profile context before logging."}',
        "Show me Dr. Amit Mehta's profile before I log the meeting.",
    )

    assert result.tool_name == "search_hcp_profile"
    assert result.rationale == "The user wants profile context before logging."


def test_parse_tool_decision_extracts_embedded_json() -> None:
    result = parse_tool_decision(
        'Here is the result: {"tool_name":"check_compliance","reason":"The user asked for a compliance check."}',
        "Check compliance for this claim.",
    )

    assert result.tool_name == "check_compliance"


def test_graph_uses_llm_decision_when_json_is_valid(monkeypatch) -> None:
    def fake_send_groq_test_prompt(_: str) -> str:
        return '{"tool_name":"edit_interaction","reason":"The user is correcting a prior interaction entry."}'

    monkeypatch.setattr("app.agent.tools.send_groq_test_prompt", fake_send_groq_test_prompt)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"sentiment":"neutral"}',
    )

    result = run_interaction_graph(
        user_message="Actually, change the sentiment to neutral.",
        current_interaction={"sentiment": "positive"},
    )

    assert result["tool_used"] == "edit_interaction"
    assert result["updated_interaction"]["sentiment"] == "neutral"
    assert "Reason: The user is correcting a prior interaction entry." in result["assistant_message"]


def test_graph_falls_back_when_json_parsing_fails(monkeypatch) -> None:
    def fake_send_groq_test_prompt(_: str) -> str:
        return "not valid json"

    monkeypatch.setattr("app.agent.tools.send_groq_test_prompt", fake_send_groq_test_prompt)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"follow_up_action":"Send additional product information","follow_up_date":"2026-07-18"}',
    )

    result = run_interaction_graph(
        user_message="Set a follow-up for next Friday.",
        current_interaction={},
    )

    assert result["tool_used"] == "set_follow_up_action"
    assert result["updated_interaction"]["follow_up_action"] == "Send additional product information"
    assert result["updated_interaction"]["follow_up_date"] == "2026-07-18"
