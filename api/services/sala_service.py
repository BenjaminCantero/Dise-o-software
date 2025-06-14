# services/sala_service.py
from api.db import SessionLocal
from models.models import Sala, Reserva
from smartroom.core.observable import Observable
from smartroom.core.singleton import SingletonMeta  # <--- IMPORTADO para Singleton
from smartroom.builders.sala_builder import SalaBuilder
from sqlalchemy.orm import joinedload

class SalaService(Observable, metaclass=SingletonMeta): # <--- METACLASE AÑADIDA para Singleton
    def __init__(self):
        super().__init__() # Inicialización de Observable

    def listar_salas(self):
        db = SessionLocal()
        salas_db = db.query(Sala).all()
        salas = [
            {"id": s.id, "nombre": s.nombre, "capacidad": s.capacidad, "estado": s.estado}
            for s in salas_db
        ]
        db.close()
        return salas

    def crear_sala(self, nombre, capacidad, estado="disponible"):
        db = SessionLocal()
        nueva_sala = (
            SalaBuilder()
                .set_nombre(nombre)
                .set_capacidad(capacidad)
                .set_estado(estado)
                .build()
        )
        db.add(nueva_sala)
        db.commit()
        db.refresh(nueva_sala)
        db.close()
        self.notify_observers(event="sala_creada", data=nueva_sala)
        return nueva_sala

    def editar_sala(self, sala_id, nombre, capacidad, estado):
        db = SessionLocal()
        sala = db.query(Sala).filter_by(id=sala_id).first()
        if sala:
            sala.nombre = nombre
            sala.capacidad = capacidad
            sala.estado = estado
            db.commit()
            self.notify_observers(event="sala_editada", data=sala)
        db.close()

    def eliminar_sala(self, sala_id):
        db = SessionLocal()
        # Elimina primero las reservas asociadas a la sala
        reservas = db.query(Reserva).filter_by(sala_id=sala_id).all()
        for reserva in reservas:
            db.delete(reserva)
        db.commit()
        # Ahora elimina la sala
        sala = db.query(Sala).filter_by(id=sala_id).first()
        if sala:
            db.delete(sala)
            db.commit()
            self.notify_observers(event="sala_eliminada", data=sala_id)
        db.close()

    def obtener_sala_por_id(self, sala_id: int):
        db = SessionLocal()
        try:
            sala = db.query(Sala).filter(Sala.id == sala_id).first()
            return sala
        finally:
            db.close()