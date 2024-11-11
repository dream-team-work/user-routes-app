# app/crud.py

from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

# Função para criar um novo usuário
def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, role=user.role, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Função para obter um usuário por username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
