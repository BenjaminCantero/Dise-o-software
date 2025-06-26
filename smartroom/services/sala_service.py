import requests
from smartroom.services.interfaces import ISalaCRUDService

class SalaService(ISalaCRUDService):
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_all(self):
        resp = requests.get(f"{self.API_URL}/salas/", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create(self, nombre, capacidad, estado):
        data = {"nombre": nombre, "capacidad": capacidad, "estado": estado}
        resp = requests.post(f"{self.API_URL}/salas/", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update(self, sala_id, nombre, capacidad, estado):
        data = {"nombre": nombre, "capacidad": capacidad, "estado": estado}
        resp = requests.put(f"{self.API_URL}/salas/{sala_id}", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete(self, sala_id):
        resp = requests.delete(f"{self.API_URL}/salas/{sala_id}", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.status_code == 204