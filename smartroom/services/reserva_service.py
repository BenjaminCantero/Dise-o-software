import requests

class ReservaService:
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_reservas(self):
        resp = requests.get(f"{self.API_URL}/reservas/", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create_reserva(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        data = {
            "usuario_id": usuario_id,
            "sala_id": sala_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        resp = requests.post(f"{self.API_URL}/reservas/", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update_reserva(self, reserva_id, usuario_id, sala_id, fecha_inicio, fecha_fin):
        data = {
            "usuario_id": usuario_id,
            "sala_id": sala_id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        resp = requests.put(f"{self.API_URL}/reservas/{reserva_id}", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete_reserva(self, reserva_id):
        resp = requests.delete(f"{self.API_URL}/reservas/{reserva_id}", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()