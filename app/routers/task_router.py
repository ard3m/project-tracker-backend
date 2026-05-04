#task_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)
from app.services.task_service import (
    create_task,
    get_task,
    update_task,
    archive_task,
    unarchive_task,
    list_tasks,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task_endpoint(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await create_task(
        db=db,
        project_id=payload.project_id,
        task_name=payload.task_name,
        task_description=payload.task_description,
        is_active=True,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return row


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_task(db, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return row


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_task(db, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    updated = await update_task(
        db=db,
        task_id=task_id,
        new_task_name=payload.task_name,
        new_task_description=payload.task_description,
        new_is_active=payload.is_active,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return updated


@router.post("/{task_id}/archive", response_model=TaskResponse)
async def archive_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_task(db, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    archived = await archive_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return archived


@router.post("/{task_id}/unarchive", response_model=TaskResponse)
async def unarchive_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_task(db, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    unarchived = await unarchive_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return unarchived


@router.get("/", response_model=list[TaskResponse])
async def list_tasks_endpoint(
    project_id: int | None = None,
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    filters = {}

    if project_id is not None:
        filters["project_id"] = project_id
    if is_active is not None:
        filters["is_active"] = is_active

    rows = await list_tasks(db, filters=filters)
    return rows