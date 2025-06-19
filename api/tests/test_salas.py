from fastapi.testclient import TestClient
from api.main import app
import uuid

client = TestClient(app)
headers = {"Authorization": "Bearer secrettoken"}

def test_get_salas():
    response = client.get("/salas/", headers=headers)
    assert response.status_code == 200

def test_create_sala():
    unique_nombre = f"Sala Test {uuid.uuid4()}"
    data = {"nombre": unique_nombre, "capacidad": 20, "estado": "disponible"}
    response = client.post("/salas/", json=data, headers=headers)
    if response.status_code != 201:
        print("Sala data:", data)
        print("Respuesta:", response.json())
    assert response.status_code == 201
    assert response.json()["nombre"] == unique_nombre

def test_get_sala_by_id():
    unique_nombre = f"Sala Test {uuid.uuid4()}"
    data = {"nombre": unique_nombre, "capacidad": 15, "estado": "disponible"}
    create_resp = client.post("/salas/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Sala data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    sala_id = create_resp.json()["id"]
    response = client.get(f"/salas/{sala_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == unique_nombre

def test_update_sala():
    unique_nombre = f"Sala Test {uuid.uuid4()}"
    data = {"nombre": unique_nombre, "capacidad": 10, "estado": "disponible"}
    create_resp = client.post("/salas/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Sala data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    sala_id = create_resp.json()["id"]
    update_data = {"nombre": f"Sala Actualizada {uuid.uuid4()}", "capacidad": 12, "estado": "ocupada"}
    response = client.put(f"/salas/{sala_id}", json=update_data, headers=headers)
    if response.status_code != 200:
        print("Update data:", update_data)
        print("Respuesta:", response.json())
    assert response.status_code == 200
    assert response.json()["nombre"].startswith("Sala Actualizada")

def test_delete_sala():
    unique_nombre = f"Sala Test {uuid.uuid4()}"
    data = {"nombre": unique_nombre, "capacidad": 8, "estado": "disponible"}
    create_resp = client.post("/salas/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Sala data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    sala_id = create_resp.json()["id"]
    response = client.delete(f"/salas/{sala_id}", headers=headers)
    if response.status_code != 200:
        print("Delete sala id:", sala_id)
        print("Respuesta:", response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)