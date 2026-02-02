from fastapi import FastAPI
from app.routers.projects import router as project_router
from app.routers.tasks import router as task_router

app = FastAPI()

app.include_router(project_router)
app.include_router(task_router)
