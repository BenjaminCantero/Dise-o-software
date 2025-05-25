from core.observable import Observable
from repositories import sala_repository
from repositories.db import SessionLocal
import tkinter.ttk as ttk

class SalaService(Observable):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()

    def listar_salas(self):
        return sala_repository.obtener_salas(self.db)

    def crear_sala(self, nombre, capacidad, estado="disponible"):
        sala = sala_repository.crear_sala(self.db, nombre, capacidad)
        self.notify_observers(event="sala_creada", data=sala)
        return sala

    def eliminar_sala(self, sala_id):
        sala_repository.eliminar_sala(self.db, sala_id)
        self.notify_observers(event="sala_eliminada", data=sala_id)

    def contar_salas(self):
        return len(self.listar_salas())

    def contar_ocupadas(self):
        return len([s for s in self.listar_salas() if getattr(s, "estado", "disponible") == "ocupada"])

    def contar_disponibles(self):
        return len([s for s in self.listar_salas() if getattr(s, "estado", "disponible") == "disponible"])

class DashboardPanel(ttk.Frame):
    def __init__(self, parent, sala_service):
        super().__init__(parent)
        self.sala_service = sala_service
        # ...