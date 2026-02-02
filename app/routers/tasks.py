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

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate):
    task_out = TaskOut(
        id=len(tasks) + 1,
        project_id=task.project_id,
        title=task.title,
        status=task.status,
        updated_at=datetime.utcnow()
    )

    tasks.append(task_out)

    history.append(
        HistoryEventOut(
            id=len(history) + 1,
            event_type="TASK_CREATED",
            description=f"Task '{task.title}' added to project {task.project_id}",
            timestamp=datetime.utcnow()
        )
    )

    return task_out


@router.put("/{task_id}", response_model=TaskOut)
def update_task_status(task_id: int, status: str):
    for task in tasks:
        if task.id == task_id:
            task.status = status
            task.updated_at = datetime.utcnow()

            history.append(
                HistoryEventOut(
                    id=len(history) + 1,
                    event_type="TASK_UPDATED",
                    description=f"Task {task_id} updated to '{status}'",
                    timestamp=datetime.utcnow()
                )
            )

            return task

    raise HTTPException(status_code=404, detail="Task not found")
