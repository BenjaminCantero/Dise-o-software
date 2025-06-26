from datetime import datetime
from sqlalchemy.orm import Session

from api.repositories.reserva_repository import ReservaRepository
from api.repositories.user_repository import UserRepository
from api.repositories.sala_repository import SalaRepository

class UsuarioNoExisteError(Exception): pass
class SalaNoExisteError(Exception): pass
class ReservaNoExisteError(Exception): pass

class ReservaService:
    def __init__(self, reserva_repository=None, user_repository=None, sala_repository=None):
        self.reserva_repository = reserva_repository or ReservaRepository()
        self.user_repository = user_repository or UserRepository()
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_usuario(self, db, usuario_id):
        usuario = self.user_repository.obtener(db, usuario_id)
        if not usuario:
            raise UsuarioNoExisteError(f"Usuario con id {usuario_id} no existe")
        return usuario

    def _validar_sala(self, db, sala_id):
        sala = self.sala_repository.obtener(db, sala_id)
        if not sala:
            raise SalaNoExisteError(f"Sala con id {sala_id} no existe")
        return sala

    def _validar_reserva(self, db, reserva_id):
        reserva = self.reserva_repository.obtener(db, reserva_id)
        if not reserva:
            raise ReservaNoExisteError(f"Reserva con id {reserva_id} no existe")
        return reserva

    def listar_reservas(self, db: Session):
        return self.reserva_repository.listar_reservas(db)

    def crear_reserva(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio: datetime, fecha_fin: datetime):
        self._validar_usuario(db, usuario_id)
        self._validar_sala(db, sala_id)
        return self.reserva_repository.crear(db, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def editar_reserva(self, db: Session, reserva_id: int, usuario_id=None, sala_id=None, fecha_inicio=None, fecha_fin=None):
        self._validar_reserva(db, reserva_id)
        return self.reserva_repository.actualizar(db, reserva_id, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def eliminar_reserva(self, db: Session, reserva_id: int):
        self._validar_reserva(db, reserva_id)
        return self.reserva_repository.eliminar(db, reserva_id)

    def obtener_reserva_por_id(self, db: Session, reserva_id: int):
        return self.reserva_repository.obtener(db, reserva_id)