import ChatPanel from './features/chat/ChatPanel';
import InteractionForm from './features/interaction-form/InteractionForm';

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

      <ChatPanel />
    </main>
  );
}
