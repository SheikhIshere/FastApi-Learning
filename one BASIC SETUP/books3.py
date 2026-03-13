from fastapi import FastAPI

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

@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get('/books/my-books') 
async def read_all_books():
    """ 
    if this stays after dynamic params book this will 
    show the dynamic one instead of my book cz python
    execute program with chronological order so even you try 
    to hit this thing you get up one :) what i have seen in django
    """
    return {'title': 'art of seduction :)'}

@app.get('/books/{dynamic_param}')
async def read_all_books(dynamic_param: str):
    return {'dynamic_param': dynamic_param}

# @app.get('/books/my-books') 
# async def read_all_books():
#     """ 
#     if this stays after dynamic params book this will 
#     show the dynamic one instead of my book cz python
#     execute program with chronological order so even you try 
#     to hit this thing you get up one :) what i have seen in django
#     """
#     return {'title': 'art of seduction :)'}

