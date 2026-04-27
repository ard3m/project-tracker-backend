#account_schema

from pydantic import BaseModel
from typing import Optional


class AccountCreate(BaseModel):
    account_name: str
    account_email: str


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    account_email: Optional[str] = None


class AccountResponse(BaseModel):
    account_id: int
    account_name: str
    account_email: str

    class Config:
        from_attributes = True