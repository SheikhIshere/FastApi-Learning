from turtle import update
from fastapi import FastAPI, Body

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
    {'title': 'title ten', 'author': 'Author ten', 'category': 'cooking'}
]

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
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book