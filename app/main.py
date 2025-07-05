
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Task(BaseModel):
    name: str

@app.get("/tasks")
def get_tasks():
    task = Task(name="дай мне новую задачу!")
    return {"data": task}

#app.include_router(get_tasks)