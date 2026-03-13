# assignment
"""
Assignment

Here is your opportunity to keep learning!
Add a new field to Book and BookRequest called published_date: int (for example, 
published_date: int = 2012). So, this book as published on the year of 2012.
Enhance each Book to now have a published_date
Then create a new GET Request method to filter by published_date

Solution in next video
"""


# imports
from fastapi import FastAPI
from pydantic import Field, BaseModel

app = FastAPI()



class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# validation
class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int = Field(gt=1900, lt=2026, description='please provide the year only')

BOOKS = [
    Book(1, "Book 1", "Author 1", "Description 1", 5, 2012),
    Book(2, "Book 2", "Author 2", "Description 2", 4, 2013),
    Book(3, "Book 3", "Author 3", "Description 3", 3, 2014),
    Book(4, "Book 4", "Author 4", "Description 4", 2, 2015),
    Book(5, "Book 5", "Author 5", "Description 5", 1, 2016),
]

# TODO: create a new GET Request method to filter by published_date
@app.get('/books/publish-date')
async def get_books_by_publish_date(publish_date: int):
    for book in BOOKS:
        if book.published_date == publish_date:
            return book
    return {"message": "Book not found"}