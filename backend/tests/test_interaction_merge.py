from datetime import date

from app.schemas.interaction import InteractionPatch
from app.services.interaction_merge import merge_interaction_patch



def test_merge_keeps_existing_values_when_patch_contains_nulls() -> None:
    current_interaction = {
        "hcp_name": "Dr. Amit Mehta",
        "sentiment": "positive",
        "key_outcomes": "Shared brochure.",
    }
    patch = InteractionPatch(hcp_name=None, sentiment=None, key_outcomes=None)

    result = merge_interaction_patch(current_interaction, patch)

    assert result["updated_interaction"] == current_interaction
    assert result["fields_updated"] == []



def test_merge_deduplicates_arrays_and_tracks_updated_fields() -> None:
    current_interaction = {
        "topics_discussed": ["efficacy", "pricing"],
        "materials_shared": ["brochure"],
    }
    patch = InteractionPatch(
        topics_discussed=["pricing", "patient adherence"],
        materials_shared=["brochure", "clinical study"],
    )

    result = merge_interaction_patch(current_interaction, patch)

    assert result["updated_interaction"]["topics_discussed"] == [
        "efficacy",
        "pricing",
        "patient adherence",
    ]
    assert result["updated_interaction"]["materials_shared"] == [
        "brochure",
        "clinical study",
    ]
    assert result["fields_updated"] == ["topics_discussed", "materials_shared"]



def test_merge_updates_scalars_and_preserves_omitted_arrays() -> None:
    current_interaction = {
        "hcp_name": "Dr. Amit Mehta",
        "interaction_date": date(2026, 7, 9),
        "sentiment": "positive",
        "topics_discussed": ["efficacy"],
    }
    patch = InteractionPatch(
        sentiment="neutral",
        key_outcomes="HCP had concerns about pricing.",
    )

    result = merge_interaction_patch(current_interaction, patch)

    assert result["updated_interaction"] == {
        "hcp_name": "Dr. Amit Mehta",
        "interaction_date": date(2026, 7, 9),
        "sentiment": "neutral",
        "topics_discussed": ["efficacy"],
        "key_outcomes": "HCP had concerns about pricing.",
    }
    assert result["fields_updated"] == ["sentiment", "key_outcomes"]



def test_merge_adds_array_field_when_current_value_is_missing() -> None:
    current_interaction = {"hcp_name": "Dr. Neha Sharma"}
    patch = InteractionPatch(materials_shared=["product brochure"])

    result = merge_interaction_patch(current_interaction, patch)

    assert result["updated_interaction"]["materials_shared"] == ["product brochure"]
    assert result["fields_updated"] == ["materials_shared"]
