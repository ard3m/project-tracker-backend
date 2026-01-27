from fastapi import APIRouter
from typing import List

from app.schemas.history import HistoryEventOut
from app.storage.memory import history

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/", response_model=List[HistoryEventOut])
def get_history():
    return history
