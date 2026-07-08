from app.agent.graph import run_interaction_graph



def test_search_hcp_profile_updates_state_from_seeded_db(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="search_hcp_profile",
            rationale="The user wants HCP profile context.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr("app.agent.tools.send_groq_prompt", lambda _: '{"hcp_name":"Dr. Amit Mehta"}')

    result = run_interaction_graph(
        user_message="Show me Dr. Amit Mehta's profile before I log the meeting.",
        current_interaction={},
    )

    assert result["tool_used"] == "search_hcp_profile"
    assert result["hcp_profile"]["name"] == "Dr. Amit Mehta"
    assert result["updated_interaction"]["hcp_name"] == "Dr. Amit Mehta"
    assert result["updated_interaction"]["specialty"] == "Cardiologist"
