from typing import Any

from app.agent.graph import run_interaction_graph



def run_chat_agent(
    *,
    session_id: str,
    message: str,
    current_interaction: dict[str, Any],
) -> dict[str, Any]:
    # Session tracking is not persisted yet, but the service contract accepts it now.
    return run_interaction_graph(
        user_message=message,
        current_interaction=current_interaction,
    )
