#task_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    project_id: int
    task_name: str
    task_description: Optional[str] = None
    is_active: Optional[bool] = True

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    is_active: Optional[bool] = None


class TaskResponse(BaseModel):
    task_id: int
    project_id: int
    task_name: str
    task_description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config: #whats this all about?
        from_attributes = True