from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskOut


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def list_tasks(self):
        return self.repo.list_tasks()

    def get_task(self, task_id: int) -> TaskOut | None:
        return self.repo.get_task(task_id)

    def create_task(self, data: TaskCreate) -> TaskOut:
        return self.repo.create_task(data)

    def delete_task(self, task_id: int) -> bool:
        return self.repo.delete_task(task_id)
