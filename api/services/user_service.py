from sqlalchemy.orm import Session
from api.repositories.user_repository import UserRepository

class UsuarioNoExisteError(Exception): pass
class UsernameYaExisteError(Exception): pass

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def _validar_usuario(self, db, usuario_id):
        usuario = self.user_repository.obtener(db, usuario_id)
        if not usuario:
            raise UsuarioNoExisteError(f"Usuario con id {usuario_id} no existe")
        return usuario

    def _validar_username_unico(self, db, username):
        usuario = self.user_repository.buscar_usuario_por_username(db, username)
        if usuario:
            raise UsernameYaExisteError(f"El username '{username}' ya está en uso")

    def autenticar(self, db: Session, username: str, password: str):
        usuario = self.user_repository.buscar_usuario_por_username(db, username)
        if usuario and usuario.password == password:
            return usuario
        return None

    def listar_usuarios(self, db: Session):
        return self.user_repository.obtener_usuarios(db)

    def crear_usuario(self, db: Session, username: str, password: str, role: str):
        self._validar_username_unico(db, username)
        return self.user_repository.crear(db, username, password, role)

    def eliminar_usuario(self, db: Session, usuario_id: int):
        self._validar_usuario(db, usuario_id)
        return self.user_repository.eliminar(db, usuario_id)