from langgraph.graph import END, START, StateGraph

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools import classify_tool_decision, fallback_tool_decision, run_tool



def agent_node(state: AgentState) -> dict[str, object]:
    decision = classify_tool_decision(state["user_message"])
    return {
        "tool_decision": decision,
        "tool_used": decision.tool_name,
    }



def tool_node(state: AgentState) -> dict[str, object]:
    decision = state["tool_decision"] or fallback_tool_decision(state["user_message"])
    return run_tool(
        decision.tool_name,
        state["user_message"],
        state.get("current_interaction", {}),
    )



def response_node(state: AgentState) -> dict[str, object]:
    rationale = state["tool_decision"].rationale if state["tool_decision"] else "No rationale available."
    tool_message = state.get("tool_message")

    if tool_message:
        assistant_message = f"{tool_message} Reason: {rationale}"
    elif state.get("hcp_profile") is not None:
        profile = state["hcp_profile"]
        assistant_message = (
            f"Found HCP profile for {profile['name']} ({profile['specialty']}, {profile['location']}). "
            f"Reason: {rationale}"
        )
    else:
        assistant_message = (
            f"{SYSTEM_PROMPT.strip()}\n\n"
            f"Tool selected: {state['tool_used']}. Reason: {rationale}"
        )

    return {"assistant_message": assistant_message}



def build_interaction_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent_node", agent_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("response_node", response_node)
    graph.add_edge(START, "agent_node")
    graph.add_edge("agent_node", "tool_node")
    graph.add_edge("tool_node", "response_node")
    graph.add_edge("response_node", END)
    return graph.compile()



def run_interaction_graph(
    user_message: str, current_interaction: dict[str, object] | None = None
) -> dict[str, object]:
    app = build_interaction_graph()
    initial_state: AgentState = {
        "user_message": user_message,
        "current_interaction": dict(current_interaction or {}),
        "assistant_message": "",
        "tool_decision": None,
        "tool_used": "",
        "updated_interaction": {},
        "fields_updated": [],
        "hcp_profile": None,
        "tool_message": None,
    }
    result = app.invoke(initial_state)
    return {
        "assistant_message": result["assistant_message"],
        "tool_used": result["tool_used"],
        "updated_interaction": result["updated_interaction"],
        "fields_updated": result.get("fields_updated", []),
        "hcp_profile": result.get("hcp_profile"),
        "tool_decision": result.get("tool_decision"),
    }
