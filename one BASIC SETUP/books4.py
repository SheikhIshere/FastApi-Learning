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

@app.get('/books/by-category')
async def read_category_by_query(category: str):
    book_to_return = []
    i = 0
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_to_return.append(book)
            i += 1
    
    return {"books": book_to_return, "total_results": i}

@app.get('/books/by-author/{books_author}')
async def read_author_and_category_by_query(books_author: str, category: str):
    books_to_return = []
    i = 0
    for book in BOOKS:
        if book.get('author').casefold() == books_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
            i += 1
    
    return {"books": books_to_return, "total_results": i}

@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


