from repositories import reserva_repository
from repositories.db import SessionLocal

class ReservaService:
    def __init__(self):
        self.db = SessionLocal()

    def listar_reservas(self):
        return reserva_repository.obtener_reservas(self.db)

    def crear_reserva(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        return reserva_repository.crear_reserva(self.db, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def eliminar_reserva(self, reserva_id):
        reserva_repository.eliminar_reserva(self.db, reserva_id)

    def buscar_reservas_por_usuario(self, usuario_id):
        return reserva_repository.buscar_reservas_por_usuario(self.db, usuario_id)