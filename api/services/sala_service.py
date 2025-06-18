from sqlalchemy.orm import Session
from api.repositories.sala_repository import SalaRepository

class SalaNoExisteError(Exception): pass
class NombreSalaYaExisteError(Exception): pass

class SalaService:
    def __init__(self, sala_repository=None):
        self.sala_repository = sala_repository or SalaRepository()

    def _validar_sala(self, db, sala_id):
        sala = self.sala_repository.obtener_sala(db, sala_id)
        if not sala:
            raise SalaNoExisteError("La sala no existe.")
        return sala

    def _validar_nombre_unico(self, db, nombre):
        salas = self.sala_repository.obtener_salas(db)
        if any(s.nombre == nombre for s in salas):
            raise NombreSalaYaExisteError("El nombre de la sala ya está en uso.")
        return True

    def listar_salas(self, db: Session):
        return self.sala_repository.obtener_salas(db)

    def crear_sala(self, db: Session, nombre: str, capacidad: int, estado: str = "disponible"):
        self._validar_nombre_unico(db, nombre)
        return self.sala_repository.crear_sala(db, nombre, capacidad, estado)

    def editar_sala(self, db: Session, sala_id: int, nombre: str = None, capacidad: int = None, estado: str = None):
        self._validar_sala(db, sala_id)
        if nombre:
            self._validar_nombre_unico(db, nombre)
        return self.sala_repository.actualizar_sala(db, sala_id, nombre, capacidad, estado)

    def eliminar_sala(self, db: Session, sala_id: int):
        self._validar_sala(db, sala_id)
        return self.sala_repository.eliminar_sala(db, sala_id)

    def obtener_sala_por_id(self, db: Session, sala_id: int):
        return self.sala_repository.obtener_sala(db, sala_id)