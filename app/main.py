from http.client import HTTPException
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Task(BaseModel):
    name: str

books = [
    {
        "id": 1,
        "name": "Адольф",
        "description": "супер интересная книга"
    },
    {
        "id": 2,
        "name": "Принц на белом коне",
        "description": "ваще крутой конь на белом коне"
    }
]

@app.get("/books",
         tags=["Книги"],
         summary="Получить все книги")
def get_books():
    return books

@app.get("/books/{book_id}",
         tags=["Книги"],
         summary="Получить одну книгу"
         )
def get_book_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


#@app.post("/books")
#app.include_router(get_tasks)