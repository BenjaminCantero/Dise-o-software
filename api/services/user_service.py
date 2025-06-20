from sqlalchemy.orm import Session
from api.repositories.user_repository import UserRepository

class UsuarioNoExisteError(Exception): pass
class UsernameYaExisteError(Exception): pass

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def _validar_usuario(self, db, usuario_id):
        usuario = self.user_repository.obtener_usuario(db, usuario_id)
        if not usuario:
            raise UsuarioNoExisteError("El usuario no existe.")
        return usuario

    def _validar_username_unico(self, db, username):
        usuario = self.user_repository.buscar_usuario_por_username(db, username)
        if usuario:
            raise UsernameYaExisteError("El nombre de usuario ya está en uso.")
        return True

    def autenticar(self, db: Session, username: str, password: str):
        usuario = self.user_repository.buscar_usuario_por_username(db, username)
        if usuario and usuario.password == password:
            return usuario
        return None

    def listar_usuarios(self, db: Session):
        return self.user_repository.obtener_usuarios(db)

    def crear_usuario(self, db: Session, username: str, password: str, role: str):
        self._validar_username_unico(db, username)
        return self.user_repository.crear_usuario(db, username, password, role)

    def eliminar_usuario(self, db: Session, usuario_id: int):
        self._validar_usuario(db, usuario_id)
        return self.user_repository.eliminar_usuario(db, usuario_id)

    def editar_usuario(self, db: Session, usuario_id: int, username: str = None, password: str = None, role: str = None):
        self._validar_usuario(db, usuario_id)
        if username:
            self._validar_username_unico(db, username)
        return self.user_repository.actualizar_usuario(db, usuario_id, username, password, role)