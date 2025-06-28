from sqlalchemy.orm import Session
from api.repositories.sala_repository import SalaRepository
from api.services.interfaces import ISalaCRUDService

class SalaNoExisteError(Exception): pass
class NombreSalaYaExisteError(Exception): pass

class SalaService(ISalaCRUDService):
    """
    Servicio para la gestión de salas en SmartRoom API.
    Permite listar, crear, editar y eliminar salas, validando unicidad de nombre y existencia.
    """
    def __init__(self, sala_repository=None):
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_sala(self, db, sala_id):
        """Valida que la sala exista."""
        sala = self.sala_repository.obtener(db, sala_id)
        if not sala:
            raise SalaNoExisteError(f"Sala con id {sala_id} no existe")
        return sala

    def _validar_nombre_unico(self, db, nombre):
        """Valida que el nombre de la sala sea único."""
        salas = self.sala_repository.obtener_salas(db)
        if any(sala.nombre == nombre for sala in salas):
            raise NombreSalaYaExisteError(f"El nombre '{nombre}' ya está en uso")

    def listar_salas(self, db: Session):
        """Obtiene la lista de todas las salas."""
        return self.sala_repository.obtener_salas(db)

    def crear_sala(self, db: Session, nombre: str, capacidad: int, estado: str = "disponible"):
        """Crea una nueva sala validando unicidad de nombre."""
        if self.sala_repository.existe_nombre(db, nombre):
            raise NombreSalaYaExisteError("El nombre ya está en uso")
        return self.sala_repository.crear(db, nombre, capacidad, estado)

    def editar_sala(self, db: Session, sala_id: int, nombre: str = None, capacidad: int = None, estado: str = None):
        """Edita los datos de una sala existente."""
        self._validar_sala(db, sala_id)
        return self.sala_repository.actualizar(db, sala_id, nombre, capacidad, estado)

    def eliminar_sala(self, db: Session, sala_id: int):
        """Elimina una sala por su ID."""
        self._validar_sala(db, sala_id)
        return self.sala_repository.eliminar(db, sala_id)