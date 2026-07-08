from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.hcp_repository import HCPRepository
from app.repositories.interaction_repository import InteractionRepository
from app.schemas.interaction import InteractionSaveRequest, InteractionSaveResponse


router = APIRouter(tags=["interactions"])


@router.post("/interactions", response_model=InteractionSaveResponse, status_code=status.HTTP_201_CREATED)
def save_interaction(request: InteractionSaveRequest, db: Session = Depends(get_db)) -> InteractionSaveResponse:
    interaction_repository = InteractionRepository(db)
    interaction = request.current_interaction

    if not interaction_repository.has_enough_data(interaction):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Interaction needs an HCP name and at least one meaningful detail before it can be saved.",
        )

    hcp_name = interaction.hcp_name
    if hcp_name is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Interaction needs an HCP name before it can be saved.",
        )

    hcp_repository = HCPRepository(db)
    hcp_profile = hcp_repository.search_by_name(hcp_name)
    if hcp_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No HCP profile found for {hcp_name}.",
        )

    saved_record = interaction_repository.create(hcp_profile=hcp_profile, interaction=interaction)
    return InteractionSaveResponse(
        id=saved_record.id,
        message=f"Interaction saved for {hcp_profile.name}.",
    )
