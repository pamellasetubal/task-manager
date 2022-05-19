from fastapi import FastAPI
from task_manager.task import InputTask, Task
from uuid import uuid4
from fastapi import status


app = FastAPI()
TASKS = []


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_tasks(task: InputTask):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task
