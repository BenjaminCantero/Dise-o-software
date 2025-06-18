from sqlalchemy.orm import Session
from api.repositories.sala_repository import SalaRepository

class SalaService:
    def __init__(self, sala_repository=None):
        self.sala_repository = sala_repository or SalaRepository()

    def listar_salas(self, db: Session):
        return self.sala_repository.obtener_salas(db)

    def crear_sala(self, db: Session, nombre: str, capacidad: int, estado: str = "disponible"):
        return self.sala_repository.crear_sala(db, nombre, capacidad, estado)

    def editar_sala(self, db: Session, sala_id: int, nombre: str = None, capacidad: int = None, estado: str = None):
        return self.sala_repository.actualizar_sala(db, sala_id, nombre, capacidad, estado)

    def eliminar_sala(self, db: Session, sala_id: int):
        return self.sala_repository.eliminar_sala(db, sala_id)

    def obtener_sala_por_id(self, db: Session, sala_id: int):
        return self.sala_repository.obtener_sala(db, sala_id)