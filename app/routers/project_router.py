#project_router
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


router = APIRouter(prefix="/projects", tags=["Projects"])


# CREATE
@router.post("/", response_model=ProjectResponse)
async def create_project_endpoint(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await create_project(
        db=db,
        user_id=user.user_id,
        account_id=account.account_id,
        **payload.dict(),
    )
    return row


# GET (single)
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_project(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return row


# LIST
@router.get("/", response_model=list[ProjectResponse])
async def list_projects_endpoint(
    filters: dict | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    rows = await list_projects(db, filters=filters)
    return rows


# UPDATE
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project_endpoint(
    project_id: int,
    payload: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await update_project(
        db=db,
        project_id=project_id,
        user_id=user.user_id,
        account_id=account.account_id,
        **payload.dict(),
    )
    return row


# ARCHIVE
@router.post("/{project_id}/archive", response_model=ProjectResponse)
async def archive_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await archive_project(
        db=db,
        project_id=project_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return row


# UNARCHIVE
@router.post("/{project_id}/unarchive", response_model=<ProjectResponse)
async def unarchive_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await unarchive_project(
        db=db,
        project_id=project_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return row