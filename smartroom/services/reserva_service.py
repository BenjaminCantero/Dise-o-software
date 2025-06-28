import requests
from typing import Any, Dict, List
from smartroom.services.base_api_service import BaseApiService
from smartroom.services.interfaces import IReservaCRUDService
from smartroom.decorators.notificacion_reserva import (
    ComponenteConcreto,
    DecoradorLogging,
    DecoradorValidacion,
    DecoradorAuditoria,
    DecoradorNotificacion
)

class ReservaService(BaseApiService, IReservaCRUDService):
    """
    Facade para la gestión de reservas vía API REST.
    Expone una interfaz simple y maneja internamente las llamadas HTTP y los errores.
    """

    def get_all(self) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{self.API_URL}/reservas/", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al obtener reservas: {e}")

    def create(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        try:
            datos = {
                "usuario": usuario_id,  # Se asume que usuario_id identifica al usuario
                "accion": "crear_reserva",
                "detalle": {
                    "sala": sala_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            }
            # Aplica la cadena de decoradores
            componente = ComponenteConcreto()
            componente = DecoradorLogging(componente)
            componente = DecoradorValidacion(componente)
            componente = DecoradorAuditoria(componente)
            componente = DecoradorNotificacion(componente)
            # Ejecuta la operación decorada (puedes usar el resultado si lo necesitas)
            componente.operacion(datos)

            # Lógica real de creación de reserva
            data = {
                "usuario_id": usuario_id,
                "sala_id": sala_id,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            }
            resp = requests.post(f"{self.API_URL}/reservas/", json=data, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al crear reserva: {e}")

    def update(self, reserva_id, **kwargs):
        try:
            resp = requests.put(f"{self.API_URL}/reservas/{reserva_id}", json=kwargs, headers=self.HEADERS)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise Exception(f"Error al actualizar reserva: {e}")

    def delete(self, reserva_id):
        try:
            resp = requests.delete(f"{self.API_URL}/reservas/{reserva_id}", headers=self.HEADERS)
            resp.raise_for_status()
            return resp.status_code == 204
        except requests.RequestException as e:
            raise Exception(f"Error al eliminar reserva: {e}")