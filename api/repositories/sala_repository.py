from sqlalchemy.orm import Session
from api.models.sala import Sala
from .base_repository import BaseRepository

class SalaRepository(BaseRepository):
    def crear(self, db: Session, nombre: str, capacidad: int, estado: str = "disponible"):
        sala = Sala(nombre=nombre, capacidad=capacidad, estado=estado)
        db.add(sala)
        db.commit()
        db.refresh(sala)
        return sala

    def obtener(self, db: Session, sala_id: int):
        return db.query(Sala).filter(Sala.id == sala_id).first()

    def actualizar(self, db: Session, sala_id: int, nombre: str = None, capacidad: int = None, estado: str = None):
        sala = db.query(Sala).filter(Sala.id == sala_id).first()
        if sala:
            if nombre is not None:
                sala.nombre = nombre
            if capacidad is not None:
                sala.capacidad = capacidad
            if estado is not None:
                sala.estado = estado
            db.commit()
            db.refresh(sala)
        return sala

    def eliminar(self, db: Session, sala_id: int):
        sala = db.query(Sala).filter(Sala.id == sala_id).first()
        if sala:
            db.delete(sala)
            db.commit()
        return sala

    # Métodos adicionales específicos
    def obtener_salas(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Sala).offset(skip).limit(limit).all()