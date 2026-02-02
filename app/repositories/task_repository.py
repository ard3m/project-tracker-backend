from typing import List, Optional
from app.schemas.task import TaskOut

class TaskRepository:
    def __init__(self):
        self.tasks: List[TaskOut] = []
        self.next_id = 1

    def list_tasks(self) -> List[TaskOut]:
        return self.tasks

    def get_task(self, task_id: int) -> Optional[TaskOut]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def create_task(self, task: TaskOut) -> TaskOut:
        self.tasks.append(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        original_len = len(self.tasks)
        self.tasks = [
            task_in_list for task_in_list in self.tasks if task_in_list.task_id != task_id
        ]
        return len(self.tasks) < original_len
