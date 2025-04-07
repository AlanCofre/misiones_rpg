#aqui se defeniran todas las rutas que crean y listam los personajes y misiones, asigna las misiones desde la cola
#FIFO y ve el estado de la cola 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, cola

router = APIRouter()
cola_misiones = cola.ColaMisiones()

#dependecia para obtener la sesion de base de datos

def get_db():
    db = database.SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# crear un perosnaje
@router.post("/personajes", response_model=schemas.PersonajeSchema)
def crear_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = models.Personaje(nombre=personaje.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Listar personajes
@router.get("/personajes", response_model=list[schemas.PersonajeSchema])
def listar_personajes(db: Session = Depends(get_db)):
    return db.query(models.Personaje).all()

#Crear una mision y agregarla en la cola
@router.post("/misiones", response_model=schemas.MisionSchema)
def crear_mision(mision: schemas.MisionCreate, db: Session = Depends(get_db)):
    nueva = models.Mision(descripcion=mision.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    cola_misiones.agregar_mision(nueva.id) #solo el ID
    return nueva

# Ver misiones en la cola
@router.get("/cola", response_model=list[schemas.MisionSchema])
def ver_cola(db: Session = Depends(get_db)):
    ids = cola_misiones.obtener_todos_los_ids()
    if not ids:
        return[]
    misiones = db.query(models.Mision).filter(models.Mision.id.in_(ids)).all()
    # Para mantener el orden original segun cola
    ordenadas = sorted(misiones, key=lambda m: ids.index(m.id))
    return ordenadas

#asignar una mision de la cola a un perosnaje
@router.post("/asignar/{personaje_id}", response_model=schemas.MisionSchema)
def asignar_mision(personaje_id: int, db: Session = Depends(get_db)):
    mision_id = cola_misiones.obtener_siguiente_mision_id()
    if not mision_id:
        raise HTTPException(status_code=404, detail="No hay misiones en la cola.")

    mision = db.query(models.Mision).filter(models.Mision.id == mision_id).first()
    if not mision:
        raise HTTPException(status_code=404, details="Mision no encontrada.")
    
    personaje = db.query(models.Personaje).filter(models.Personaje.id == personaje_id).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")
    
    mision.personaje = personaje
    personaje.xp += 10    #Ganar experiencia por tomar la mision
    db.commit()
    db.refresh(mision)
    return mision