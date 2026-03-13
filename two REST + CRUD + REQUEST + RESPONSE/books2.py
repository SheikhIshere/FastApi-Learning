from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 
        


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

# post a new book
@app.post('/books/')
async def create_book(book_request = Body()):
    BOOKS.append(book_request)
    return BOOKS
