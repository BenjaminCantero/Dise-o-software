import requests
from core.observable import Observable

API_URL = "http://127.0.0.1:8000/reservas/"

class ReservaService(Observable):
    def listar_reservas(self):
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()

    def crear_reserva(self, sala_nombre, usuario_username, fecha_inicio, fecha_fin):
        data = {
            "sala_nombre": sala_nombre,
            "usuario_username": usuario_username,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_reserva(self, reserva_id):
        response = requests.delete(f"{API_URL}{reserva_id}")
        response.raise_for_status()
        return response.json()

    def contar_reservas(self):
        reservas = self.listar_reservas()
        return len(reservas)

    def obtener_reservas_por_usuario(self, username):
        reservas = self.listar_reservas()
        return [r for r in reservas if r.get("usuario_username") == username]

    def editar_reserva(self, reserva_id, sala_nombre, usuario_username, fecha_inicio, fecha_fin):
        data = {
            "sala_nombre": sala_nombre,
            "usuario_username": usuario_username,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        response = requests.put(f"{API_URL}{reserva_id}", json=data)
        response.raise_for_status()
        return response.json()

    def obtener_reserva_por_id(self, reserva_id):
        response = requests.get(f"{API_URL}{reserva_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def eliminar_reservas_por_usuario(self, username):
        reservas = self.obtener_reservas_por_usuario(username)
        for reserva in reservas:
            self.eliminar_reserva(reserva["id"])