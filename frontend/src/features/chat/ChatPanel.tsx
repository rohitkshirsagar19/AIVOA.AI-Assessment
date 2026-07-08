import { FormEvent, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../app/store';
import { sendChatMessage } from '../../api/chat';
import { addAssistantMessage, addUserMessage } from '../../store/chatSlice';
import { setHcpProfile } from '../../store/hcpSlice';
import { patchInteraction } from '../../store/interactionSlice';
import { setError, setLastToolUsed, setLoading } from '../../store/uiSlice';

export default function ChatPanel() {
  const dispatch = useDispatch<AppDispatch>();
  const messages = useSelector((state: RootState) => state.chat.messages);
  const currentInteraction = useSelector((state: RootState) => state.interaction.data);
  const loading = useSelector((state: RootState) => state.ui.loading);
  const error = useSelector((state: RootState) => state.ui.error);
  const lastToolUsed = useSelector((state: RootState) => state.ui.lastToolUsed);
  const [input, setInput] = useState('');

  const sessionId = useMemo(() => 'demo-session-1', []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    dispatch(addUserMessage(message));
    dispatch(setLoading(true));
    dispatch(setError(null));
    setInput('');

    try {
      const payload = await sendChatMessage(message, currentInteraction, sessionId);

      dispatch(patchInteraction(payload.updated_fields));
      dispatch(setHcpProfile(payload.hcp_profile));
      dispatch(setLastToolUsed(payload.tool_calls[0]?.tool_name ?? null));
      dispatch(addAssistantMessage(payload.message));

      if (payload.warnings.length > 0) {
        dispatch(setError(payload.warnings.join(' ')));
      }
    } catch (caughtError) {
      const messageText = caughtError instanceof Error ? caughtError.message : 'Unknown chat error';
      dispatch(setError(messageText));
      dispatch(addAssistantMessage('The assistant could not process that request.'));
      dispatch(setLastToolUsed(null));
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <section className="panel panel-chat">
      <div className="panel-header">
        <div>
          <p className="eyebrow">AI Assistant</p>
          <h1>Conversation Control</h1>
        </div>
        <span className="status-pill status-pill-accent">Groq + LangGraph</span>
      </div>

      {lastToolUsed ? <div className="tool-banner">Last tool used: {lastToolUsed}</div> : null}
      {error ? <div className="error-banner">{error}</div> : null}

      <div className="chat-stack">
        {messages.length === 0 ? (
          <article className="chat-bubble assistant">
            <span className="bubble-label">Assistant</span>
            <p>Ask the assistant to search an HCP, log an interaction, edit a field, set a follow-up, or run a compliance check.</p>
          </article>
        ) : (
          messages.map((chatMessage) => (
            <article
              key={chatMessage.id}
              className={`chat-bubble ${chatMessage.role === 'user' ? 'user' : 'assistant'}`}
            >
              <span className="bubble-label">{chatMessage.role === 'user' ? 'User' : 'Assistant'}</span>
              <p>{chatMessage.content}</p>
            </article>
          ))
        )}

        {loading ? (
          <article className="chat-bubble assistant loading-bubble">
            <span className="bubble-label">Assistant</span>
            <p>Thinking...</p>
          </article>
        ) : null}
      </div>

      <form className="composer" onSubmit={handleSubmit}>
        <input
          className="composer-input"
          type="text"
          placeholder="Describe the interaction or ask the assistant what to do next"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading || input.trim().length === 0}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </section>
  );
}
