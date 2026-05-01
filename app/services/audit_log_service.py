from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_log import AuditLog


async def write_audit_log(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
    account_id: int,
    performed_by: int,
    action: str,
    details: dict | None,
    performed_at: datetime | None = None,
):
    """
    Universal audit log writer.
    All service-layer write operations call this function.
    """

    if performed_at is None:
        performed_at = datetime.now(timezone.utc)

    log_entry = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        account_id=account_id,
        performed_by=performed_by,
        action=action,
        details=details,
        performed_at=performed_at,
    )

    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)

    return log_entry


async def list_audit_log( #THIS WAS 'LOGS' PLURAL - give a look. should be one singular and one plural.
    db: AsyncSession,
    entity_type: str | None = None,
    entity_id: int | None = None,
    account_id: int | None = None,
):
    """
    this one is meant to be singular - while there is also a  'list_audit_logs' - plural.
    """

    query = select(AuditLog)

    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)

    if entity_id:
        query = query.where(AuditLog.entity_id == entity_id)

    if account_id:
        query = query.where(AuditLog.account_id == account_id)

    result = await db.execute(query)
    return result.scalars().all()

async def list_audit_logs(
    db: AsyncSession,
    account_id: int | None = None,
    filters: dict | None = None,
):
    query = select(AuditLog)

    # Optional account scoping
    if account_id is not None:
        query = query.where(AuditLog.account_id == account_id)

    # Optional dynamic filters
    if filters:
        for field, value in filters.items():
            query = query.where(getattr(AuditLog, field) == value)

    result = await db.execute(query)
    return result.scalars().all()