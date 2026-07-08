from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.hcp_repository import HCPRepository
from app.schemas.hcp import HCPProfileRead


router = APIRouter(prefix="/hcps", tags=["hcps"])


@router.get("", response_model=list[HCPProfileRead])
def list_hcps(db: Session = Depends(get_db)) -> list[HCPProfileRead]:
    repository = HCPRepository(db)
    return repository.list_profiles()
