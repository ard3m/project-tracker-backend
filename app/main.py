#main.py
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions import ErrorResponse

from routers.account_router import router as account_router
from routers.user_router import router as user_router
from routers.project_router import router as project_router
from routers.task_router import router as task_router
from routers.materials_equipment_router import router as materials_equipment_router
from routers.project_access_router import router as project_access_router
from routers.project_contacts_router import router as project_contacts_router
from routers.image_router import router as image_router
from routers.image_attachment_router import router as image_attachment_router
from routers.audit_log_router import router as audit_log_router
from routers.auth_router import router as auth_router

from services.audit_log_service import write_audit_log

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    response = await call_next(request)

    print(f"{method} {path} -> {response.status_code}")

    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response


@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    start_time = time.time()

    # Extract user + account if available (depends on your auth layer)
    performed_by = request.headers.get("X-User-Id")
    account_id = request.headers.get("X-Account-Id")

    method = request.method
    path = request.url.path

    # Process request
    response = await call_next(request)

    duration = time.time() - start_time

    # Only log meaningful actions (skip docs, favicon, health checks)
    if not path.startswith("/docs") and not path.startswith("/openapi") and path != "/favicon.ico":
        await write_audit_log(
            entity_type="request",
            entity_id=None,
            account_id=int(account_id) if account_id else None,
            performed_by=int(performed_by) if performed_by else None,
            action=f"{method} {path}",
            details={
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        )

    return response

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    status = exc.status_code

    # Map status codes to clean error labels
    error_labels = {
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
    }

    return JSONResponse(
        status_code=status,
        content=ErrorResponse(
            status_code=status,
            error=error_labels.get(status, "HTTP Error"),
            message=str(exc.detail),
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status_code=422,
            error="Validation Error",
            message="Invalid request data",
            details={"errors": exc.errors()},
        ).model_dump()
    )


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status_code=500,
            error="Internal Server Error",
            message="An unexpected error occurred",
        ).model_dump()
    )

app.include_router(account_router, prefix="/accounts", tags=["Accounts"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
app.include_router(materials_equipment_router, prefix="/materials-equipment", tags=["Materials & Equipment"])
app.include_router(project_access_router, prefix="/project-access", tags=["Project Access"])
app.include_router(project_contacts_router, prefix="/project-contacts", tags=["Project Contacts"])
app.include_router(image_router, prefix="/images", tags=["Images"])
app.include_router(image_attachment_router, prefix="/image-attachments", tags=["Image Attachments"])
app.include_router(audit_log_router, prefix="/audit-logs", tags=["Audit Logs"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
