#account_router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.account_schema import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
)
from app.services.account_service import (
    create_account,
    get_account,
    update_account,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/accounts", tags=["Accounts"])


# CREATE ACCOUNT
@router.post("/", response_model=AccountResponse)
async def create_account_endpoint(
    payload: AccountCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    row = await create_account(
        db=db,
        user_id=user.user_id,
        **payload.dict(),
    )
    return row


# GET ACCOUNT
@router.get("/{account_id}", response_model=AccountResponse)
async def get_account_endpoint(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    row = await get_account(db, account_id)
    if not row:
        raise HTTPException(status_code=404, detail="Account not found")
    return row


# UPDATE ACCOUNT
@router.put("/{account_id}", response_model=AccountResponse)
async def update_account_endpoint(
    account_id: int,
    payload: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    if account.account_id != account_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this account",
        )

    row = await update_account(
        db=db,
        account_id=account_id,
        user_id=user.user_id,
        **payload.dict(),
    )
    return row