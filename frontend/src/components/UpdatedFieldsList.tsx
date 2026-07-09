interface UpdatedFieldsListProps {
  fieldsUpdated: string[];
}

export default function UpdatedFieldsList({ fieldsUpdated }: UpdatedFieldsListProps) {
  if (fieldsUpdated.length === 0) {
    return null;
  }

  return (
    <section className="updated-fields-card">
      <div className="updated-fields-header">
        <p className="eyebrow">Updated Fields</p>
        <h2>Backend-applied changes</h2>
      </div>
      <ul className="chip-list">
        {fieldsUpdated.map((field) => (
          <li key={field} className="chip-item">
            {field}
          </li>
        ))}
      </ul>
    </section>
  );
}
