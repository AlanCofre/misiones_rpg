from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# direccion de la base de datos
DATABASE_URL = "sqlite:///./rpg.db"

# crear el motor de la base de datos, la conexion con SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

#crear la sesion para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#crear todas las tablas definidas en models.py
def init_db():
    Base.metadata.create_all(bind=engine)