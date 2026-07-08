export interface SaveInteractionResponse {
  id: number;
  message: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim() ?? 'http://127.0.0.1:8000';

export async function saveInteraction(currentInteraction: Record<string, unknown>): Promise<SaveInteractionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/interactions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      current_interaction: currentInteraction,
    }),
  });

  if (!response.ok) {
    let detail = `Save request failed with status ${response.status}`;

    try {
      const payload = (await response.json()) as { detail?: string };
      if (typeof payload.detail === 'string' && payload.detail.trim().length > 0) {
        detail = payload.detail;
      }
    } catch {
      // Ignore JSON parsing errors and fall back to the HTTP status message.
    }

    throw new Error(detail);
  }

  return (await response.json()) as SaveInteractionResponse;
}
