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

@app.get('/all-books')
async def first_api():
    return BOOKS