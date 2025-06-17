<<<<<<<< HEAD:smart room/services/sala_service.py
import requests
from core.observable import Observable
API_URL = "http://127.0.0.1:8000/salas/"
========
# services/sala_service.py
from api.db import SessionLocal
from api.models.sala import Sala
from api.models.reserva import Reserva
from smartroom.core.observable import Observable
from smartroom.core.singleton import SingletonMeta  # <--- IMPORTADO para Singleton
from smartroom.builders.sala_builder import SalaBuilder
from sqlalchemy.orm import joinedload

class SalaService(Observable, metaclass=SingletonMeta): # <--- METACLASE AÑADIDA para Singleton
    def __init__(self):
        super().__init__() # Inicialización de Observable
>>>>>>>> Benjamín-cantero:api/services/sala_service.py

class SalaService(Observable):
    def listar_salas(self):
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()

    def crear_sala(self, nombre, capacidad, estado="disponible"):
        data = {
            "nombre": nombre,
            "capacidad": capacidad,
            "estado": estado
        }
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def editar_sala(self, sala_id, nombre, capacidad, estado):
        data = {
            "nombre": nombre,
            "capacidad": capacidad,
            "estado": estado
        }
        response = requests.put(f"{API_URL}{sala_id}", json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_sala(self, sala_id):
        response = requests.delete(f"{API_URL}{sala_id}")
        response.raise_for_status()
        return response.json()

    def obtener_sala_por_id(self, sala_id):
        response = requests.get(f"{API_URL}{sala_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()