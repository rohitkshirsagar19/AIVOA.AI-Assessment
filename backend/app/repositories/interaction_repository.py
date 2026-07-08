from sqlalchemy.orm import Session

from app.models.interaction import Interaction
from app.models.hcp_profile import HCPProfile
from app.schemas.interaction import InteractionRecord


class InteractionRepository:
    def __init__(self, db: Session):
        self.db = db

    def has_enough_data(self, interaction: InteractionRecord) -> bool:
        if not interaction.hcp_name:
            return False

        meaningful_fields = [
            interaction.interaction_date,
            interaction.interaction_type,
            interaction.product_discussed,
            interaction.sentiment,
            interaction.key_outcomes,
            interaction.follow_up_action,
            interaction.follow_up_date,
            interaction.compliance_status,
            interaction.compliance_suggestion,
        ]

        if any(value not in (None, "") for value in meaningful_fields):
            return True

        return any(
            [
                len(interaction.topics_discussed) > 0,
                len(interaction.materials_shared) > 0,
                len(interaction.samples_shared) > 0,
                len(interaction.compliance_issues) > 0,
            ]
        )

    def create(self, *, hcp_profile: HCPProfile, interaction: InteractionRecord) -> Interaction:
        summary = interaction.key_outcomes or self._build_summary(interaction)
        record = Interaction(
            hcp_profile_id=hcp_profile.id,
            specialty=interaction.specialty or hcp_profile.specialty,
            location=interaction.location or hcp_profile.location,
            interaction_date=interaction.interaction_date,
            interaction_type=interaction.interaction_type,
            product_discussed=interaction.product_discussed,
            topics_discussed=interaction.topics_discussed,
            sentiment=interaction.sentiment,
            materials_shared=interaction.materials_shared,
            samples_shared=interaction.samples_shared,
            key_outcomes=interaction.key_outcomes,
            follow_up_action=interaction.follow_up_action,
            follow_up_date=interaction.follow_up_date,
            compliance_status=interaction.compliance_status,
            compliance_issues=interaction.compliance_issues,
            compliance_suggestion=interaction.compliance_suggestion,
            summary=summary,
        )
        self.db.add(record)

        if summary:
            hcp_profile.last_interaction_summary = summary

        self.db.commit()
        self.db.refresh(record)
        return record

    def _build_summary(self, interaction: InteractionRecord) -> str | None:
        parts: list[str] = []

        if interaction.product_discussed:
            parts.append(f"Product: {interaction.product_discussed}")
        if interaction.sentiment:
            parts.append(f"Sentiment: {interaction.sentiment}")
        if interaction.topics_discussed:
            parts.append("Topics: " + ", ".join(interaction.topics_discussed))

        if not parts:
            return None

        return " | ".join(parts)
