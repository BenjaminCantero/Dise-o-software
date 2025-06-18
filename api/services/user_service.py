from sqlalchemy.orm import Session
from api.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def autenticar(self, db: Session, username: str, password: str):
        usuario = self.user_repository.buscar_usuario_por_username(db, username)
        if usuario and usuario.password == password:
            return usuario
        return None

    def listar_usuarios(self, db: Session):
        return self.user_repository.obtener_usuarios(db)

    def crear_usuario(self, db: Session, username: str, password: str, role: str):
        return self.user_repository.crear_usuario(db, username, password, role)

    def eliminar_usuario(self, db: Session, usuario_id: int):
        return self.user_repository.eliminar_usuario(db, usuario_id)

    def editar_usuario(self, db: Session, usuario_id: int, username: str = None, password: str = None):
        return self.user_repository.actualizar_usuario(db, usuario_id, username, password)