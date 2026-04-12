#materials_equipement.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.materials_equipment import MaterialsEquipment
from app.services.audit_log_service import write_audit_log

async def get_materials_equipment(db: AsyncSession, project_id: int) -> MaterialsEquipment | None:
    result = await db.execute(
        select(MaterialsEquipment).where(MaterialsEquipment.project_id == project_id)
    )
    return result.scalar_one_or_none()

async def update_materials_equipment(
    db: AsyncSession,
    project_id: int,
    new_materials_equipment_details: str, #used to update the details
    account_id: int,
    user_id: int,
):

    materials_equipment = await get_materials_equipment(db, project_id) #project_access is the row from the table, ProjectAccess is the model/blueprint itself.
    if not materials_equipment:
        raise ValueError("MaterialsEquipment not found")

    old = {"materials_equipment_details": materials_equipment.materials_equipment_details} #this creates a snapshot of the old value before we overwrite it.

    now = datetime.now(timezone.utc) #this solidifies the correct 'now' timing. to be used by other code for synchronocity.

    materials_equipment.materials_equipment_details = new_materials_equipment_details
    materials_equipment.updated_at = now
    materials_equipment.updated_by = user_id

    await write_audit_log(
        db=db,
        entity_type="materials_equipment",
        entity_id=project_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={"old": old, "new": {"materials_equipment_details": new_materials_equipment_details}},
        performed_at=now,
    )

    await db.commit()
    await db.refresh(materials_equipment)

    return materials_equipment