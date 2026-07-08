from app.agent.graph import run_interaction_graph
from app.core.database import SessionLocal
from app.repositories.follow_up_repository import FollowUpActionRepository
from app.repositories.hcp_repository import HCPRepository



def test_set_follow_up_action_updates_interaction_and_persists_record(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="set_follow_up_action",
            rationale="The user is setting a follow-up action.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"follow_up_action":"Send clinical study data","follow_up_date":"2026-07-10"}',
    )

    result = run_interaction_graph(
        user_message="Set a follow-up for next Friday to send clinical study data.",
        current_interaction={"hcp_name": "Dr. Amit Mehta"},
    )

    assert result["tool_used"] == "set_follow_up_action"
    assert result["updated_interaction"]["follow_up_action"] == "Send clinical study data"
    assert result["updated_interaction"]["follow_up_date"] == "2026-07-10"
    assert result["fields_updated"] == ["follow_up_action", "follow_up_date"]
    assert "Follow-up action saved." in result["assistant_message"]

    with SessionLocal() as db:
        hcp_repository = HCPRepository(db)
        profile = hcp_repository.search_by_name("Dr. Amit Mehta")
        assert profile is not None
        follow_up_repository = FollowUpActionRepository(db)
        follow_ups = follow_up_repository.list_for_hcp(profile.id)
        assert any(
            follow_up.action == "Send clinical study data"
            and str(follow_up.due_date) == "2026-07-10"
            for follow_up in follow_ups
        )



def test_set_follow_up_action_skips_db_record_without_hcp_context(monkeypatch) -> None:
    def fake_classify(_: str):
        from app.schemas.tool import ToolDecision

        return ToolDecision(
            tool_name="set_follow_up_action",
            rationale="The user is setting a follow-up action.",
            arguments={},
        )

    monkeypatch.setattr("app.agent.graph.classify_tool_decision", fake_classify)
    monkeypatch.setattr(
        "app.agent.tools.send_groq_prompt",
        lambda _: '{"follow_up_action":"Send clinical study data","follow_up_date":"2026-07-10"}',
    )

    result = run_interaction_graph(
        user_message="Set a follow-up for next Friday to send clinical study data.",
        current_interaction={},
    )

    assert result["updated_interaction"]["follow_up_action"] == "Send clinical study data"
    assert result["updated_interaction"]["follow_up_date"] == "2026-07-10"
    assert result["fields_updated"] == ["follow_up_action", "follow_up_date"]
    assert "Follow-up action saved." not in result["assistant_message"]
