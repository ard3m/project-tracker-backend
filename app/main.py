from fastapi import FastAPI

from app.routers import projects, tasks, history

app = FastAPI(title="Project Tracking API")

app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(history.router)


@app.get("/")
def root():
    return {"status": "API is running"}
