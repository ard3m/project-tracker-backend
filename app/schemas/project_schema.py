#project_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    account_id: int
    project_name: str
    is_active: Optional[bool] = True
    address: Optional[str] = None
    updated_by: int


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    is_active: Optional[bool] = None
    address: Optional[str] = None
    updated_by: Optional[int] = None


class ProjectResponse(BaseModel):
    project_id: int
    account_id: int
    project_name: str
    is_active: bool
    address: Optional[str]
    updated_at: datetime
    updated_by: int

    class Config:
        from_attributes = True