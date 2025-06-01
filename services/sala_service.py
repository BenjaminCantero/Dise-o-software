# services/sala_service.py
from repositories.db import SessionLocal
from repositories.models import Sala
from core.observable import Observable
from core.singleton import SingletonMeta # <--- IMPORTADO para Singleton

class SalaService(Observable, metaclass=SingletonMeta): # <--- METACLASE AÑADIDA para Singleton
    def __init__(self):
        super().__init__() # Inicialización de Observable
        print("SalaService Singleton Inicializado") # Demuestra que __init__ se llama una vez

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
        nueva_sala = Sala(nombre=nombre, capacidad=capacidad, estado=estado)
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
        sala = db.query(Sala).filter_by(id=sala_id).first()
        if sala:
            db.delete(sala)
            db.commit()
            self.notify_observers(event="sala_eliminada", data=sala_id)
        db.close()
