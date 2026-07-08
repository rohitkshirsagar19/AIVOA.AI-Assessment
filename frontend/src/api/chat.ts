export interface SendChatMessageRequest {
  sessionId: string;
  message: string;
  currentInteraction: Record<string, unknown>;
}

export interface ChatResponse {
  message: string;
  tool_calls: Array<{
    tool_name: string;
    rationale: string;
  }>;
  updated_fields: Record<string, unknown>;
  fields_updated: string[];
  warnings: string[];
  hcp_profile: Record<string, unknown> | null;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim() ?? 'http://127.0.0.1:8000';

export async function sendChatMessage(
  message: string,
  currentInteraction: Record<string, unknown>,
  sessionId = 'demo-session-1',
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
      current_interaction: currentInteraction,
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`);
  }

  return (await response.json()) as ChatResponse;
}
