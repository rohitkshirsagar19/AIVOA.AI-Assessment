import InteractionForm from './features/interaction-form/InteractionForm';

const chatMessages = [
  'Show me Dr. Amit Mehta\'s profile before I log the meeting.',
  'I met Dr. Amit Mehta today in person and discussed CardioPlus efficacy.',
  'Set a follow-up for next Friday to send clinical study data.',
];

export default function App() {
  return (
    <main className="app-shell">
      <section className="panel panel-form">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Interaction Workspace</p>
            <h1>Log Interaction</h1>
          </div>
          <span className="status-pill">Read only</span>
        </div>

        <InteractionForm />
      </section>

      <section className="panel panel-chat">
        <div className="panel-header">
          <div>
            <p className="eyebrow">AI Assistant</p>
            <h1>Conversation Control</h1>
          </div>
          <span className="status-pill status-pill-accent">Groq + LangGraph</span>
        </div>

        <div className="chat-stack">
          {chatMessages.map((message, index) => (
            <article key={message} className={`chat-bubble ${index % 2 === 0 ? 'user' : 'assistant'}`}>
              <span className="bubble-label">{index % 2 === 0 ? 'User' : 'Assistant'}</span>
              <p>{message}</p>
            </article>
          ))}
        </div>

        <div className="composer">
          <span className="placeholder-line" />
          <button type="button">Send</button>
        </div>
      </section>
    </main>
  );
}
