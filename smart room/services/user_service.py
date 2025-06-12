import requests
from core.observable import Observable
from core.singleton import SingletonMeta

API_URL = "http://127.0.0.1:8000/usuarios/"

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService(Observable, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

    def autenticar(self, username, password):
        data = {"username": username, "password": password}
        response = requests.post("http://127.0.0.1:8000/usuarios/login", json=data)
        if response.status_code == 200:
            user_data = response.json()
            return User(user_data["username"], user_data["role"])
        return None

    def listar_usuarios(self):
        response = requests.get(API_URL)
        response.raise_for_status()
        usuarios_data = response.json()
        # Si la API no devuelve la contraseña, solo devuelve username y role
        return [User(u["username"], u["role"]) for u in usuarios_data]

    def crear_usuario(self, username, password, role):
        data = {
            "username": username,
            "password": password,
            "role": role
        }
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        nuevo_usuario = response.json()
        self.notify_observers(event="usuario_creado", data=nuevo_usuario)
        return nuevo_usuario

    def eliminar_usuario(self, username):
        # Busca el usuario por nombre para obtener su id
        usuarios = self.listar_usuarios()
        usuario = next((u for u in usuarios if u.username == username), None)
        if usuario:
            # Supón que la API elimina por id
            response = requests.delete(f"{API_URL}{usuario.id}")
            response.raise_for_status()
            self.notify_observers(event="usuario_eliminado", data=username)

    def editar_usuario(self, username, role):
        # Busca el usuario por nombre para obtener su id
        usuarios = self.listar_usuarios()
        usuario = next((u for u in usuarios if u.username == username), None)
        if usuario:
            data = {
                "username": username,
                "password": "",  # Si la API requiere password, deberías pedirlo o dejar el actual
                "role": role
            }
            response = requests.put(f"{API_URL}{usuario.id}", json=data)
            response.raise_for_status()
            self.notify_observers(event="usuario_editado", data={"username": username, "role": role})