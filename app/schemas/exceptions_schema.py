#exceptions_schema

from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None