import requests
from requests.exceptions import HTTPError
from typing import Any, Dict, List

class ReservaService:
    """
    Cliente de servicio para interactuar con la API de Reservas.
    
    Esta clase encapsula las llamadas HTTP (GET, POST, PUT, DELETE)
    al backend para gestionar las reservas, manejando la comunicación
    y la estructura de los datos.
    """
    
    # URL base de la API y encabezados de autenticación
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_reservas(self) -> List[Dict[str, Any]]:
        """
        Obtiene una lista de todas las reservas desde la API.

        Returns:
            Una lista de diccionarios, donde cada uno representa una reserva.

        Raises:
            HTTPError: Si la respuesta de la API tiene un código de estado de error (4xx o 5xx).
        """
        url = f"{self.API_URL}/reservas/"
        resp = requests.get(url, headers=self.HEADERS)
        # Lanza una excepción si la petición no fue exitosa (código 4xx o 5xx)
        resp.raise_for_status()
        return resp.json()

    def create_reserva(self, usuario_id: int, sala_id: int, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """
        Envía una petición para crear una nueva reserva.

        Args:
            usuario_id: El ID del usuario que hace la reserva.
            sala_id: El ID de la sala a reservar.
            fecha_inicio: La fecha y hora de inicio en formato ISO (ej. "2025-06-20T10:00:00").
            fecha_fin: La fecha y hora de fin en formato ISO.

        Returns:
            La lista actualizada de todas las reservas después de la creación.

        Raises:
            HTTPError: Si la API retorna un error durante la creación.
        """
        url = f"{self.API_URL}/reservas/"
        data = {
            "usuario_id": usuario_id,
            "sala_id": sala_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        resp = requests.post(url, json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update_reserva(self, reserva_id: int, usuario_id: int, sala_id: int, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """
        Actualiza una reserva existente a través de la API.

        Args:
            reserva_id: El ID de la reserva a modificar.
            usuario_id: El nuevo ID de usuario para la reserva.
            sala_id: El nuevo ID de sala para la reserva.
            fecha_inicio: La nueva fecha y hora de inicio en formato ISO.
            fecha_fin: La nueva fecha y hora de fin en formato ISO.

        Returns:
            La lista actualizada de todas las reservas después de la modificación.

        Raises:
            HTTPError: Si la API retorna un error durante la actualización.
        """
        url = f"{self.API_URL}/reservas/{reserva_id}"
        data = {
            "usuario_id": usuario_id,
            "sala_id": sala_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        resp = requests.put(url, json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete_reserva(self, reserva_id: int) -> List[Dict[str, Any]]:
        """
        Elimina una reserva a través de la API.

        Args:
            reserva_id: El ID de la reserva a eliminar.

        Returns:
            La lista actualizada de todas las reservas después de la eliminación.

        Raises:
            HTTPError: Si la API retorna un error durante la eliminación.
        """
        url = f"{self.API_URL}/reservas/{reserva_id}"
        resp = requests.delete(url, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()
