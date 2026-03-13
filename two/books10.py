from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date
        

class BookRequest(BaseModel):
    # id: int
    id: Optional[int] = Field(default=None, description="ID of the book (optional for creation)")
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    publish_date: int = Field(gt=1200, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming",
                "author": "John Smith",
                "description": "Complete guide to Python",
                "rating": 5,
                "publish_date": 2024
            }
        }
    }



BOOKS = [
    Book(1, 'computer science pro', 'sheikh imran', ' best book in the history', 5, 2024),
    Book(2, 'Python Programming', 'John Smith', 'Complete guide to Python', 4, 2023),
    Book(3, 'Data Structures', 'Jane Doe', 'Essential data structures and algorithms', 4, 2022),
    Book(4, 'Web Development', 'Mike Johnson', 'Modern web development with React', 5, 2024),
    Book(5, 'Machine Learning', 'Sarah Wilson', 'Introduction to machine learning', 3, 2021),
    Book(6, 'Database Design', 'Robert Brown', 'SQL and database fundamentals', 4, 2023),
    Book(7, 'Cloud Computing', 'Emily Davis', 'AWS and cloud architecture', 5, 2024),
    Book(8, 'Cybersecurity', 'David Miller', 'Network security fundamentals', 4, 2022),
    Book(9, 'Mobile Development', 'Lisa Anderson', 'iOS and Android development', 3, 2021),
    Book(10, 'DevOps Essentials', 'James Taylor', 'CI/CD and deployment strategies', 5, 2023),
    Book(11, 'Software Engineering', 'Jennifer White', 'Software design patterns', 4, 2022)
]




@app.get('/')
def redirect_to_doc():
    return RedirectResponse('/docs')

# get all books
@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# get book by id
@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book 
    raise HTTPException(status_code=404, detail='Book not found')

# filter by rating
@app.get('/books/rating/{rating}', status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Path(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == rating]

# update a object
@app.put('/books/update_book', status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Book not found')


# filter by publish date
@app.get('/books/publish_date/', status_code=status.HTTP_200_OK)
# async def get_books_by_publish_date(publish_date: int = Path(gt=0)):
async def get_books_by_publish_date(publish_date: int = Query(gt=0)):
    return [book for book in BOOKS if book.publish_date == publish_date]

# delete a book
@app.delete('/books/delete_book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break

    if not book_change:
        raise HTTPException(status_code=404, detail='Book not found')

@app.post('/books/', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    # print(type(book_request))
    # new_book = Book(**book_request.dict()) # the .dict() used in pydantic v1
    new_book = Book(**book_request.model_dump()) # the .model_dump() used in pydantic v2
    print(type(new_book))
    BOOKS.append(find_a_book_id(new_book))
    return {"message": "Book created successfully"}


"""
this is a basically helper function to auto generate the id
it take new book compare with last book and the automatically
add 1 plus to the last book id
"""
def find_a_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

