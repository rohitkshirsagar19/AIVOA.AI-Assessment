import { useSelector } from 'react-redux';

import type { RootState } from '../app/store';

export default function ComplianceCard() {
  const interaction = useSelector((state: RootState) => state.interaction.data);
  const status = interaction.compliance_status;
  const issues = Array.isArray(interaction.compliance_issues) ? interaction.compliance_issues : [];
  const suggestion = interaction.compliance_suggestion;

  if (!status && issues.length === 0 && !suggestion) {
    return null;
  }

  return (
    <section className="insight-card compliance-card">
      <div className="insight-header">
        <p className="eyebrow">Compliance</p>
        <h2>{typeof status === 'string' ? status : 'No review yet'}</h2>
      </div>

      {issues.length > 0 ? (
        <div>
          <span className="summary-label">Issues</span>
          <ul className="issue-list">
            {issues.map((issue) => (
              <li key={String(issue)}>{String(issue)}</li>
            ))}
          </ul>
        </div>
      ) : null}

      {typeof suggestion === 'string' && suggestion.trim() ? (
        <div className="profile-summary">
          <span className="summary-label">Suggestion</span>
          <p>{suggestion}</p>
        </div>
      ) : null}
    </section>
  );
}
