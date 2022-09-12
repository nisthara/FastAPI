# from fastapi import FastAPI,HTTPException
# from pydantic import BaseModel, Field
# from uuid import UUID

# app = FastAPI()

# class Book(BaseModel):
#     id: UUID
#     title: str = Field(min_lenght=1)
#     author: str = Field(min_length=1, max_length=100)
#     description: str = Field(min_lenght = 1)
#     rating: int = Field(gt=-1, lt=101)
    
# BOOKS = []

# # @app.get("/")
# # def read_api():
#     # return{"welcome": "user"}
    
# # @app.get("/{name}")
# # def read_api(name: str):
#     # return{"welcome": name}

# @app.get("/create")
# def create_book():
#     return BOOKS

# @app.post("/book")
# def create_book(book: Book):
#     BOOKS.append(book)
#     return book
    
# def update_book(book_id: UUID, book: Book):
#     counter = 0
    
#     for x in BOOKS:
#         counter += 1
#         if x.id == book_id:
#             BOOKS[counter - 1] = book
#             return BOOKS[counter-1]

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

