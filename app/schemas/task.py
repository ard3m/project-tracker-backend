from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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