#audit_log_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.audit_log_schema import 
    AuditLogCreate, 
    AuditLogResponse
from app.services.audit_log_service import (
    write_audit_log,
    list_audit_logs,
)
from app.dependencies.auth import get_current_user, get_current_account


router = APIRouter(prefix="/audit_logs", tags=["Audit Logs"])


@router.post("/", response_model=AuditLogResponse)
async def write_audit_log_endpoint(
    payload: AuditLogCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    row = await write_audit_log(
        db=db,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        account_id=account.account_id,
        performed_by=user.user_id,
        action=payload.action,
        details=payload.details,
        performed_at=payload.performed_at,
    )
    return row


@router.get("/entity", response_model=list[AuditLogResponse])
async def list_audit_log_endpoint(
    entity_type: str,
    entity_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    rows = await list_audit_logs(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id,
        account_id=account.account_id,
    )
    return rows


@router.get("/", response_model=list[AuditLogResponse])
async def list_audit_logs_endpoint(
    filters: dict | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account=Depends(get_current_account),
):
    if filters is None:
        filters = {}

    filters["account_id"] = account.account_id

    rows = await list_audit_logs(
        db=db,
        entity_type=filters.get("entity_type"),
        entity_id=filters.get("entity_id"),
        account_id=filters.get("account_id"),
    )
    return rows