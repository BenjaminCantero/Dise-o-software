import requests
from smartroom.services.base_api_service import BaseApiService
from smartroom.services.interfaces import ISalaCRUDService

class SalaService(BaseApiService, ISalaCRUDService):
    """
    Facade para la gestión de salas vía API REST.
    Expone una interfaz simple y maneja internamente las llamadas HTTP y los errores.
    """

    def get_all(self):
        try:
            resp = requests.get(f"{self.API_URL}/salas/", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al obtener salas: {e}")

    def create(self, nombre, capacidad, estado):
        try:
            data = {"nombre": nombre, "capacidad": capacidad, "estado": estado}
            resp = requests.post(f"{self.API_URL}/salas/", json=data, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al crear sala: {e}")

    def update(self, sala_id, nombre, capacidad, estado):
        try:
            data = {"nombre": nombre, "capacidad": capacidad, "estado": estado}
            resp = requests.put(f"{self.API_URL}/salas/{sala_id}", json=data, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al actualizar sala: {e}")

    def delete(self, sala_id):
        try:
            resp = requests.delete(f"{self.API_URL}/salas/{sala_id}", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.status_code == 204
        except requests.RequestException as e:
            raise Exception(f"Error al eliminar sala: {e}")