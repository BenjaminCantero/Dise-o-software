import requests
from typing import Any, Dict, List
from smartroom.services.interfaces import IReservaCRUDService

class ReservaService(IReservaCRUDService):
    """
    Cliente de servicio para interactuar con la API de Reservas.
    """

    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_all(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.API_URL}/reservas/", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        data = {
            "usuario_id": usuario_id,
            "sala_id": sala_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        resp = requests.post(f"{self.API_URL}/reservas/", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update(self, reserva_id, **kwargs):
        resp = requests.put(f"{self.API_URL}/reservas/{reserva_id}", json=kwargs, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete(self, reserva_id):
        resp = requests.delete(f"{self.API_URL}/reservas/{reserva_id}", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.status_code == 204