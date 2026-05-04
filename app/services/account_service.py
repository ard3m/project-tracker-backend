#account_service.py
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.account import Account
from app.services.audit_log_service import write_audit_log

async def create_account(
    db: AsyncSession,
    account_id: int,
    account_name: str,
    account_email: str,
    user_id: int, #not implemented as part of the account_model yet. there is no row for 'user_id'
):
    now = datetime.now(timezone.utc)
    row = Account(
	    account_id=account_id,
	    account_name=account_name,
	    account_email=account_email,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    await write_audit_log(
	    db=db,
	    entity_type="account",
	    entity_id=row.account_id,
	    account_id=account_id,
	    performed_by=user_id,
	    action="create",
	    details={
	        "old": None,
	        "new": {
	            "account_id": account_id,
	            "account_name": account_name,
	            "account_email": account_email,
	        },
	    },
	    performed_at=now,
    )

    return row


async def get_account(db: AsyncSession, account_id: int) -> Account | None:
    result = await db.execute(
        select(Account).where(Account.account_id == account_id)
    )
    return result.scalar_one_or_none()


async def update_account(
    db: AsyncSession,
    account_id: int,
    new_account_name: str,
    new_account_email: str,
    user_id: int,          # the user performing the update
):

    account = await get_account(db, account_id)
    if not account:
        raise ValueError("Account not found")

    old = {
        "account_name": account.account_name,
        "account_email": account.account_email,
    }

    now = datetime.now(timezone.utc)

    account.account_name = new_account_name
    account.account_email = new_account_email

    await write_audit_log(
        db=db,
        entity_type="account",
        entity_id=account_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={
            "old": old,
            "new": {
                "account_name": new_account_name,
                "account_email": new_account_email,
            },
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(account)

    return account