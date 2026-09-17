
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

import database
from schceduler import start_scheduler


app = FastAPI(title="ToDo Telegram Mini App")

BASE_DIR = Path(__file__).resolve().parent


@app.on_event("startup")
def on_startup():
    start_scheduler()


class TaskCreateSchema(BaseModel):
    title: str
    deadline: str
    chat_id: int


@app.get("/api/tasks")
def get_tasks():
    return database.get_all_tasks()


@app.post("/api/tasks")
def create_task(data: TaskCreateSchema):
    if not data.title or not data.deadline:
        raise HTTPException(
            status_code=400,
            detail="Заполните название и время"
        )

    new_task = database.add_task(
        title=data.title,
        deadline=data.deadline,
        chat_id=data.chat_id
    )

    return {
        "status": "ok",
        "task": new_task
    }


@app.post("/api/tasks/{task_id}/complete")
def complete_task(task_id: int):
    task = database.mark_task_completed(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена"
        )

    return {
        "status": "ok",
        "task": task
    }


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/")
async def serve_frontend():
    return FileResponse(
        BASE_DIR / "static" / "index.html"
    )
