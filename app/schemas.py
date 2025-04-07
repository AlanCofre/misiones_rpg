# Usaremos Pyantic para validar y estructurar los datos que entran o salen de mi API
from pydantic import BaseModel
from typing import List, Optional

# Esquema para crear un personaje
class PersonajeCreate(BaseModel):
    nombre: str

#esquema para crear una mision
class MisionCreate(BaseModel):
    descripcion: str
    
# esquema para mostrar un personaje 
class MisionSchema(BaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True

class PersonajeSchema(BaseModel):
    id: int
    nombre: str
    xp: int
    misiones: Optional[List [MisionSchema]] = []

    class Config:
        orm_mode = True


