import requests
from typing import Any, Dict, List
from smartroom.services.interfaces import ISalaCRUDService

class SalaService(ISalaCRUDService):
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_salas(self) -> List[Dict[str, Any]]:
        url = f"{self.API_URL}/salas/"
        resp = requests.get(url, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create_sala(self, nombre: str, capacidad: int, estado: str) -> Dict[str, Any]:
        url = f"{self.API_URL}/salas/"
        data = {
            "nombre": nombre,
            "capacidad": capacidad,
            "estado": estado
        }
        resp = requests.post(url, json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update_sala(self, sala_id: int, nombre: str, capacidad: int, estado: str) -> Dict[str, Any]:
        url = f"{self.API_URL}/salas/{sala_id}"
        data = {
            "nombre": nombre,
            "capacidad": capacidad,
            "estado": estado
        }
        resp = requests.put(url, json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete_sala(self, sala_id: int) -> Dict[str, Any]:
        url = f"{self.API_URL}/salas/{sala_id}"
        resp = requests.delete(url, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()