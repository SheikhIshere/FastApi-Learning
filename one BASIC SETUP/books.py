from fastapi import FastAPI

app = FastAPI()

@app.get('/hi')
async def first_api():
# def first_api():
    return {
        'message':'hello in the world of fast api'
    }