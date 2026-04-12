#project_contacts.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_contacts import ProjectContacts
from app.services.audit_log_service import write_audit_log

async def get_project_contacts(db: AsyncSession, project_id: int) -> ProjectContacts | None:
    result = await db.execute(
        select(ProjectContacts).where(ProjectContacts.project_id == project_id)
    )
    return result.scalar_one_or_none()

async def update_project_contacts(
    db: AsyncSession,
    project_id: int,
    new_contact_notes: str, #used to update the details
    account_id: int,
    user_id: int,
):

    project_contacts = await get_project_contacts(db, project_id) #project_access is the row from the table, ProjectAccess is the model/blueprint itself.
    if not project_contacts:
        raise ValueError("ProjectContacts not found")

    old = {"project_contacts": project_contacts.project_contact_notes} #this creates a snapshot of the old value before we overwrite it.

    now = datetime.now(timezone.utc) #this solidifies the correct 'now' timing. to be used by other code for synchronocity.

    project_contacts.project_contact_notes = new_contact_notes
    project_contacts.updated_at = now
    project_contacts.updated_by = user_id

    await write_audit_log(
        db=db,
        entity_type="project_contacts",
        entity_id=project_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={"old": old, "new": {"project_contact_notes": new_contact_notes}},
        performed_at=now,
    )

    await db.commit()
    await db.refresh(project_contacts)

    return project_contacts

