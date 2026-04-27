#project_contacts_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectContactsCreate(BaseModel):
    project_id: int
    project_contacts_notes: str
    updated_by: int


class ProjectContactsUpdate(BaseModel):
    project_contacts_notes: Optional[str] = None
    updated_by: Optional[int] = None


class ProjectContactsResponse(BaseModel):
    project_id: int
    project_contacts_notes: str
    updated_at: datetime
    updated_by: int

    class Config:
        from_attributes = True