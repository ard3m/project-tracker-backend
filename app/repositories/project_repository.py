from typing import List, Optional
from app.schemas.project import ProjectOut

class ProjectRepository:
    def __init__(self):
        self.projects: List[ProjectOut] = []
        self.next_id = 1

    def list_projects(self) -> List[ProjectOut]:
        return self.projects

    def get_project(self, project_id: int) -> Optional[ProjectOut]:
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    def create_project(self, project: ProjectOut) -> ProjectOut:
        self.projects.append(project)
        return project

    def delete_project(self, project_id: int) -> bool:
        original_len = len(self.projects)
        self.projects = [
            project_in_list for project_in_list in self.projects if project_in_list.project_id != project_id
        ]
        return len(self.projects) < original_len
