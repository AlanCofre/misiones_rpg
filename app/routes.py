from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, cola

router = APIRouter()
cola_misiones = cola.ColaMisiones()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/personajes", response_model=schemas.PersonajeSchema)
def crear_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = models.Personaje(nombre=personaje.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/personajes", response_model=list[schemas.PersonajeSchema])
def listar_personajes(db: Session = Depends(get_db)):
    return db.query(models.Personaje).all()

@router.post("/misiones", response_model=schemas.MisionSchema)
def crear_mision(mision: schemas.MisionCreate, db: Session = Depends(get_db)):
    nueva = models.Mision(descripcion=mision.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    cola_misiones.agregar_mision(nueva.id)
    return nueva

@router.post("/personajes/{personaje_id}/misiones/{mision_id}", response_model=schemas.PersonajeMisionSchema)
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    
    #verificar  existencia del personaje
    personaje = db.query(models.Personaje).filter(models.Personaje.id == personaje_id).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")
    
    #verificar exitencia de la mision
    mision = db.query(models.Mision).filter(models.Mision.id == mision_id).first()
    if not mision:
        raise HTTPException(status_code=404, detail="Mision no encontrada.")
    
    #verificar si la mision ya fue asignada al personaje
    existente = db.query(models.PersonajeMision).filter_by(personaje_id=personaje_id, mision_id=mision_id).first()
    if existente:
        raise HTTPException(status_code=404, detail="Esta mision ya está asignada al personaje.")
    
    #calcular orden: ultimo +1
    ultimo = db.query(models.PersonajeMision).filter_by(personaje_id=personaje_id).order_by(models.PersonajeMision.orden.desc()).first()
    nuevo_orden = ultimo.orden + 1 if ultimo else 0

    asignacion = models.PersonajeMision(
        personaje_id = personaje_id,
        mision_id = mision_id,
        orden = nuevo_orden
    )

    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    return asignacion

@router.get("/personajes/{personaje_id}/misiones", response_model=list[schemas.MisionSchema])
def misiones_personaje(personaje_id: int, db: Session = Depends(get_db)):
    # Verificar que el personaje exista
    personaje = db.query(models.Personaje).filter(models.Personaje.id == personaje_id).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    # Obtener asignaciones en orden FIFO
    asignaciones = (
        db.query(models.PersonajeMision)
        .filter(models.PersonajeMision.personaje_id == personaje_id)
        .order_by(models.PersonajeMision.orden)
        .all()
    )

    # Obtener todas las misiones correspondientes
    misiones = [a.mision for a in asignaciones]
    return misiones

@router.post("/personajes/{personaje_id}/completar", response_model=schemas.MisionSchema)
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    # Verificar existencia del personaje
    personaje = db.query(models.Personaje).filter(models.Personaje.id == personaje_id).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    # Obtener la misión más antigua en la cola (orden más bajo)
    asignacion = (
        db.query(models.PersonajeMision)
        .filter(models.PersonajeMision.personaje_id == personaje_id)
        .order_by(models.PersonajeMision.orden)
        .first()
    )

    if not asignacion:
        raise HTTPException(status_code=404, detail="No hay misiones para completar.")

    mision = asignacion.mision

    # Eliminar la asignación y sumar XP
    db.delete(asignacion)
    personaje.xp += 50
    db.commit()

    return mision
