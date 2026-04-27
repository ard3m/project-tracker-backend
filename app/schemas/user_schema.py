#user_schema

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    account_id: int
    user_email: str
    username: str
    password: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    user_email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    user_id: int
    account_id: int
    user_email: str
    username: str
    first_name: str
    last_name: str
    last_login_time: Optional[datetime]

    class Config:
        from_attributes = True