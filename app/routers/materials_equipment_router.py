#materials_equipment_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.materials_equipment_schema import (
    MaterialsEquipmentUpdate,
    MaterialsEquipmentResponse,
)
from app.services.materials_equipment_service import (
    get_materials_equipment,
    update_materials_equipment,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/materials_equipment", tags=["Materials & Equipment"])


@router.get("/{project_id}", response_model=MaterialsEquipmentResponse)
async def get_materials_equipment_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_materials_equipment(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="MaterialsEquipment not found")
    return row


@router.put("/{project_id}", response_model=MaterialsEquipmentResponse)
async def update_materials_equipment_endpoint(
    project_id: int,
    payload: MaterialsEquipmentUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_materials_equipment(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="MaterialsEquipment not found")

    updated = await update_materials_equipment(
        db=db,
        project_id=project_id,
        new_materials_equipment_details=payload.materials_equipment_details,
        account_id=account.account_id,
        user_id=user.user_id,
    )
    return updated