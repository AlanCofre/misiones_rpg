from pydantic import BaseModel
from typing import Optional

class MisionBase(BaseModel):
    descripcion: str

class MisionCreate(MisionBase):
    pass

class MisionSchema(MisionBase):
    id: int
    personaje_id: Optional[int] = None

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
