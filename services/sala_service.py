from core.observable import Observable
import tkinter.ttk as ttk

class SalaService(Observable):
    def __init__(self):
        super().__init__()
        # Aquí puedes inicializar una lista de salas o conectar con el repositorio
        self.salas = []

    def listar_salas(self):
        return self.salas

    def crear_sala(self, nombre, capacidad, estado="disponible"):
        sala = {
            "id": len(self.salas) + 1,
            "nombre": nombre,
            "capacidad": capacidad,
            "estado": estado
        }
        self.salas.append(sala)
        return sala

    def eliminar_sala(self, sala_id):
        self.salas = [s for s in self.salas if s["id"] != sala_id]

    def contar_salas(self):
        return len(self.salas)

    def contar_ocupadas(self):
        return len([s for s in self.salas if s["estado"] == "ocupada"])

    def contar_disponibles(self):
        return len([s for s in self.salas if s["estado"] == "disponible"])

class DashboardPanel(ttk.Frame):
    def __init__(self, parent, sala_service):
        super().__init__(parent)
        self.sala_service = sala_service
        # ...