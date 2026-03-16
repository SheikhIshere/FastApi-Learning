from fastapi import APIRouter, Depends, status, Path, HTTPException
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]


# get request for all data
@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_todo(db: db_dependence):
    return db.query(Todos).all()

# get specific todo
@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def get_all_todo_by_id(db: db_dependence, todo_id:int = Path(gt=0)):
    data = db.query(Todos).filter(Todos.id == todo_id).first()

    if data is not None:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='todo not found')


# data formation for todo
class TodoFormate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

# post a new todo
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependence, todo_request: TodoFormate):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    return todo_model

# update a todo
@router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependence,
                      todo_request: TodoFormate,
                      todo_id: int = Path(gt=0)
                    ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    # error handling
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='todo not found')        

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
    return todo_model


# delete a todo
@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependence,
                      todo_id: int = Path(gt=0)
                      ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # error handling
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='todo not found')

    db.delete(todo_model)
    db.commit()
    return {'message': 'todo deleted successfully'}
