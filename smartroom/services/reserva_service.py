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
from smartroom.observer.observer import Subject

class ReservaService(BaseApiService, IReservaCRUDService, Subject):
    """
    Facade para la gestión de reservas vía API REST.
    Expone una interfaz simple y maneja internamente las llamadas HTTP y los errores.
    """

    def __init__(self):
        BaseApiService.__init__(self)
        Subject.__init__(self)

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
            reserva = resp.json()
            self.notify("reserva_creada", reserva)  # Notifica a los observers
            return reserva
        except requests.RequestException as e:
            raise Exception(f"Error al crear reserva: {e}")

    def update(self, reserva_id, **kwargs):
        try:
            datos = {
                "usuario": kwargs.get("usuario_id", "desconocido"),
                "accion": "editar_reserva",
                "detalle": kwargs
            }
            componente = ComponenteConcreto()
            componente = DecoradorLogging(componente)
            componente = DecoradorValidacion(componente)
            componente = DecoradorAuditoria(componente)
            componente = DecoradorNotificacion(componente)
            componente.operacion(datos)

            resp = requests.put(f"{self.API_URL}/reservas/{reserva_id}", json=kwargs, headers=self.HEADERS)
            resp.raise_for_status()
            reserva = resp.json()
            self.notify("reserva_actualizada", reserva)  # Notifica a los observers
            return reserva
        except requests.RequestException as e:
            raise Exception(f"Error al actualizar reserva: {e}")

    def delete(self, reserva_id):
        try:
            datos = {
                "usuario": "desconocido",  # O el usuario que corresponda si está disponible
                "accion": "eliminar_reserva",
                "detalle": {"reserva_id": reserva_id}
            }
            componente = ComponenteConcreto()
            componente = DecoradorLogging(componente)
            componente = DecoradorValidacion(componente)
            componente = DecoradorAuditoria(componente)
            componente = DecoradorNotificacion(componente)
            componente.operacion(datos)

            resp = requests.delete(f"{self.API_URL}/reservas/{reserva_id}", headers=self.HEADERS)
            resp.raise_for_status()
            self.notify("reserva_eliminada", {"reserva_id": reserva_id})  # Notifica a los observers
            return resp.status_code == 204
        except requests.RequestException as e:
            raise Exception(f"Error al eliminar reserva: {e}")

    def obtener_reserva_por_id(self, reserva_id):
        """Devuelve una reserva por su ID o None si no existe."""
        reservas = self.get_all()
        for reserva in reservas:
            if reserva.get("id") == reserva_id:
                return reserva
        return None