import { useSelector } from 'react-redux';

import type { RootState } from '../app/store';

export default function HCPProfileCard() {
  const profile = useSelector((state: RootState) => state.hcp.profile);

  if (!profile) {
    return null;
  }

  return (
    <section className="insight-card">
      <div className="insight-header">
        <p className="eyebrow">HCP Profile</p>
        <h2>{profile.name ?? 'Selected HCP'}</h2>
      </div>
      <dl className="detail-grid">
        <div>
          <dt>Specialty</dt>
          <dd>{profile.specialty ?? 'Not available'}</dd>
        </div>
        <div>
          <dt>Location</dt>
          <dd>{profile.location ?? 'Not available'}</dd>
        </div>
        <div>
          <dt>Affiliation</dt>
          <dd>{profile.affiliation ?? 'Not available'}</dd>
        </div>
        <div>
          <dt>Preferred Channel</dt>
          <dd>{profile.preferred_channel ?? 'Not available'}</dd>
        </div>
      </dl>
      {profile.last_interaction_summary ? (
        <div className="profile-summary">
          <span className="summary-label">Last interaction</span>
          <p>{profile.last_interaction_summary}</p>
        </div>
      ) : null}
    </section>
  );
}
