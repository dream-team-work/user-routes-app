# app/models.py

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"

class UserData(Base):
    __tablename__ = "user_data"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    role = Column(String)
    data = Column(JSON)  # Aqui armazenamos os dados como JSON

    def __repr__(self):
        return f"<UserData(username={self.username}, role={self.role}, data={self.data})>"
