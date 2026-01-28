from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    project_id: int
    name: str
    created_at: datetime

class TaskCreate(BaseModel):
    project_id: int
    title: str
    status: str = "Pending"

class TaskOut(BaseModel):
    task_id: int
    project_id: int
    title: str
    status: str
    updated_at: datetime

class HistoryEventOut(BaseModel):
    history_event_id: int
    event_type: str
    description: str
    timestamp: datetime
