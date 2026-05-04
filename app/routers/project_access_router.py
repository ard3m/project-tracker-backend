#project_access_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.project_access_schema import (
    ProjectAccessUpdate,
    ProjectAccessResponse,
)
from app.services.project_access_service import (
    get_project_access,
    update_project_access,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/project_access", tags=["Project Access"])


@router.get("/{project_id}", response_model=ProjectAccessResponse)
async def get_project_access_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_project_access(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="ProjectAccess not found")
    return row


@router.put("/{project_id}", response_model=ProjectAccessResponse)
async def update_project_access_endpoint(
    project_id: int,
    payload: ProjectAccessUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_project_access(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="ProjectAccess not found")

    updated = await update_project_access(
        db=db,
        project_id=project_id,
        new_details=payload.access_details,
        account_id=account.account_id,
        user_id=user.user_id,
    )
    return updated