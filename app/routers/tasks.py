from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.task import TaskCreate, TaskOut
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository

router = APIRouter()

repo = TaskRepository()
service = TaskService(repo)

@router.post("/tasks", response_model=TaskOut)
def create_task(data: TaskCreate):
    return service.create_task(data)

@router.get("/tasks", response_model=list[TaskOut])
def list_tasks():
    return service.list_tasks()

@router.get("/tasks/{task_id}", response_model=TaskOut) #this should be ok once wired in others.
def get_task(task_id: int):
    return service.get_task(task_id)

