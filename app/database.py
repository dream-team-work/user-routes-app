import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de Conexão com PostgreSQL (ajustada)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

# Espera 5 segundos para garantir que o PostgreSQL esteja pronto
time.sleep(5)

# Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})

# Criação da Sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()

# Função para obter a sessão local
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
