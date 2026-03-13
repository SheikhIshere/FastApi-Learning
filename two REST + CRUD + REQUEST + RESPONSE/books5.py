from typing import Optional
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 
        

class BookRequest(BaseModel):
    # id: int
    id: Optional[int] = Field(default=None, description="ID of the book (optional for creation)")
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming",
                "author": "John Smith",
                "description": "Complete guide to Python",
                "rating": 5
            }
        }
    }



BOOKS = [
    Book(1, 'computer science pro', 'sheikh imran', ' best book in the history', 5),
    Book(2, 'Python Programming', 'John Smith', 'Complete guide to Python', 4),
    Book(3, 'Data Structures', 'Jane Doe', 'Essential data structures and algorithms', 4),
    Book(4, 'Web Development', 'Mike Johnson', 'Modern web development with React', 5),
    Book(5, 'Machine Learning', 'Sarah Wilson', 'Introduction to machine learning', 3),
    Book(6, 'Database Design', 'Robert Brown', 'SQL and database fundamentals', 4),
    Book(7, 'Cloud Computing', 'Emily Davis', 'AWS and cloud architecture', 5),
    Book(8, 'Cybersecurity', 'David Miller', 'Network security fundamentals', 4),
    Book(9, 'Mobile Development', 'Lisa Anderson', 'iOS and Android development', 3),
    Book(10, 'DevOps Essentials', 'James Taylor', 'CI/CD and deployment strategies', 5),
    Book(11, 'Software Engineering', 'Jennifer White', 'Software design patterns', 4)
]




@app.get('/')
def redirect_to_doc():
    return RedirectResponse('/docs')

# get all books
@app.get('/books/')
async def read_all_books():
    return BOOKS

# pydantic and data validation and post request
@app.post('/books/')
async def create_book(book_request: BookRequest):
    # print(type(book_request))
    # new_book = Book(**book_request.dict())
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_a_book_id(new_book))


def find_a_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book