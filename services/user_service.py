class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService:
    def __init__(self):
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