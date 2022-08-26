from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_lenght=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_lenght = 1)
    rating: int = Field(gt=-1, lt=101)
    
BOOKS = []

# @app.get("/")
# def read_api():
    # return{"welcome": "user"}
    
# @app.get("/{name}")
# def read_api(name: str):
    # return{"welcome": name}

@app.get("/create")
def create_book():
    return BOOKS

@app.post("/book")
def create_book(book: Book):
    BOOKS.append(book)
    return book