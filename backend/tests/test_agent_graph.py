from app.agent.graph import run_interaction_graph



def test_graph_executes_with_default_mock_tool() -> None:
    result = run_interaction_graph(
        user_message="I met Dr. Amit Mehta today and discussed efficacy.",
        current_interaction={"hcp_name": "Dr. Amit Mehta"},
    )

    assert result["tool_used"] == "log_interaction"
    assert result["updated_interaction"]["hcp_name"] == "Dr. Amit Mehta"
    assert result["updated_interaction"]["interaction_type"] == "in-person"
    assert "Tool selected: log_interaction." in result["assistant_message"]



def test_graph_executes_follow_up_mock_path() -> None:
    result = run_interaction_graph(
        user_message="Set a follow-up for next week.",
        current_interaction={},
    )

    assert result["tool_used"] == "set_follow_up_action"
    assert result["updated_interaction"]["follow_up_action"] == "Send additional product information"
