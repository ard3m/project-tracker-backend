#image_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.image_schema import (
    ImageCreate,
    ImageUpdate,
    ImageResponse,
)
from app.services.image_service import (
    create_image,
    get_image,
    update_image,
    list_images,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/", response_model=ImageResponse)
async def create_image_endpoint(
    payload: ImageCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    row = await create_image(
        db=db,
        file_path=payload.file_path,
        uploaded_by=user.user_id,
    )
    return row


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image_endpoint(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    row = await get_image(db, image_id)
    if not row:
        raise HTTPException(status_code=404, detail="Image not found")
    return row


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image_endpoint(
    image_id: int,
    payload: ImageUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await get_image(db, image_id)
    if not row:
        raise HTTPException(status_code=404, detail="Image not found")

    updated = await update_image(
        db=db,
        image_id=image_id,
        new_file_path=payload.file_path,
        user_id=user.user_id,
        account_id=account.account_id,
    )
    return updated


@router.get("/", response_model=list[ImageResponse])
async def list_images_endpoint(
    uploaded_by: int | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    filters = {}
    if uploaded_by is not None:
        filters["uploaded_by"] = uploaded_by

    rows = await list_images(db, filters=filters)
    return rows