from datetime import datetime
from sqlalchemy.orm import Session

from api.services.interfaces import IReservaCRUDService
from api.repositories.reserva_repository import ReservaRepository
from api.repositories.user_repository import UserRepository
from api.repositories.sala_repository import SalaRepository

class UsuarioNoExisteError(Exception): pass
class SalaNoExisteError(Exception): pass
class ReservaNoExisteError(Exception): pass

class ReservaService(IReservaCRUDService):
    """
    Servicio para la gestión de reservas en SmartRoom API.
    Permite listar, crear, editar y eliminar reservas, validando la existencia de usuario y sala.
    """
    def __init__(self, reserva_repository=None, user_repository=None, sala_repository=None):
        self.reserva_repository = reserva_repository or ReservaRepository()
        self.user_repository = user_repository or UserRepository()
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_usuario(self, db, usuario_id):
        """Valida que el usuario exista."""
        usuario = self.user_repository.obtener(db, usuario_id)
        if not usuario:
            raise UsuarioNoExisteError(f"Usuario con id {usuario_id} no existe")
        return usuario

    def _validar_sala(self, db, sala_id):
        """Valida que la sala exista."""
        sala = self.sala_repository.obtener(db, sala_id)
        if not sala:
            raise SalaNoExisteError(f"Sala con id {sala_id} no existe")
        return sala

    def _validar_reserva(self, db, reserva_id):
        """Valida que la reserva exista."""
        reserva = self.reserva_repository.obtener(db, reserva_id)
        if not reserva:
            raise ReservaNoExisteError(f"Reserva con id {reserva_id} no existe")
        return reserva

    def listar_reservas(self, db: Session):
        """Obtiene la lista de todas las reservas."""
        return self.reserva_repository.listar_reservas(db)

    def crear_reserva(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio: datetime, fecha_fin: datetime):
        """Crea una nueva reserva validando usuario y sala."""
        self._validar_usuario(db, usuario_id)
        self._validar_sala(db, sala_id)
        return self.reserva_repository.crear(db, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def editar_reserva(self, db: Session, reserva_id: int, usuario_id=None, sala_id=None, fecha_inicio=None, fecha_fin=None):
        """Edita una reserva existente."""
        self._validar_reserva(db, reserva_id)
        return self.reserva_repository.actualizar(db, reserva_id, usuario_id, sala_id, fecha_inicio, fecha_fin)

    def eliminar_reserva(self, db: Session, reserva_id: int):
        """Elimina una reserva por su ID."""
        self._validar_reserva(db, reserva_id)
        return self.reserva_repository.eliminar(db, reserva_id)

    def obtener_reserva_por_id(self, db: Session, reserva_id: int):
        """Obtiene una reserva por su ID."""
        return self.reserva_repository.obtener(db, reserva_id)