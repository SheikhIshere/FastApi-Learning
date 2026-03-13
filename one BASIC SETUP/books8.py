from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse


app = FastAPI()


BOOKS = [
    {'title': 'title one', 'author': 'Author one', 'category': 'science'},
    {'title': 'title two', 'author': 'Author two', 'category': 'history'},
    {'title': 'title three', 'author': 'Author three', 'category': 'fiction'},
    {'title': 'title four', 'author': 'Author four', 'category': 'philosophy'},
    {'title': 'title five', 'author': 'Author five', 'category': 'technology'},
    {'title': 'title six', 'author': 'Author six', 'category': 'art'},
    {'title': 'title seven', 'author': 'Author seven', 'category': 'biography'},
    {'title': 'title eight', 'author': 'Author eight', 'category': 'poetry'},
    {'title': 'title nine', 'author': 'Author nine', 'category': 'travel'},
    {'title': 'title ten', 'author': 'Author two', 'category': 'cooking'}
]

# redirect to docs
@app.get('/')
def redirect_to_doc():
    return RedirectResponse(url='/docs')

@app.get('/books')
async def read_all_books():
    return BOOKS

# post method
@app.post('/books/create')
async def create_book(new_book=Body()):
    BOOKS.append(new_book) 

# put method
@app.put('/books/update')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


# delete method
@app.delete(('/books/delete/{book_title}'))
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

@app.get('/books/by/{author_name}/all')
async def fetch_author_book(author_name: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            book_to_return.append(book)
    return book_to_return

