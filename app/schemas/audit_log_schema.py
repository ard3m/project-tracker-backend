#audit_log_schema

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class AuditLogCreate(BaseModel):
    entity_type: str
    entity_id: int
    account_id: int
    performed_by: int
    action: str
    details: Optional[Any] = None


class AuditLogResponse(BaseModel):
    audit_id: int
    entity_type: str
    entity_id: int
    account_id: int
    performed_by: int
    performed_at: datetime
    action: str
    details: Optional[Any]

    class Config:
        from_attributes = True