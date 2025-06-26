# Se importa datetime para usarlo en los type hints y mejorar la claridad del código
from datetime import datetime 
from sqlalchemy.orm import Session

from api.repositories.reserva_repository import ReservaRepository
from api.repositories.user_repository import UserRepository
from api.repositories.sala_repository import SalaRepository

# --- Definición de Excepciones Personalizadas ---
class UsuarioNoExisteError(Exception):
    """Excepción lanzada cuando un usuario no se encuentra en la base de datos."""
    pass

class SalaNoExisteError(Exception):
    """Excepción lanzada cuando una sala no se encuentra en la base de datos."""
    pass

class ReservaNoExisteError(Exception):
    """Excepción lanzada cuando una reserva no se encuentra en la base de datos."""
    pass


class ReservaService:
    """
    Capa de servicio para gestionar la lógica de negocio de las reservas.
    Orquesta los repositorios y realiza validaciones antes de ejecutar
    las operaciones de base de datos.
    """
    def __init__(self, reserva_repository: ReservaRepository = None, 
                 user_repository: UserRepository = None,
                 sala_repository: SalaRepository = None):
        self.reserva_repository = reserva_repository or ReservaRepository()
        self.user_repository = user_repository or UserRepository()
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_usuario(self, db: Session, usuario_id: int):
        """Comprueba si un usuario existe, si no, lanza un error."""
        usuario = self.user_repository.obtener_usuario(db, usuario_id)
        if not usuario:
            # Mensaje de error ligeramente más descriptivo
            raise UsuarioNoExisteError(f"El usuario con ID '{usuario_id}' no existe.")
        return usuario

    def _validar_sala(self, db: Session, sala_id: int):
        """Comprueba si una sala existe, si no, lanza un error."""
        sala = self.sala_repository.obtener_sala(db, sala_id)
        if not sala:
            # Mensaje de error ligeramente más descriptivo
            raise SalaNoExisteError(f"La sala con ID '{sala_id}' no existe.")
        return sala
    
    def _validar_reserva(self, db: Session, reserva_id: int):
        """Comprueba si una reserva existe, si no, lanza un error."""
        reserva = self.reserva_repository.obtener_reserva(db, reserva_id)
        if not reserva:
            raise ReservaNoExisteError(f"La reserva con ID '{reserva_id}' no existe.")
        return reserva

    def crear_reserva(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio: datetime, fecha_fin: datetime):
        """
        Crea una nueva reserva después de validar el usuario y la sala.
        """
        self._validar_usuario(db, usuario_id)
        self._validar_sala(db, sala_id)
        
        # La validación de coherencia de fechas se realiza en el schema de Pydantic.
        # Se delega la creación al repositorio.
        return self.reserva_repository.crear_reserva(
            db=db, 
            usuario_id=usuario_id, 
            sala_id=sala_id, 
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    def editar_reserva(self, db: Session, reserva_id: int, usuario_id: int, sala_id: int, 
                       fecha_inicio: datetime = None, fecha_fin: datetime = None):
        """
        Actualiza una reserva existente tras validar que todos los
        elementos (reserva, usuario, sala) existen.
        """
        self._validar_reserva(db, reserva_id)
        self._validar_usuario(db, usuario_id)
        self._validar_sala(db, sala_id)
        
        return self.reserva_repository.actualizar_reserva(
            db, reserva_id, usuario_id, sala_id, fecha_inicio, fecha_fin
        )

    def listar_reservas(self, db):
        """
        Devuelve todas las reservas.
        """
        return self.reserva_repository.listar_reservas(db)
