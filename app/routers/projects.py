from fastapi import APIRouter, HTTPException
from schemas.project import ProjectCreate, ProjectOut
from repositories.project_repository import ProjectRepository
from services.project_service import ProjectService

router = APIRouter()

repo = ProjectRepository()
service = ProjectService(repo)

@router.get("/projects", response_model=list[ProjectOut])
def list_projects():
    return service.list_projects()

@router.post("/projects", response_model=ProjectOut)
def create_project(data: ProjectCreate):
    return service.create_project(data)

@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int):
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
