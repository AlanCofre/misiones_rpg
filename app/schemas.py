from pydantic import BaseModel
from typing import Optional, List

class MisionBase(BaseModel):
    descripcion: str

class MisionCreate(MisionBase):
    pass

class MisionSchema(MisionBase):
    id: int

    class Config:
        from_attributes = True

class PersonajeBase(BaseModel):
    nombre: str

class PersonajeCreate(PersonajeBase):
    pass

class PersonajeSchema(PersonajeBase):
    id: int
    xp: int

    class Config:
        from_attributes = True

class PersonajeMisionBase(BaseModel):
    personaje_id: int
    mision_id: int

class PersonajeMisionCreate(PersonajeMisionBase):
    pass

class PersonajeMisionSchema(PersonajeMisionBase):
    id: int
    orden: int

    class Config:
        from_attributes = True
