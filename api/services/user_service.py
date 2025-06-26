from sqlalchemy.orm import Session
from api.services.interfaces import IUsuarioCRUDService, IAutenticacionService
from api.repositories.user_repository import UserRepository

class UsuarioNoExisteError(Exception): pass
class UsernameYaExisteError(Exception): pass

class UserService(IUsuarioCRUDService, IAutenticacionService):
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def listar_usuarios(self, db: Session):
        return self.user_repository.obtener_usuarios(db)

    def crear_usuario(self, db: Session, username: str, password: str, role: str):
        return self.user_repository.crear(db, username, password, role)

    def editar_usuario(self, db: Session, user_id: int, username: str = None, password: str = None, role: str = None):
        return self.user_repository.actualizar(db, user_id, username, password, role)

    def eliminar_usuario(self, db: Session, user_id: int):
        return self.user_repository.eliminar(db, user_id)

    def autenticar(self, db: Session, username: str, password: str):
        return self.user_repository.autenticar(db, username, password)