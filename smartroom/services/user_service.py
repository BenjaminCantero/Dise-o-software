import requests
from smartroom.services.base_api_service import BaseApiService
from smartroom.services.interfaces import IAutenticacionService, IUsuarioCRUDService
from smartroom.decorators.notificacion_reserva import (
    ComponenteConcreto,
    DecoradorLogging,
    DecoradorValidacion,
    DecoradorAuditoria,
    DecoradorNotificacion
)

class UserService(BaseApiService, IAutenticacionService, IUsuarioCRUDService):
    """
    Facade para la gestión de usuarios vía API REST.
    Expone una interfaz simple y maneja internamente las llamadas HTTP y los errores.
    """
    def get_all(self):
        try:
            resp = requests.get(f"{self.API_URL}/usuarios/", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al obtener usuarios: {e}")

    def create(self, username, password, role):
        try:
            datos = {
                "usuario": username,
                "accion": "crear_usuario",
                "detalle": {"role": role}
            }
            componente = ComponenteConcreto()
            componente = DecoradorLogging(componente)
            componente = DecoradorValidacion(componente)
            componente = DecoradorAuditoria(componente)
            componente = DecoradorNotificacion(componente)
            componente.operacion(datos)

            data = {"username": username, "password": password, "role": role}
            resp = requests.post(f"{self.API_URL}/usuarios/", json=data, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al crear usuario: {e}")

    def update(self, user_id, username, role):
        try:
            data = {"username": username, "role": role}
            resp = requests.put(f"{self.API_URL}/usuarios/{user_id}", json=data, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al actualizar usuario: {e}")

    def delete(self, user_id):
        try:
            resp = requests.delete(f"{self.API_URL}/usuarios/{user_id}", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.status_code == 204
        except requests.RequestException as e:
            raise Exception(f"Error al eliminar usuario: {e}")

    def autenticar(self, username, password):
        try:
            data = {"username": username, "password": password}
            resp = requests.post(f"{self.API_URL}/login", json=data, headers=self.HEADERS)
            if resp.status_code == 200:
                return resp.json()
            return None
        except requests.RequestException as e:
            raise Exception(f"Error de autenticación: {e}")