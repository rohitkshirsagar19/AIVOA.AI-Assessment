import { useSelector } from 'react-redux';

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

export default function InteractionForm() {
  const interaction = useSelector((state: RootState) => state.interaction.data);

  return (
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
  );
}
