#image_attachment_service.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.image_attachment import ImageAttachment
from app.services.audit_log_service import write_audit_log


async def get_image_attachment(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
) -> ImageAttachment | None:

    result = await db.execute(
        select(ImageAttachment)
        .where(ImageAttachment.entity_type == entity_type)
        .where(ImageAttachment.entity_id == entity_id)
    )
    return result.scalar_one_or_none()


async def attach_image( #CREATE
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
    image_id: int,
    account_id: int,
    user_id: int,
):

    now = datetime.now(timezone.utc)

    attachment = ImageAttachment(
        entity_type=entity_type,
        entity_id=entity_id,
        image_id=image_id,
        updated_at=now,
        updated_by=user_id,
    )

    db.add(attachment)

    await write_audit_log(
        db=db,
        entity_type="image_attachment",
        entity_id=entity_id,
        account_id=account_id,
        performed_by=user_id,
        action="create",
        details={
            "old": None,
            "new": {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "image_id": image_id,
            },
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(attachment)

    return attachment


async def update_image_attachment(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
    new_image_id: int,
    account_id: int,
    user_id: int,
):

    attachment = await get_image_attachment(db, entity_type, entity_id)
    if not attachment:
        raise ValueError("ImageAttachment not found")

    old = {
        "image_id": attachment.image_id,
    }

    now = datetime.now(timezone.utc)

    attachment.image_id = new_image_id
    attachment.updated_at = now
    attachment.updated_by = user_id

    await write_audit_log(
        db=db,
        entity_type="image_attachment",
        entity_id=entity_id,
        account_id=account_id,
        performed_by=user_id,
        action="update",
        details={
            "old": old,
            "new": {"image_id": new_image_id},
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(attachment)

    return attachment


async def delete_image_attachment(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
    account_id: int,
    user_id: int,
):

    attachment = await get_image_attachment(db, entity_type, entity_id)
    if not attachment:
        raise ValueError("ImageAttachment not found")

    old = {
        "entity_type": attachment.entity_type,
        "entity_id": attachment.entity_id,
        "image_id": attachment.image_id,
    }

    now = datetime.now(timezone.utc)

    await db.execute(
        delete(ImageAttachment)
        .where(ImageAttachment.image_attachment_id == attachment.image_attachment_id)
    )

    await write_audit_log(
        db=db,
        entity_type="image_attachment",
        entity_id=entity_id,
        account_id=account_id,
        performed_by=user_id,
        action="delete",
        details={"old": old, "new": None},
        performed_at=now,
    )

    await db.commit()

    return True


async def list_image_attachments(
    db: AsyncSession,
    filters: dict | None = None,
):
    query = select(ImageAttachment)

    # Optional dynamic filters
    if filters:
        for field, value in filters.items():
            query = query.where(getattr(ImageAttachment, field) == value)

    result = await db.execute(query)
    return result.scalars().all()