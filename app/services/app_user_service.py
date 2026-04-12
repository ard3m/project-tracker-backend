#app_user_service.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import AppUser
from app.services.audit_log_service import write_audit_log

	async def create_user(
	    db: AsyncSession,
	    user_id: int,
        user_email: str,
        username: str,
        first_name: str,
        last_name: str,
        account_id: int,
        last_login_time: int,
	):
	    now = datetime.now(timezone.utc)
	    row = User(
	        user_id=user_id,
	        user_email=user_email,
	        username=username,
            first_name=first_name,
            last_name=last_name,
            account_id=account_id,
            last_login_time=last_login_time,
	    )
	    db.add(row)
	    await db.commit()
	    await db.refresh(row)
	    await write_audit_log(
	        db=db,
	        entity_type="app_user",
	        entity_id=row.account_id,
	        account_id=account_id,
	        performed_by=user_id,
	        action="create",
	        details={
	            "old": None,
	            "new": {
	                "user_id": user_id,
	                "user_email": user_email,
	                "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "account_id": account_id,
                    "last_login_time": last_login_time,
	            },
	        },
	        performed_at=now,
	    )
    return row

async def get_user(db: AsyncSession, user_id: int) -> AppUser | None:
    result = await db.execute(
        select(AppUser).where(AppUser.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_user(
    db: AsyncSession,
    user_id: int,
    new_user_email: str,
    new_username: str,
    new_first_name: str,
    new_last_name: str,
    account_id: int,
    user_id_performing: int,
):

    user = await get_user(db, user_id)
    if not user:
        raise ValueError("User not found")

    old = {
        "user_email": user.user_email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    now = datetime.now(timezone.utc)

    user.user_email = new_user_email
    user.username = new_username
    user.first_name = new_first_name
    user.last_name = new_last_name

    await write_audit_log(
        db=db,
        entity_type="app_user",
        entity_id=user_id,
        account_id=account_id,
        performed_by=user_id_performing,
        action="update",
        details={
            "old": old,
            "new": {
                "user_email": new_user_email,
                "username": new_username,
                "first_name": new_first_name,
                "last_name": new_last_name,
            },
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(user)

    return user


async def update_last_login_time(
    db: AsyncSession,
    user_id: int,
    account_id: int,
    user_id_performing: int,
):

    user = await get_user(db, user_id)
    if not user:
        raise ValueError("User not found")

    old = {"last_login_time": user.last_login_time}

    now = datetime.now(timezone.utc)
    user.last_login_time = now

    await write_audit_log(
        db=db,
        entity_type="app_user",
        entity_id=user_id,
        account_id=account_id,
        performed_by=user_id_performing,
        action="update",
        details={
            "old": old,
            "new": {"last_login_time": now.isoformat()},
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(user)

    return user

    
    	async def delete_user(
	    db: AsyncSession,
	    user_id: int,
	    account_id: int,
	    performed_by: int,
	):
	    # Fetch the user first
	    result = await db.execute(
	        select(AppUser).where(AppUser.user_id == user_id)
	    )
	    user = result.scalar_one_or_none()
	    if not user:
	        raise ValueError("User not found")
	    # Prepare old values for audit log
	    old = {
	        "user_email": user.user_email,
	        "username": user.username,
	        "first_name": user.first_name,
	        "last_name": user.last_name,
	    }
	    now = datetime.now(timezone.utc)
	    # Attempt deletion (will fail if RESTRICT is triggered)
	    await db.execute(
	        delete(AppUser).where(AppUser.user_id == user_id)
	    )
	    await write_audit_log(
	        db=db,
	        entity_type="app_user",
	        entity_id=user_id,
	        account_id=account_id,
	        performed_by=performed_by,
	        action="delete",
	        details={"old": old, "new": None},
	        performed_at=now,
	    )
	    await db.commit()
	    return True
