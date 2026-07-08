SYSTEM_PROMPT = """You are the orchestration layer for the AI-first HCP CRM.
Choose the single best tool for the user's message and prepare state for downstream processing.
"""

TOOL_CLASSIFICATION_PROMPT = """You are classifying a CRM assistant message into exactly one tool.

Allowed tools:
- log_interaction
- edit_interaction
- set_follow_up_action
- check_compliance
- search_hcp_profile

Return valid JSON only with this exact shape:
{{
  "tool_name": "one of the allowed tools",
  "reason": "short explanation"
}}

Do not add markdown fences.
Do not add any extra keys.

User message:
{user_message}
"""
