#materials_equipment_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MaterialsEquipmentCreate(BaseModel):
    project_id: int
    materials_equipment_details: str
    updated_by: int


class MaterialsEquipmentUpdate(BaseModel):
    materials_equipment_details: Optional[str] = None
    updated_by: Optional[int] = None


class MaterialsEquipmentResponse(BaseModel):
    project_id: int
    materials_equipment_details: str
    updated_at: datetime
    updated_by: int

    class Config:
        from_attributes = True