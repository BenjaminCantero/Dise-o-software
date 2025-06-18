from sqlalchemy.orm import Session
from api.repositories.reserva_repository import ReservaRepository

class ReservaService:
    def __init__(self, reserva_repository=None):
        self.reserva_repository = reserva_repository or ReservaRepository()

    def listar_reservas(self, db: Session):
        return self.reserva_repository.obtener_reservas(db)

    def crear_reserva(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio, fecha_fin):
        return self.reserva_repository.crear_reserva(db, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def eliminar_reserva(self, db: Session, reserva_id: int):
        return self.reserva_repository.eliminar_reserva(db, reserva_id)

    def editar_reserva(self, db: Session, reserva_id: int, fecha_inicio=None, fecha_fin=None):
        return self.reserva_repository.actualizar_reserva(db, reserva_id, fecha_inicio, fecha_fin)

    def obtener_reserva_por_id(self, db: Session, reserva_id: int):
        return self.reserva_repository.obtener_reserva(db, reserva_id)

    def obtener_reservas_por_usuario(self, db: Session, usuario_id: int):
        return self.reserva_repository.obtener_reservas_por_usuario(db, usuario_id)

    def eliminar_reservas_por_usuario(self, db: Session, usuario_id: int):
        reservas = self.obtener_reservas_por_usuario(db, usuario_id)
        for reserva in reservas:
            self.eliminar_reserva(db, reserva.id)