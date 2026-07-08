from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.schemas.interaction import InteractionPatch


def merge_interaction_patch(
    current_interaction: Mapping[str, Any], patch: InteractionPatch
) -> dict[str, Any]:
    patch_data = patch.model_dump(exclude_unset=True)
    updated_interaction = dict(current_interaction)
    fields_updated: list[str] = []

    for field_name, incoming_value in patch_data.items():
        if incoming_value is None:
            continue

        current_value = updated_interaction.get(field_name)

        if isinstance(incoming_value, list):
            merged_value = _merge_unique_list(current_value, incoming_value)
            if merged_value != current_value:
                updated_interaction[field_name] = merged_value
                fields_updated.append(field_name)
            continue

        if current_value != incoming_value:
            updated_interaction[field_name] = incoming_value
            fields_updated.append(field_name)

    return {
        "updated_interaction": updated_interaction,
        "fields_updated": fields_updated,
    }


def _merge_unique_list(current_value: Any, incoming_value: Sequence[Any]) -> list[Any]:
    existing_items = list(current_value) if isinstance(current_value, list) else []
    merged_items = list(existing_items)

    for item in incoming_value:
        if item not in merged_items:
            merged_items.append(item)

    return merged_items
