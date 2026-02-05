from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TaskCreate(BaseModel):
    name: str
    task_id: int

class TaskOut(BaseModel):
    name: str
    task_id: int
    created_at: datetime