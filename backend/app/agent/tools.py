from datetime import date
import json
import re
from typing import Any

from app.agent.prompts import (
    COMPLIANCE_SUGGESTION_PROMPT,
    EDIT_INTERACTION_EXTRACTION_PROMPT,
    FOLLOW_UP_EXTRACTION_PROMPT,
    HCP_NAME_EXTRACTION_PROMPT,
    LOG_INTERACTION_EXTRACTION_PROMPT,
    TOOL_CLASSIFICATION_PROMPT,
)
from app.core.database import SessionLocal
from app.repositories.follow_up_repository import FollowUpActionRepository
from app.repositories.hcp_repository import HCPRepository
from app.schemas.compliance import ComplianceResult
from app.schemas.hcp import HCPProfileOut
from app.schemas.interaction import InteractionPatch
from app.schemas.tool import ToolDecision
from app.services.groq_client import GroqConfigurationError, send_groq_prompt, send_groq_test_prompt
from app.services.interaction_merge import merge_interaction_patch

ALLOWED_TOOLS = {
    "log_interaction",
    "edit_interaction",
    "set_follow_up_action",
    "check_compliance",
    "search_hcp_profile",
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



def extract_hcp_name(user_message: str) -> str | None:
    prompt = HCP_NAME_EXTRACTION_PROMPT.format(user_message=user_message)

    try:
        raw_response = send_groq_prompt(prompt)
        payload = _extract_json_payload(raw_response)
        hcp_name = payload.get("hcp_name")
        if isinstance(hcp_name, str) and hcp_name.strip():
            return hcp_name.strip()
    except (GroqConfigurationError, RuntimeError, ToolDecisionParseError):
        pass

    return _fallback_extract_hcp_name(user_message)



def _fallback_extract_hcp_name(user_message: str) -> str | None:
    normalized_message = user_message.lower()

    with SessionLocal() as db:
        repository = HCPRepository(db)
        for profile in repository.list_profiles():
            full_name = profile.name.lower()
            last_name = full_name.split()[-1]
            if full_name in normalized_message or last_name in normalized_message:
                return profile.name

    return None



def extract_interaction_patch(user_message: str) -> InteractionPatch:
    prompt = LOG_INTERACTION_EXTRACTION_PROMPT.replace("{user_message}", user_message)

    try:
        raw_response = send_groq_prompt(prompt)
        payload = _extract_json_payload(raw_response)
        return InteractionPatch.model_validate_json(json.dumps(payload))
    except Exception:
        return InteractionPatch()



def log_interaction_tool(user_message: str, current_interaction: dict[str, Any]) -> dict[str, Any]:
    patch = extract_interaction_patch(user_message)
    merge_result = merge_interaction_patch(current_interaction, patch)
    fields_updated = merge_result["fields_updated"]

    if fields_updated:
        assistant_message = "Logged interaction details and updated: " + ", ".join(fields_updated) + "."
    else:
        assistant_message = "No interaction fields could be confirmed from the message."

    return {
        "updated_interaction": merge_result["updated_interaction"],
        "fields_updated": fields_updated,
        "hcp_profile": None,
        "tool_message": assistant_message,
    }



COMPLIANCE_RULES = {
    "guaranteed cure": "Guaranteed cure claim",
    "no side effects": "Claims no side effects",
    "100% safe": "Claims 100% safe",
    "better than all competitors": "Comparative superiority claim",
    "off-label use": "Mentions off-label use",
}



def detect_compliance_issues(user_message: str) -> list[str]:
    normalized = user_message.lower()
    issues: list[str] = []

    for phrase, label in COMPLIANCE_RULES.items():
        if phrase in normalized:
            issues.append(label)

    return issues



def generate_compliance_suggestion(user_message: str, issues: list[str]) -> str:
    prompt = COMPLIANCE_SUGGESTION_PROMPT.format(
        issues=", ".join(issues),
        user_message=user_message,
    )

    try:
        suggestion = send_groq_prompt(prompt)
        cleaned = suggestion.strip()
        if cleaned:
            return cleaned
    except Exception:
        pass

    return "Use approved, evidence-based product language and avoid absolute safety, efficacy, or off-label claims."



def check_compliance_tool(user_message: str, current_interaction: dict[str, Any]) -> dict[str, Any]:
    issues = detect_compliance_issues(user_message)
    status = "flagged" if issues else "clear"
    suggestion = generate_compliance_suggestion(user_message, issues) if issues else "No risky compliance language detected."

    result = ComplianceResult(
        compliance_status=status,
        compliance_issues=issues,
        compliance_suggestion=suggestion,
    )

    updated_interaction = dict(current_interaction)
    updated_interaction.update(result.model_dump())

    fields_updated = [
        "compliance_status",
        "compliance_issues",
        "compliance_suggestion",
    ]

    if status == "flagged":
        assistant_message = "Compliance review flagged risky language and added a safer suggestion."
    else:
        assistant_message = "Compliance review found no risky language."

    return {
        "updated_interaction": updated_interaction,
        "fields_updated": fields_updated,
        "hcp_profile": None,
        "tool_message": assistant_message,
    }


def extract_follow_up_payload(user_message: str) -> dict[str, Any]:
    prompt = FOLLOW_UP_EXTRACTION_PROMPT.replace("{user_message}", user_message)

    try:
        raw_response = send_groq_prompt(prompt)
        payload = _extract_json_payload(raw_response)
        if not isinstance(payload.get("follow_up_action"), (str, type(None))):
            payload["follow_up_action"] = None
        if not isinstance(payload.get("follow_up_date"), (str, type(None))):
            payload["follow_up_date"] = None
        return payload
    except Exception:
        return {"follow_up_action": None, "follow_up_date": None}



def set_follow_up_action_tool(
    user_message: str, current_interaction: dict[str, Any]
) -> dict[str, Any]:
    payload = extract_follow_up_payload(user_message)
    updated_interaction = dict(current_interaction)
    fields_updated: list[str] = []

    follow_up_action = payload.get("follow_up_action")
    follow_up_date = payload.get("follow_up_date")

    if isinstance(follow_up_action, str) and follow_up_action.strip():
        updated_interaction["follow_up_action"] = follow_up_action.strip()
        fields_updated.append("follow_up_action")
    else:
        follow_up_action = None

    if isinstance(follow_up_date, str) and follow_up_date.strip():
        updated_interaction["follow_up_date"] = follow_up_date.strip()
        fields_updated.append("follow_up_date")
    else:
        follow_up_date = None

    created_record = False
    hcp_name = updated_interaction.get("hcp_name")
    if follow_up_action and hcp_name:
        with SessionLocal() as db:
            hcp_repository = HCPRepository(db)
            profile = hcp_repository.search_by_name(str(hcp_name))
            if profile is not None:
                follow_up_repository = FollowUpActionRepository(db)
                follow_up_repository.create(
                    hcp_profile_id=profile.id,
                    action=follow_up_action,
                    due_date=date.fromisoformat(follow_up_date) if follow_up_date else None,
                )
                created_record = True

    if fields_updated:
        assistant_message = "Updated follow-up details: " + ", ".join(fields_updated) + "."
        if created_record:
            assistant_message += " Follow-up action saved."
    else:
        assistant_message = "No follow-up details could be confirmed from the message."

    return {
        "updated_interaction": updated_interaction,
        "fields_updated": fields_updated,
        "hcp_profile": None,
        "tool_message": assistant_message,
    }


def extract_edit_interaction_patch(
    user_message: str, current_interaction: dict[str, Any]
) -> InteractionPatch:
    prompt = EDIT_INTERACTION_EXTRACTION_PROMPT.format(
        current_interaction=json.dumps(current_interaction, default=str, sort_keys=True),
        user_message=user_message,
    )

    try:
        raw_response = send_groq_prompt(prompt)
        payload = _extract_json_payload(raw_response)
        return InteractionPatch.model_validate_json(json.dumps(payload))
    except Exception:
        return InteractionPatch()



def edit_interaction_tool(user_message: str, current_interaction: dict[str, Any]) -> dict[str, Any]:
    patch = extract_edit_interaction_patch(user_message, current_interaction)
    merge_result = merge_interaction_patch(current_interaction, patch)
    fields_updated = merge_result["fields_updated"]

    if fields_updated:
        assistant_message = "Updated interaction fields: " + ", ".join(fields_updated) + "."
    else:
        assistant_message = "No explicit interaction changes were identified from the message."

    return {
        "updated_interaction": merge_result["updated_interaction"],
        "fields_updated": fields_updated,
        "hcp_profile": None,
        "tool_message": assistant_message,
    }


def search_hcp_profile_tool(
    user_message: str, current_interaction: dict[str, Any]
) -> dict[str, Any]:
    hcp_name = extract_hcp_name(user_message)
    if hcp_name is None:
        return {
            "updated_interaction": dict(current_interaction),
            "fields_updated": [],
            "hcp_profile": None,
            "tool_message": "I could not identify an HCP name from that message.",
        }

    with SessionLocal() as db:
        repository = HCPRepository(db)
        profile = repository.search_by_name(hcp_name)

    if profile is None:
        return {
            "updated_interaction": dict(current_interaction),
            "fields_updated": [],
            "hcp_profile": None,
            "tool_message": f"I could not find a profile for {hcp_name}.",
        }

    profile_out = HCPProfileOut.model_validate(profile)
    updated_interaction = dict(current_interaction)
    updated_interaction.update(
        {
            "hcp_name": profile_out.name,
            "specialty": profile_out.specialty,
            "location": profile_out.location,
        }
    )

    return {
        "updated_interaction": updated_interaction,
        "fields_updated": ["hcp_name", "specialty", "location"],
        "hcp_profile": profile_out.model_dump(),
        "tool_message": f"Found HCP profile for {profile_out.name} ({profile_out.specialty}, {profile_out.location}).",
    }



def run_tool(tool_name: str, user_message: str, current_interaction: dict[str, Any]) -> dict[str, Any]:
    if tool_name == "search_hcp_profile":
        return search_hcp_profile_tool(user_message, current_interaction)

    if tool_name == "log_interaction":
        return log_interaction_tool(user_message, current_interaction)

    if tool_name == "edit_interaction":
        return edit_interaction_tool(user_message, current_interaction)

    if tool_name == "set_follow_up_action":
        return set_follow_up_action_tool(user_message, current_interaction)

    if tool_name == "check_compliance":
        return check_compliance_tool(user_message, current_interaction)

    updated_interaction = dict(current_interaction)
    fields_updated: list[str] = []
    tool_message = f"Tool selected: {tool_name}."

    return {
        "updated_interaction": updated_interaction,
        "fields_updated": fields_updated,
        "hcp_profile": None,
        "tool_message": tool_message,
    }
