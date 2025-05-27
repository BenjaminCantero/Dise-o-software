from repositories.db import SessionLocal
from repositories.models import Sala
from core.observable import Observable
import tkinter.ttk as ttk

class SalaService(Observable):
    def __init__(self):
        super().__init__()

    def listar_salas(self):
        db = SessionLocal()
        salas_db = db.query(Sala).all()
        salas = [
            {"id": s.id, "nombre": s.nombre, "capacidad": s.capacidad, "estado": s.estado}
            for s in salas_db
        ]
        db.close()
        return salas

    def crear_sala(self, nombre, capacidad):
        db = SessionLocal()
        nueva_sala = Sala(nombre=nombre, capacidad=capacidad, estado="disponible")
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

class DashboardPanel(ttk.Frame):
    def __init__(self, parent, sala_service):
        super().__init__(parent)
        self.sala_service = sala_service
        # ...