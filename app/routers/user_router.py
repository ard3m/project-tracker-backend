#user_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.app_user import (
    AppUserCreate,
    AppUserUpdate,
    AppUserResponse,
)
from app.services.app_user_service import (
    create_user,
    get_user,
    update_user,
    update_last_login_time,
    list_users,
    archive_user,
    unarchive_user,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=AppUserResponse)
async def create_user_endpoint(
    payload: AppUserCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await create_user(
        db=db,
        account_id=account.account_id,
        user_id_performing=user.user_id,
        **payload.dict(),
    )
    return row


@router.get("/{user_id}", response_model=AppUserResponse)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_user(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if row.account_id != account.account_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return row


@router.get("/", response_model=list[AppUserResponse])
async def list_users_endpoint(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    rows = await list_users(
        db=db,
        filters={"account_id": account.account_id},
    )
    return rows


@router.put("/{user_id}", response_model=AppUserResponse)
async def update_user_endpoint(
    user_id: int,
    payload: AppUserUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_user(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if row.account_id != account.account_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    updated = await update_user(
        db=db,
        user_id=user_id,
        account_id=account.account_id,
        user_id_performing=user.user_id,
        **payload.dict(),
    )
    return updated


@router.post("/{user_id}/update_last_login", response_model=AppUserResponse)
async def update_last_login_time_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_user(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if row.account_id != account.account_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    updated = await update_last_login_time(
        db=db,
        user_id=user_id,
        account_id=account.account_id,
        user_id_performing=user.user_id,
    )
    return updated


@router.post("/{user_id}/archive", response_model=AppUserResponse)
async def archive_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_user(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if row.account_id != account.account_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    archived = await archive_user(
        db=db,
        user_id=user_id,
        account_id=account.account_id,
        user_id_performing=user.user_id,
    )
    return archived


@router.post("/{user_id}/unarchive", response_model=AppUserResponse)
async def unarchive_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_user(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    if row.account_id != account.account_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    unarchived = await unarchive_user(
        db=db,
        user_id=user_id,
        account_id=account.account_id,
        user_id_performing=user.user_id,
    )
    return unarchived