#vamos a crear la clase Personaje y Mision. Y la base declarativa para cear las tablas
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Inicializa la base para definir tablas ORM
Base = declarative_base()

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    xp = Column(Integer, default=0)

    # realtionship() permite acceder a las realciones en ambos sentidos
    misiones_en_cola = relationship("PersonajeMision", back_populates="personaje")

class Mision(Base): 
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)

    asignaciones = relationship("PersonajeMision", back_populates="mision")

class PersonajeMision(Base):
    __tablename__ = "personaje_mision"

    id = Column(Integer, primary_key=True )
    personaje_id = Column(Integer, ForeignKey("perosnajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    orden = Column(Integer, nullable=False)

    personaje = relationship("Personaje", back_populates="misiones_en_cola")
    mision = relationship("Mision", back_populates="asignaciones")