from fastapi import APIRouter
from datetime import datetime
from typing import List

from app.schemas.project import ProjectCreate, ProjectOut
from app.schemas.history import HistoryEventOut
from app.storage.memory import projects, history

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate):
    project_out = ProjectOut(
        id=len(projects) + 1,
        name=project.name,
        created_at=datetime.utcnow()
    )

    projects.append(project_out)

    history.append(
        HistoryEventOut(
            id=len(history) + 1,
            event_type="PROJECT_CREATED",
            description=f"Project '{project.name}' created",
            timestamp=datetime.utcnow()
        )
    )

    return project_out


@router.get("/", response_model=List[ProjectOut])
def get_projects():
    return projects
