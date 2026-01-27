from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class HistoryEventOut(BaseModel):
    history_event_id: int #changed from 'id'
    event_type: str
    description: str
    timestamp: datetime
