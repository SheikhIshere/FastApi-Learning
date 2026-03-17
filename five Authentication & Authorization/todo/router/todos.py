from fastapi import APIRouter, status, Path, HTTPException
from models import Todos
from pydantic import BaseModel, Field
from dependencies import db_dependence, user_dependence


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

# get request for all data
@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_todo(user: user_dependence, db: db_dependence):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authentication failed'
        )
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

# get specific todo
@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def get_all_todo_by_id(user: user_dependence, db: db_dependence, todo_id:int = Path(gt=0)): 
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authentication failed'
        )
    data = db.query(Todos).filter(
        Todos.id == todo_id, 
        Todos.owner_id == user.get('id')
    ).first()

    if data is not None:
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail='todo not found'
    )


# data formation for todo
class TodoFormate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

# post a new todo
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependence, db: db_dependence, 
                                    todo_request: TodoFormate):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authentication failed'
        )
    todo_model = Todos(**todo_request.model_dump())
    todo_model.owner_id = user.get('id')
    db.add(todo_model)
    db.commit()
    return todo_model

# update a todo
@router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependence, db: db_dependence,
                      todo_request: TodoFormate,
                      todo_id: int = Path(gt=0)
                    ):
    todo_model = db.query(Todos).filter(
        Todos.id == todo_id, 
        Todos.owner_id == user.get('id')
    ).first()
    
    # error handling
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='todo not found'
        )        

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
    return todo_model


# delete a todo
@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependence, db: db_dependence,
                      todo_id: int = Path(gt=0)
                      ):
    todo_model = db.query(Todos).filter(
        Todos.id == todo_id, 
        Todos.owner_id == user.get('id')
    ).first()

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='todo not found'
        )

    db.delete(todo_model)
    db.commit()
    return  # No response body for 204