from sqlalchemy.orm import Session
from api.models import Sala

def crear_sala(db: Session, nombre: str, capacidad: int):
    sala = Sala(nombre=nombre, capacidad=capacidad)
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala

def obtener_sala(db: Session, sala_id: int):
    return db.query(Sala).filter(Sala.id == sala_id).first()

def obtener_salas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sala).offset(skip).limit(limit).all()

def actualizar_sala(db: Session, sala_id: int, nombre: str = None, capacidad: int = None):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if sala:
        if nombre:
            sala.nombre = nombre
        if capacidad is not None:
            sala.capacidad = capacidad
        db.commit()
        db.refresh(sala)
    return sala

def eliminar_sala(db: Session, sala_id: int):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if sala:
        db.delete(sala)
        db.commit()
    return sala