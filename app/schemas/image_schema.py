#image_schema

from pydantic import BaseModel
from datetime import datetime


class ImageCreate(BaseModel):
    file_path: str
    uploaded_by: int


class ImageResponse(BaseModel):
    image_id: int
    file_path: str
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True