#vamos a crear la clase Personaje y Mision. Y la base declarativa para cear las tablas
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Base para los modelos ORM
Base = declarative_base

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    xp = Column(Integer, default=0)

    # realtionship() permite acceder a las realciones en ambos sentidos
    misiones = relationship("Mision", back_populates="personaje")

class Mision(Base): 
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)

    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    personaje = relationship("Personaje", back_populates="misiones")