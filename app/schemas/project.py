from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    project_id: int
    name: str
    created_at: datetime






