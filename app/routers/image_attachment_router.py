#image_attachment_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.image_attachment import (
    ImageAttachmentCreate,
    ImageAttachmentResponse,
)
from app.services.image_attachment_service import (
    attach_image,
    get_image_attachment,
    delete_image_attachment,
    list_image_attachments,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/image_attachments", tags=["Image Attachments"])


@router.post("/", response_model=ImageAttachmentResponse)
async def attach_image_endpoint(
    payload: ImageAttachmentCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await attach_image(
        db=db,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        image_id=payload.image_id,
        account_id=account.account_id,
        user_id=user.user_id,
    )
    return row


@router.get("/{image_attachment_id}", response_model=ImageAttachmentResponse)
async def get_image_attachment_endpoint(
    image_attachment_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_image_attachment(db, image_attachment_id)
    if not row:
        raise HTTPException(status_code=404, detail="Image attachment not found")
    return row


@router.delete("/{image_attachment_id}", response_model=ImageAttachmentResponse)
async def delete_image_attachment_endpoint(
    image_attachment_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_image_attachment(db, image_attachment_id)
    if not row:
        raise HTTPException(status_code=404, detail="Image attachment not found")

    deleted = await delete_image_attachment(
        db=db,
        image_attachment_id=image_attachment_id,
        account_id=account.account_id,
        user_id=user.user_id,
    )
    return deleted


@router.get("/", response_model=list[ImageAttachmentResponse])
async def list_image_attachments_endpoint(
    entity_type: str | None = None,
    entity_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    filters = {"account_id": account.account_id}

    if entity_type:
        filters["entity_type"] = entity_type
    if entity_id:
        filters["entity_id"] = entity_id

    rows = await list_image_attachments(db, filters=filters)
    return rows