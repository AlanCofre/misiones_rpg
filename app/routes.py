from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

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
    return nueva

@router.post("/personajes/{personaje_id}/misiones/{mision_id}", response_model=schemas.PersonajeMisionSchema)
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = db.query(models.Personaje).get(personaje_id)
    mision = db.query(models.Mision).get(mision_id)
    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrada.")
    
    existe = db.query(models.PersonajeMision).filter_by(personaje_id=personaje_id, mision_id=mision_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="Misión ya asignada.")
    
    ultimo = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .order_by(models.PersonajeMision.orden.desc()).first()
    orden = ultimo.orden + 1 if ultimo else 0

    asignacion = models.PersonajeMision(
        personaje_id=personaje_id,
        mision_id=mision_id,
        orden=orden
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    return asignacion

@router.get("/personajes/{personaje_id}/misiones", response_model=list[schemas.MisionSchema])
def misiones_personaje(personaje_id: int, db: Session = Depends(get_db)):
    if not db.query(models.Personaje).get(personaje_id):
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")
    
    asignaciones = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .order_by(models.PersonajeMision.orden).all()
    return [a.mision for a in asignaciones]

@router.post("/personajes/{personaje_id}/completar", response_model=schemas.MisionSchema)
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(models.Personaje).get(personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado.")

    asignacion = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .order_by(models.PersonajeMision.orden).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="No hay misiones para completar.")

    mision = asignacion.mision
    db.delete(asignacion)
    personaje.xp += 50
    db.commit()
    return mision
