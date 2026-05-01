# app/services/auth_service.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from passlib.context import CryptContext

from app.models.user import AppUser
from app.services.audit_log_service import write_audit_log
from app.services.app_user_service import update_last_login_time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os
SECRET_KEY = os.getenv("SECRET_KEY") #the secret key is stored on my computer (server). By running in powershell: setx SECRET_KEY "your-long-random-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[AppUser]:
    result = await db.execute(
        select(AppUser).where(AppUser.user_email == email)
    )
    return result.scalar_one_or_none()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> dict:
    user = await get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    # assumes AppUser has a `password` column with the bcrypt hash
    if not verify_password(password, user.password):
        raise ValueError("Invalid credentials")

    now = datetime.now(timezone.utc)

    # update last_login_time using your existing service
    await update_last_login_time(
        db=db,
        user_id=user.user_id,
        account_id=user.account_id,
        user_id_performing=user.user_id,
    )

    access_token = create_access_token(
        {
            "sub": str(user.user_id),
            "account_id": str(user.account_id),
        }
    )

    await write_audit_log(
        db=db,
        entity_type="app_user",
        entity_id=user.user_id,
        account_id=user.account_id,
        performed_by=user.user_id,
        action="login",
        details={
            "old": None,
            "new": {
                "user_id": user.user_id,
                "user_email": user.user_email,
                "account_id": user.account_id,
                "last_login_time": now.isoformat(),
            },
        },
        performed_at=now,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
