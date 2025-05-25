from core.observable import Observable
from repositories import user_repository
from repositories.db import SessionLocal

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService(Observable):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        # Usuarios de ejemplo
        self.usuarios = {
            "admin": {"password": "admin123", "role": "admin"},
            "profesor": {"password": "prof123", "role": "profesor"},
            "estudiante": {"password": "estu123", "role": "estudiante"},
        }

    def autenticar(self, username, password):
        user = self.usuarios.get(username)
        if user and user["password"] == password:
            return User(username, user["role"])
        return None

    def listar_usuarios(self):
        return user_repository.obtener_usuarios(self.db)

    def crear_usuario(self, nombre, email, password):
        return user_repository.crear_usuario(self.db, nombre, email, password)

    def eliminar_usuario(self, user_id):
        user_repository.eliminar_usuario(self.db, user_id)

    def buscar_usuario_por_email(self, email):
        return user_repository.buscar_usuario_por_email(self.db, email)

    # Métodos para observer
    def crear_usuario_observer(self, username, role):
        self.usuarios[username] = {"password": "default123", "role": role}
        nuevo_usuario = User(username=username, role=role)
        self.notify_observers(event="usuario_creado", data=nuevo_usuario)
        return nuevo_usuario

    def eliminar_usuario_observer(self, username):
        if username in self.usuarios:
            del self.usuarios[username]
            self.notify_observers(event="usuario_eliminado", data=username)

    def editar_usuario_observer(self, username, password=None, role=None):
        if username in self.usuarios:
            if password:
                self.usuarios[username]["password"] = password
            if role:
                self.usuarios[username]["role"] = role
            self.notify_observers(event="usuario_editado", data=username)