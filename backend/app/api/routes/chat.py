from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent_service import run_chat_agent


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = run_chat_agent(
        session_id=request.session_id,
        message=request.message,
        current_interaction=request.current_interaction,
    )

    tool_calls = []
    if result.get("tool_decision") is not None:
        tool_calls.append(result["tool_decision"])

    updated_fields = {
        field_name: result["updated_interaction"][field_name]
        for field_name in result.get("fields_updated", [])
        if field_name in result["updated_interaction"]
    }

    return ChatResponse(
        message=result["assistant_message"],
        tool_calls=tool_calls,
        updated_fields=updated_fields,
        fields_updated=result.get("fields_updated", []),
        hcp_profile=result.get("hcp_profile"),
        warnings=[],
    )
