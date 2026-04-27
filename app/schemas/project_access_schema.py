#project_access_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectAccessCreate(BaseModel):
    project_id: int
    access_details: str
    updated_by: int


class ProjectAccessUpdate(BaseModel):
    access_details: Optional[str] = None
    updated_by: Optional[int] = None


class ProjectAccessResponse(BaseModel):
    project_id: int
    access_details: str
    updated_at: datetime
    updated_by: int

    class Config:
        from_attributes = True