from datetime import datetime
from repositories.project_repository import ProjectRepository
from schemas.project import ProjectCreate, ProjectOut

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def list_projects(self):
        return self.repo.list_projects()

    def create_project(self, data: ProjectCreate) -> ProjectOut:
        project = ProjectOut(
            project_id=self.repo.next_id,
            name=data.name,
            created_at=datetime.utcnow()
        )
        self.repo.next_id += 1
        return self.repo.create_project(project)

    def delete_project(self, project_id: int) -> bool:
        project = self.repo.get_project(project_id)
        if not project:
            return False

        self.repo.delete_project(project_id)
        return True
