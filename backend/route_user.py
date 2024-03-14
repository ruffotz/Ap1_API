from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schema import UsuarioSchema

router = APIRouter(prefix="/usuarios")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
async def add_user(user_data: UsuarioSchema, db: Session = Depends(get_db)):
    new_user = User(id=request.id, username=request.username, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/listar")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return f"message: User with ID {user_id} deleted successfully"