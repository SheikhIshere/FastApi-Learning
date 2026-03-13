from fastapi import FastAPI
import models
from database import engin

app = FastAPI()

# Create all tables in the database
models.Base.metadata.create_all(bind=engin)

@app.get("/")
def read_root():
    return {"Hello": "World"}

