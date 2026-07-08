from datetime import date

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
  \"tool_name\": \"one of the allowed tools\",
  \"reason\": \"short explanation\"
}}

Do not add markdown fences.
Do not add any extra keys.

User message:
{user_message}
"""

HCP_NAME_EXTRACTION_PROMPT = """Extract the doctor or HCP name from the user message.
Return valid JSON only with this exact shape:
{{
  \"hcp_name\": \"full name or empty string if unknown\"
}}

User message:
{user_message}
"""

LOG_INTERACTION_EXTRACTION_PROMPT = f"""Extract structured CRM interaction fields from the user's message.
Today is {date.today().isoformat()}.

Return valid JSON only.
Use this exact shape and do not add extra keys:
{{
  \"hcp_name\": \"string or null\",
  \"interaction_date\": \"YYYY-MM-DD or null\",
  \"interaction_type\": \"string or null\",
  \"product_discussed\": \"string or null\",
  \"topics_discussed\": [\"string\"],
  \"sentiment\": \"string or null\",
  \"materials_shared\": [\"string\"],
  \"key_outcomes\": \"string or null\"
}}

Rules:
- Only include values supported by the user message.
- Do not invent unknown values.
- If a field is unknown, use null for scalars and [] for arrays.
- Resolve relative dates like today using today's date above.
- Return JSON only, with no markdown fences.

User message:
{{user_message}}
"""

EDIT_INTERACTION_EXTRACTION_PROMPT = """You are updating an existing CRM interaction.
You must only extract fields the user explicitly wants to change.
Do not re-extract the whole interaction.
Do not modify unrelated fields.
Do not set fields to null unless the user clearly asks to remove a value.

Current interaction:
{current_interaction}

Return valid JSON only.
Use this exact shape and do not add extra keys:
{{
  \"hcp_name\": \"string or null\",
  \"interaction_date\": \"YYYY-MM-DD or null\",
  \"interaction_type\": \"string or null\",
  \"product_discussed\": \"string or null\",
  \"topics_discussed\": [\"string\"],
  \"sentiment\": \"string or null\",
  \"materials_shared\": [\"string\"],
  \"key_outcomes\": \"string or null\"
}}

Rules:
- Only include fields the user explicitly changes.
- Leave unmentioned fields absent from the effective update.
- Use null only when the user clearly removes a field.
- Return JSON only, with no markdown fences.

User message:
{user_message}
"""
