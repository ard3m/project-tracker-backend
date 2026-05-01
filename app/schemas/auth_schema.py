#auth_schema
from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    account_id: str
    exp: Optional[int] = None
