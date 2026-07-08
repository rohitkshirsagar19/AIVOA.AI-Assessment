import json
import re
from typing import Any

from app.agent.prompts import TOOL_CLASSIFICATION_PROMPT
from app.schemas.tool import ToolDecision
from app.services.groq_client import GroqConfigurationError, send_groq_test_prompt

ALLOWED_TOOLS = {
    "log_interaction",
    "edit_interaction",
    "set_follow_up_action",
    "check_compliance",
    "search_hcp_profile",
}

MOCK_INTERACTION_UPDATE = {
    "interaction_type": "in-person",
    "sentiment": "positive",
    "topics_discussed": ["efficacy"],
}


class ToolDecisionParseError(ValueError):
    """Raised when the LLM tool decision cannot be parsed safely."""



def classify_tool_decision(user_message: str) -> ToolDecision:
    prompt = TOOL_CLASSIFICATION_PROMPT.format(user_message=user_message)

    try:
        raw_response = send_groq_test_prompt(prompt)
        return parse_tool_decision(raw_response, user_message)
    except (GroqConfigurationError, ToolDecisionParseError, RuntimeError):
        return fallback_tool_decision(user_message)



def parse_tool_decision(raw_response: str, user_message: str) -> ToolDecision:
    payload = _extract_json_payload(raw_response)

    tool_name = payload.get("tool_name")
    reason = payload.get("reason")

    if tool_name not in ALLOWED_TOOLS:
        raise ToolDecisionParseError("LLM returned an unsupported tool name.")

    if not isinstance(reason, str) or not reason.strip():
        raise ToolDecisionParseError("LLM returned an invalid reason.")

    return ToolDecision(
        tool_name=tool_name,
        rationale=reason.strip(),
        arguments={"message": user_message},
    )



def _extract_json_payload(raw_response: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not match:
            raise ToolDecisionParseError("No JSON object found in LLM response.")
        try:
            payload = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise ToolDecisionParseError("Invalid JSON returned by LLM.") from exc

    if not isinstance(payload, dict):
        raise ToolDecisionParseError("LLM response must decode to a JSON object.")

    return payload



def fallback_tool_decision(user_message: str) -> ToolDecision:
    normalized = user_message.lower()

    if "profile" in normalized or "previous interaction" in normalized:
        tool_name = "search_hcp_profile"
        reason = "Fallback matched an HCP profile lookup request."
    elif "change" in normalized or "actually" in normalized or "update" in normalized:
        tool_name = "edit_interaction"
        reason = "Fallback matched an interaction correction request."
    elif "follow-up" in normalized or "follow up" in normalized:
        tool_name = "set_follow_up_action"
        reason = "Fallback matched a follow-up request."
    elif "compliance" in normalized or "side effects" in normalized:
        tool_name = "check_compliance"
        reason = "Fallback matched a compliance review request."
    else:
        tool_name = "log_interaction"
        reason = "Fallback defaulted to interaction logging."

    return ToolDecision(
        tool_name=tool_name,
        rationale=reason,
        arguments={"message": user_message},
    )



def run_mock_tool(tool_name: str, current_interaction: dict[str, Any]) -> dict[str, Any]:
    updated_interaction = dict(current_interaction)

    if tool_name == "log_interaction":
        updated_interaction.update(MOCK_INTERACTION_UPDATE)
    elif tool_name == "set_follow_up_action":
        updated_interaction["follow_up_action"] = "Send additional product information"
    elif tool_name == "check_compliance":
        updated_interaction["compliance_status"] = "clear"
    elif tool_name == "search_hcp_profile":
        updated_interaction["profile_lookup_requested"] = True
    elif tool_name == "edit_interaction":
        updated_interaction["interaction_edit_requested"] = True

    return updated_interaction
