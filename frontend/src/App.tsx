import ComplianceCard from './components/ComplianceCard';
import HCPProfileCard from './components/HCPProfileCard';
import ChatPanel from './features/chat/ChatPanel';
import InteractionForm from './features/interaction-form/InteractionForm';

export default function App() {
  return (
    <main className="app-shell">
      <section className="panel panel-form">
        <div className="panel-header panel-header-form">
          <div>
            <p className="eyebrow">Interaction Workspace</p>
            <h1>Log Interaction</h1>
            <p className="panel-subtitle">
              The form is populated only from validated assistant actions. Manual editing is disabled.
            </p>
          </div>
          <span className="status-pill">Read only</span>
        </div>

        <div className="panel-insights">
          <HCPProfileCard />
          <ComplianceCard />
        </div>

        <InteractionForm />
      </section>

      <ChatPanel />
    </main>
  );
}
