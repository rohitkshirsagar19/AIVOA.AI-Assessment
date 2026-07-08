import { useMemo, useState } from 'react';
import { useSelector } from 'react-redux';

import { saveInteraction } from '../../api/interactions';
import type { RootState } from '../../app/store';

interface FieldConfig {
  key: string;
  label: string;
  multiline?: boolean;
  list?: boolean;
}

const fields: FieldConfig[] = [
  { key: 'hcp_name', label: 'HCP Name' },
  { key: 'specialty', label: 'Specialty' },
  { key: 'location', label: 'Location' },
  { key: 'interaction_date', label: 'Interaction Date' },
  { key: 'interaction_type', label: 'Interaction Type' },
  { key: 'product_discussed', label: 'Product Discussed' },
  { key: 'topics_discussed', label: 'Topics Discussed', list: true },
  { key: 'sentiment', label: 'Sentiment' },
  { key: 'materials_shared', label: 'Materials Shared', list: true },
  { key: 'samples_shared', label: 'Samples Shared', list: true },
  { key: 'key_outcomes', label: 'Key Outcomes', multiline: true },
  { key: 'follow_up_action', label: 'Follow-up Action', multiline: true },
  { key: 'follow_up_date', label: 'Follow-up Date' },
  { key: 'compliance_status', label: 'Compliance Status' },
  { key: 'compliance_issues', label: 'Compliance Issues', list: true },
  { key: 'compliance_suggestion', label: 'Compliance Suggestion', multiline: true },
];

const saveEligibilityKeys = [
  'interaction_date',
  'interaction_type',
  'product_discussed',
  'topics_discussed',
  'sentiment',
  'materials_shared',
  'samples_shared',
  'key_outcomes',
  'follow_up_action',
  'follow_up_date',
  'compliance_status',
  'compliance_issues',
  'compliance_suggestion',
] as const;

function formatValue(value: unknown, config: FieldConfig): string {
  if (Array.isArray(value)) {
    return value.length > 0 ? value.join(', ') : 'No value yet';
  }

  if (value === null || value === undefined || value === '') {
    return 'No value yet';
  }

  if (typeof value === 'string') {
    return value;
  }

  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value);
  }

  if (config.multiline || config.list) {
    return JSON.stringify(value);
  }

  return String(value);
}

function hasUsableValue(value: unknown): boolean {
  if (Array.isArray(value)) {
    return value.length > 0;
  }

  if (typeof value === 'string') {
    return value.trim().length > 0;
  }

  return value !== null && value !== undefined;
}

function canSaveInteraction(interaction: Record<string, unknown>): boolean {
  const hcpName = interaction.hcp_name;
  if (typeof hcpName !== 'string' || hcpName.trim().length === 0) {
    return false;
  }

  return saveEligibilityKeys.some((key) => hasUsableValue(interaction[key]));
}

export default function InteractionForm() {
  const interaction = useSelector((state: RootState) => state.interaction.data);
  const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const saveEnabled = useMemo(() => canSaveInteraction(interaction), [interaction]);

  const handleSave = async () => {
    if (!saveEnabled || saveState === 'saving') {
      return;
    }

    setSaveState('saving');
    setSaveMessage(null);

    try {
      const payload = await saveInteraction(interaction);
      setSaveState('saved');
      setSaveMessage(`${payload.message} Record #${payload.id}.`);
    } catch (caughtError) {
      const message = caughtError instanceof Error ? caughtError.message : 'Unknown save error';
      setSaveState('error');
      setSaveMessage(message);
    }
  };

  return (
    <div className="interaction-form-shell">
      <div className="form-section-header">
        <div>
          <p className="eyebrow">Current Interaction</p>
          <h2>Structured CRM record</h2>
        </div>
        <div className="form-actions">
          <span className="read-only-flag">Assistant controlled</span>
          <button
            type="button"
            className="save-button"
            onClick={handleSave}
            disabled={!saveEnabled || saveState === 'saving'}
          >
            {saveState === 'saving' ? 'Saving...' : 'Save interaction'}
          </button>
        </div>
      </div>

      <p className="save-helper">
        Save is enabled after the assistant fills an HCP and at least one meaningful interaction detail.
      </p>

      {saveMessage ? (
        <div className={saveState === 'error' ? 'save-banner save-banner-error' : 'save-banner save-banner-success'}>
          {saveMessage}
        </div>
      ) : null}

      <div className="interaction-form">
        {fields.map((field) => {
          const value = interaction[field.key];
          const displayValue = formatValue(value, field);
          const isEmpty = displayValue === 'No value yet';

          return (
            <label key={field.key} className="field-card" aria-label={field.label}>
              <span className="field-label">{field.label}</span>
              <div
                className={`field-value ${field.multiline ? 'field-value-multiline' : ''} ${
                  isEmpty ? 'field-value-empty' : ''
                }`}
                aria-readonly="true"
              >
                {displayValue}
              </div>
            </label>
          );
        })}
      </div>
    </div>
  );
}
