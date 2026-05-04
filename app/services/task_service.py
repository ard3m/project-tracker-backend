#task_service.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.services.audit_log_service import write_audit_log

async def create_task(
    db: AsyncSession,
    task_id: int,
    task_name: str,
    task_description: str,
    is_active: bool,
    updated_at: int,
    updated_by: int,
    account_id: int, #this is only for audit log functionality
    user_id: int,
):
    now = datetime.now(timezone.utc)
    row = task(
        task_id=task_id,
        task_name=task_name,
        task_description=task_description,   # optional
        is_active=is_active,
        updated_at=now,      # only if your model has it
        updated_by=user_id,  # only if your model has it
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    await write_audit_log(
        db=db,
        entity_type="task",
        entity_id=row.task_id,
        account_id=account_id,
        performed_by=user_id,
        action="create",
        details={
            "old": None,
            "new": {
                "task_id": task_id,
                "task_name": task_name,
                "task_description": task_description,
                "is_active": is_active,
                "updated_at": updated_at,
                "updated_by": updated_by,
            },
        },
        performed_at=now,
    )
    return row


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.task_id == task_id)
    )
    return result.scalar_one_or_none()

async def update_task(
    db: AsyncSession,
    task_id: int,
    new_task_name: str,
    new_task_description: str,
    new_is_active: bool,
    updated_at: int,
    updated_by: int,
    account_id: int,
    user_id: int,
):

    task = await get_task(db, task_id)
    if not task:
        raise ValueError("Task not found")

    old = {
        "task_name": task.task_name,
        "task_description": task.task_description,
        "is_active": task.is_active,
    }

    now = datetime.now(timezone.utc)

    task.task_name = new_task_name
    task.task_description = new_task_description
    task.is_active = new_is_active
    task.updated_at = now
    task.updated_by = user_id

    await write_audit_log(
        db=db,
        entity_type="task",
        entity_id=task_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={"old": old, "new": {"task_name": new_task_name,"task_description": new_task_description,"is_active": new_is_active,}},
        performed_at=now,
    )

    await db.commit()
    await db.refresh(task)

    return task


async def archive_task(
    db: AsyncSession,
    task_id: int,
    account_id: int,
    user_id: int,
):
    row = await get_task(db, task_id)
    if not row:
        raise ValueError("task not found")
    old = {
        "is_active": row.is_active,
    }
    now = datetime.now(timezone.utc)
    row.is_active = False
    row.updated_at = now
    row.updated_by = user_id
    await write_audit_log(
        db=db,
        entity_type="task",
        entity_id=task_id,
        account_id=account_id,
        performed_by=user_id,
        action="archive",
        details={
            "old": old,
            "new": {"is_active": False},
        },
        performed_at=now,
    )
    await db.commit()
    await db.refresh(row)
    return row


    async def unarchive_task(
    db: AsyncSession,
    task_id: int,
    account_id: int,
    user_id: int,
):
    row = await get_task(db, task_id)
    if not row:
        raise ValueError("task not found")
    old = {
        "is_active": row.is_active,
    }
    now = datetime.now(timezone.utc)
    row.is_active = True
    row.updated_at = now
    row.updated_by = user_id
    await write_audit_log(
        db=db,
        entity_type="task",
        entity_id=task_id,
        account_id=account_id,
        performed_by=user_id,
        action="unarchive",
        details={
            "old": old,
            "new": {"is_active": True},
        },
        performed_at=now,
    )
    await db.commit()
    await db.refresh(row)
    return row

	async def list_tasks(
	    db: AsyncSession,
	    project_id: int | None = None,
	    filters: dict | None = None,
	):
	    query = select(Task)
	    # Optional account scoping
	    if project_id is not None:
	        query = query.where(Task.project_id == project_id)
	    # Optional dynamic filters
	    if filters:
	        for field, value in filters.items():
	            query = query.where(getattr(Task, field) == value)
	    result = await db.execute(query)
	    return result.scalars().all()
