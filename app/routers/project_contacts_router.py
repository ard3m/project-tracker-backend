#project_contacts_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.project_contacts_schema import (
    ProjectContactsUpdate,
    ProjectContactsResponse,
)
from app.services.project_contacts_service import (
    get_project_contacts,
    update_project_contacts,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/project_contacts", tags=["Project Contacts"])


@router.get("/{project_id}", response_model=ProjectContactsResponse)
async def get_project_contacts_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_project_contacts(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="ProjectContacts not found")
    return row


@router.put("/{project_id}", response_model=ProjectContactsResponse)
async def update_project_contacts_endpoint(
    project_id: int,
    payload: ProjectContactsUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_project_contacts(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="ProjectContacts not found")

    updated = await update_project_contacts(
        db=db,
        project_id=project_id,
        new_project_contact_notes=payload.project_contact_notes,
        account_id=account.account_id,
        user_id=user.user_id,
    )
    return updated