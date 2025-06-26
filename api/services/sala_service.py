from sqlalchemy.orm import Session
from api.repositories.sala_repository import SalaRepository
from api.services.interfaces import ISalaCRUDService

class SalaNoExisteError(Exception): pass
class NombreSalaYaExisteError(Exception): pass

class SalaService(ISalaCRUDService):
    def __init__(self, sala_repository=None):
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_sala(self, db, sala_id):
        sala = self.sala_repository.obtener(db, sala_id)
        if not sala:
            raise SalaNoExisteError(f"Sala con id {sala_id} no existe")
        return sala

    def _validar_nombre_unico(self, db, nombre):
        salas = self.sala_repository.obtener_salas(db)
        if any(sala.nombre == nombre for sala in salas):
            raise NombreSalaYaExisteError(f"El nombre '{nombre}' ya está en uso")

    def listar_salas(self, db: Session):
        return self.sala_repository.obtener_salas(db)

    def crear_sala(self, db: Session, nombre: str, capacidad: int, estado: str = "disponible"):
        self._validar_nombre_unico(db, nombre)
        return self.sala_repository.crear(db, nombre, capacidad, estado)

    def editar_sala(self, db: Session, sala_id: int, nombre: str = None, capacidad: int = None, estado: str = None):
        self._validar_sala(db, sala_id)
        return self.sala_repository.actualizar(db, sala_id, nombre, capacidad, estado)

    def eliminar_sala(self, db: Session, sala_id: int):
        self._validar_sala(db, sala_id)
        return self.sala_repository.eliminar(db, sala_id)