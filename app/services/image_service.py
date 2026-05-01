#image_service.py

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.image import Image
from app.services.audit_log_service import write_audit_log

async def create_image(
    db: AsyncSession,
    image_id: int,
    file_path: str,
    user_id: int,
    uploaded_at: int,
    uploaded_by: int,
):
    now = datetime.now(timezone.utc)
    row = image(
        image_id=image_id,
        file_path=new_file_path,
        uploaded_at=now,      
        uploaded_by=user_id,  
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    await write_audit_log(
        db=db,
        entity_type="image",
        entity_id=row.image_id,
        performed_by=user_id,
        action="create",
        details={
            "old": None,
            "new": {
                "image_id": image_id,
                "file_path": file_path,
                "uploaded_at": uploaded_at,
                "uploaded_by": uploaded_by,
            },
        },
        performed_at=now,
    )
    return row

async def get_image(db: AsyncSession, image_id: int) -> Image | None:
    result = await db.execute(
        select(Image).where(Image.image_id == image_id)
    )
    return result.scalar_one_or_none()


async def update_image(
    db: AsyncSession,
    image_id: int,
    new_file_path: str,
    user_id: int,
):

    image = await get_image(db, image_id)
    if not image:
        raise ValueError("Image not found")

    old = {
        "file_path": image.file_path,
    }

    now = datetime.now(timezone.utc)

    image.file_path = new_file_path
    # image.uploaded_by and uploaded_at NEVER change

    await write_audit_log(
        db=db,
        entity_type="image",
        entity_id=image_id,
        performed_by=user_id,
        action="update",
        details={
            "old": old,
            "new": {"file_path": new_file_path},
        },
        performed_at=now,
    )

    await db.commit()
    await db.refresh(image)

    return image

async def list_images(
    db: AsyncSession,
    filters: dict | None = None,
):
    query = select(Image)

    # Optional dynamic filters
    if filters:
        for field, value in filters.items():
            query = query.where(getattr(Image, field) == value)

    result = await db.execute(query)
    return result.scalars().all()