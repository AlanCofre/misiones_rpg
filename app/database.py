from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '../rpg.db')}"

# crear el motor de la base de datos, la conexion con SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#crear la sesion para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#crear todas las tablas definidas en models.py
def init_db():
    Base.metadata.create_all(bind=engine)