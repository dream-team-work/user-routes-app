# app/init_db.py

from .database import engine
from .models import Base

# Cria as tabelas
Base.metadata.create_all(bind=engine)
