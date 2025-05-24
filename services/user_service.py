from core.observable import Observable

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService(Observable):
    def __init__(self):
        super().__init__()
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
        return [User(username, data["role"]) for username, data in self.usuarios.items()]

    # Métodos para observer
    def crear_usuario(self, username, password, role):
        if username not in self.usuarios:
            self.usuarios[username] = {"password": password, "role": role}
            self.notify_observers(event="usuario_creado", data=username)

    def eliminar_usuario(self, username):
        if username in self.usuarios:
            del self.usuarios[username]
            self.notify_observers(event="usuario_eliminado", data=username)

    def editar_usuario(self, username, password=None, role=None):
        if username in self.usuarios:
            if password:
                self.usuarios[username]["password"] = password
            if role:
                self.usuarios[username]["role"] = role
            self.notify_observers(event="usuario_editado", data=username)