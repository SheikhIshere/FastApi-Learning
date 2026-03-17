from fastapi import APIRouter, Depends, status, Path, HTTPException
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from dependencies import user_dependence, db_dependence

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
) 

@router.get("/")
async def admin_read_all(user: user_dependence, db: db_dependence):
    if user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Permission denied")
    
    return db.query(Todos).all()


@router.delete("/{todo_id}")
async def delete_todo(user: user_dependence, db: db_dependence, todo_id: int = Path(gt=0)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Permission denied")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return {"message": "Todo deleted successfully"}

# put
@router.put("/{todo_id}")
async def update_todo(user: user_dependence, db: db_dependence, todo_id: int = Path(gt=0)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Permission denied")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = todo.title
    todo.description = todo.description
    todo.priority = todo.priority
    todo.complete = todo.complete
    
    db.commit()
    
    return {"message": "Todo updated successfully"}