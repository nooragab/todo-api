from fastapi import FastAPI, HTTPException

app = FastAPI()

print("MY MAIN FILE IS RUNNING")

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Clean the house", "done": False}
]


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            return tasks[i]
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: dict):
    if "title" not in task or not task["title"].strip():
        raise HTTPException(status_code=400, detail="Title is required")

    new_task = {
        "id": max([t["id"] for t in tasks]) + 1,
        "title": task["title"],
        "done": False
    }

    tasks.append(new_task)
    return new_task