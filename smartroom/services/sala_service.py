import requests
from typing import Any, Dict, List
from smartroom.services.interfaces import ISalaCRUDService

class SalaService(ISalaCRUDService):
    """
    Servicio para gestionar salas a través de la API REST.
    Implementa la interfaz ISalaCRUDService siguiendo el principio SOLID ISP.
    """

    API_URL = "http://127.0.0.1:8000"  # URL base de la API
    HEADERS = {"Authorization": "Bearer secrettoken"}  # Encabezados para autenticación

    def get_salas(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de salas desde la API.
        :return: Lista de diccionarios con la información de cada sala.
        """
        url = f"{self.API_URL}/salas/"
        resp = requests.get(url, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create_sala(self, nombre: str, capacidad: int, estado: str) -> Dict[str, Any]:
        """
        Crea una nueva sala en la API.
        :param nombre: Nombre de la sala.
        :param capacidad: Capacidad de la sala.
        :param estado: Estado de la sala.
        :return: Diccionario con la sala creada.
        """
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
        """
        Actualiza una sala existente en la API.
        :param sala_id: ID de la sala a actualizar.
        :param nombre: Nuevo nombre.
        :param capacidad: Nueva capacidad.
        :param estado: Nuevo estado.
        :return: Diccionario con la sala actualizada.
        """
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
        """
        Elimina una sala de la API.
        :param sala_id: ID de la sala a eliminar.
        :return: Diccionario con la respuesta de la API.
        """
        url = f"{self.API_URL}/salas/{sala_id}"
        resp = requests.delete(url, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()