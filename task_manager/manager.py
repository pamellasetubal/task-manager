from fastapi import FastAPI


app = FastAPI()
TASKS = []


@app.get("/tasks")
def list_tasks():
    return TASKS
