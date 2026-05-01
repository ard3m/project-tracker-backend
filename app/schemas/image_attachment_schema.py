#image_attachment_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageAttachmentCreate(BaseModel):
    entity_type: str
    entity_id: int
    image_id: int
    updated_by: int


class ImageAttachmentUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    image_id: Optional[int] = None
    updated_by: Optional[int] = None


class ImageAttachmentResponse(BaseModel):
    image_attachment_id: int
    entity_type: str
    entity_id: int
    image_id: int
    updated_at: datetime
    updated_by: int

    class Config:
        from_attributes = True