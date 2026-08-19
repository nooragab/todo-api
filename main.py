from fastapi import FastAPI, HTTPException

app = FastAPI()

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
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201)
def create_task(task: dict):
    if "title" not in task or not task["title"].strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    new_task = {
        "id": max([t["id"] for t in tasks]) + 1,
        "title": task["title"],
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    if "title" not in task and "done" not in task:
        raise HTTPException(
            status_code=400,
            detail="At least title or done is required"
        )

    if "title" in task and not isinstance(task["title"], str):
        raise HTTPException(
            status_code=400,
            detail="Title must be text"
        )

    if "title" in task and not task["title"].strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if "done" in task and not isinstance(task["done"], bool):
        raise HTTPException(
            status_code=400,
            detail="Done must be true or false"
        )

    for existing_task in tasks:
        if existing_task["id"] == task_id:
            if "title" in task:
                existing_task["title"] = task["title"]

            if "done" in task:
                existing_task["done"] = task["done"]

            return existing_task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )    