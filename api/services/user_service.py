from sqlalchemy.orm import Session
from api.services.interfaces import IUsuarioCRUDService, IAutenticacionService
from api.repositories.user_repository import UserRepository

class UsuarioNoExisteError(Exception): pass
class UsernameYaExisteError(Exception): pass

class UserService(IUsuarioCRUDService, IAutenticacionService):
    """
    Servicio para la gestión de usuarios en SmartRoom API.
    Permite listar, crear, editar, eliminar y autenticar usuarios usando un repositorio.
    """
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def listar_usuarios(self, db: Session):
        """Obtiene la lista de todos los usuarios."""
        return self.user_repository.obtener_usuarios(db)

    def crear_usuario(self, db: Session, username: str, password: str, role: str):
        """Crea un nuevo usuario con username, password y rol."""
        return self.user_repository.crear(db, username, password, role)

    def editar_usuario(self, db: Session, user_id: int, username: str = None, password: str = None, role: str = None):
        """Edita los datos de un usuario existente."""
        return self.user_repository.actualizar(db, user_id, username, password, role)

    def eliminar_usuario(self, db: Session, user_id: int):
        """Elimina un usuario por su ID."""
        return self.user_repository.eliminar(db, user_id)

    def autenticar(self, db: Session, username: str, password: str):
        """Autentica un usuario por username y password."""
        return self.user_repository.autenticar(db, username, password)