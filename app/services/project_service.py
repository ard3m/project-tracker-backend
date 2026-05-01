#project_service.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.services.audit_log_service import write_audit_log

	async def create_project(
	    db: AsyncSession,
        project_id: int,
        project_name: str,
        address: str,
        is_active: bool,
        account_id: int,
        user_id: int,
	):
	    now = datetime.now(timezone.utc)
	    row = project(
	        project_id=project_id,
	        project_name=project_name,
	        address=address,
            is_active=is_active,
            account_id=account_id,
            user_id=user_id,
	    )
	    db.add(row)
	    await db.commit()
	    await db.refresh(row)
	    await write_audit_log(
	        db=db,
	        entity_type="project",
	        entity_id=row.project_id,
	        account_id=account_id,
	        performed_by=user_id,
	        action="create",
	        details={
	            "old": None,
	            "new": {
	                "project_id": project_id,
	                "project_name": project_name,
	                "address": address,
                    "is_active": is_active,
                    "account_id": account_id,
                    "user_id": user_id,
	            },
	        },
	        performed_at=now,
	    )
	    return row


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    result = await db.execute(
        select(Project).where(Project.project_id == project_id)
    )
    return result.scalar_one_or_none()


async def update_project(
    db: AsyncSession,
    project_id: int,
    new_project_name: str,
    new_address: str,
    new_is_active: bool,
    account_id: int,
    user_id: int,
):

    project = await get_project(db, project_id)
    if not project:
        raise ValueError("Project not found")

    old = {
        "project_name": project.project_name,
        "address": project.address,
        "is_active": project.is_active,
    }

    now = datetime.now(timezone.utc)

    project.project_name = new_project_name
    project.address = new_address
    project.is_active = new_is_active
    project.updated_at = now
    project.updated_by = user_id

    await write_audit_log(
        db=db,
        entity_type="project",
        entity_id=project_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={
            "old": old,
            "new": {
                "project_name": new_project_name,
                "address": new_address,
                "is_active": new_is_active,
            },
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(project)

    return project


    	async def archive_project(
	    db: AsyncSession,
	    project_id: int,
	    account_id: int,
	    user_id: int,
	):
	    row = await get_project(db, project_id)
	    if not row:
	        raise ValueError("project not found")
	    old = {
	        "is_active": row.is_active,
	    }
	    now = datetime.now(timezone.utc)
	    row.is_active = False
	    row.updated_at = now
	    row.updated_by = user_id
	    await write_audit_log(
	        db=db,
	        entity_type="project",
	        entity_id=<project_id,
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


    	async def unarchive_project(
	    db: AsyncSession,
	    project_id: int,
	    account_id: int,
	    user_id: int,
	):
	    row = await get_project(db, project_id)
	    if not row:
	        raise ValueError("project not found")
	    old = {
	        "is_active": row.is_active,
	    }
	    now = datetime.now(timezone.utc)
	    row.is_active = True
	    row.updated_at = now
	    row.updated_by = user_id
	    await write_audit_log(
	        db=db,
	        entity_type="project",
	        entity_id=project_id,
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


async def list_projects(
    db: AsyncSession,
    account_id: int | None = None,
    filters: dict | None = None,
):
    query = select(Project)

    # Optional account scoping
    if account_id is not None:
        query = query.where(Project.account_id == account_id)

    # Optional dynamic filters
    if filters:
        for field, value in filters.items():
            query = query.where(getattr(Project, field) == value)

    result = await db.execute(query)
    return result.scalars().all()
