#routerTEMPLATE

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from app.services.project_service import (
    create_project,
    get_project,
    update_project,
    archive_project,
    unarchive_project,
    list_projects,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/<entity_plural>", tags=["<EntityPlural>"])


# CREATE
@router.post("/", response_model=<Entity>Response)
async def create_<entity>_endpoint(
    payload: <Entity>Create,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await create_<entity>(
        db=db,
        user_id=user.user_id,
        account_id=account.account_id,
        **payload.dict(),
    )
    return row


# GET (single)
@router.get("/{<entity>_id}", response_model=<Entity>Response)
async def get_<entity>_endpoint(
    <entity>_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_<entity>(db, <entity>_id)
    if not row:
        raise HTTPException(status_code=404, detail="<Entity> not found")
    return row


# LIST
@router.get("/", response_model=list[<Entity>Response])
async def list_<entity_plural>_endpoint(
    filters: dict | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    rows = await list_<entity_plural>(db, filters=filters)
    return rows


# UPDATE
@router.put("/{<entity>_id}", response_model=<Entity>Response)
async def update_<entity>_endpoint(
    <entity>_id: int,
    payload: <Entity>Update,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await update_<entity>(
        db=db,
        <entity>_id=<entity>_id,
        user_id=user.user_id,
        account_id=account.account_id,
        **payload.dict(),
    )
    return row


# ARCHIVE
@router.post("/{<entity>_id}/archive", response_model=<Entity>Response)
async def archive_<entity>_endpoint(
    <entity>_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await archive_<entity>(
        db=db,
        <entity>_id=<entity>_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return row


# UNARCHIVE
@router.post("/{<entity>_id}/unarchive", response_model=<Entity>Response)
async def unarchive_<entity>_endpoint(
    <entity>_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await unarchive_<entity>(
        db=db,
        <entity>_id=<entity>_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return row