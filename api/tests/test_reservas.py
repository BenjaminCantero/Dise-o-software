from fastapi.testclient import TestClient
from api.main import app
import uuid

client = TestClient(app)
headers = {"Authorization": "Bearer secrettoken"}

def test_get_reservas():
    response = client.get("/reservas/", headers=headers)
    assert response.status_code == 200

def test_create_and_get_reserva():
    # Crea usuario y sala únicos
    unique_username = f"reservauser_{uuid.uuid4()}"
    user_data = {"username": unique_username, "password": "pass", "role": "estudiante"}
    user_resp = client.post("/usuarios/", json=user_data, headers=headers)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    unique_nombre = f"Sala Reserva {uuid.uuid4()}"
    sala_data = {"nombre": unique_nombre, "capacidad": 5, "estado": "disponible"}
    sala_resp = client.post("/salas/", json=sala_data, headers=headers)
    assert sala_resp.status_code == 201
    sala_id = sala_resp.json()["id"]

    reserva_data = {
        "usuario_id": user_id,
        "sala_id": sala_id,
        "fecha_inicio": "2025-06-20T10:00:00",
        "fecha_fin": "2025-06-20T11:00:00"
    }
    create_resp = client.post("/reservas/", json=reserva_data, headers=headers)
    if create_resp.status_code != 201:
        print("Reserva data:", reserva_data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    reservas = create_resp.json()
    assert isinstance(reservas, list)
    reserva_id = reservas[-1]["id"]

    # Obtener reserva por id
    get_resp = client.get(f"/reservas/{reserva_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == reserva_id

def test_update_reserva():
    unique_username = f"reservauser_{uuid.uuid4()}"
    user_data = {"username": unique_username, "password": "pass", "role": "estudiante"}
    user_resp = client.post("/usuarios/", json=user_data, headers=headers)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    unique_nombre = f"Sala Reserva {uuid.uuid4()}"
    sala_data = {"nombre": unique_nombre, "capacidad": 5, "estado": "disponible"}
    sala_resp = client.post("/salas/", json=sala_data, headers=headers)
    assert sala_resp.status_code == 201
    sala_id = sala_resp.json()["id"]

    reserva_data = {
        "usuario_id": user_id,
        "sala_id": sala_id,
        "fecha_inicio": "2025-06-20T10:00:00",
        "fecha_fin": "2025-06-20T11:00:00"
    }
    create_resp = client.post("/reservas/", json=reserva_data, headers=headers)
    if create_resp.status_code != 201:
        print("Reserva data:", reserva_data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    reserva_id = create_resp.json()[-1]["id"]

    # Actualiza la reserva
    update_data = {
        "usuario_id": user_id,
        "sala_id": sala_id,
        "fecha_inicio": "2025-06-21T13:00:00",
        "fecha_fin": "2025-06-21T14:00:00"
    }
    update_resp = client.put(f"/reservas/{reserva_id}", json=update_data, headers=headers)
    if update_resp.status_code != 200:
        print("Update data:", update_data)
        print("Respuesta:", update_resp.json())
    assert update_resp.status_code == 200
    assert isinstance(update_resp.json(), list)

def test_delete_reserva():
    unique_username = f"reservauser_{uuid.uuid4()}"
    user_data = {"username": unique_username, "password": "pass", "role": "estudiante"}
    user_resp = client.post("/usuarios/", json=user_data, headers=headers)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    unique_nombre = f"Sala Reserva {uuid.uuid4()}"
    sala_data = {"nombre": unique_nombre, "capacidad": 5, "estado": "disponible"}
    sala_resp = client.post("/salas/", json=sala_data, headers=headers)
    assert sala_resp.status_code == 201
    sala_id = sala_resp.json()["id"]

    reserva_data = {
        "usuario_id": user_id,
        "sala_id": sala_id,
        "fecha_inicio": "2025-06-20T10:00:00",
        "fecha_fin": "2025-06-20T11:00:00"
    }
    create_resp = client.post("/reservas/", json=reserva_data, headers=headers)
    if create_resp.status_code != 201:
        print("Reserva data:", reserva_data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    reserva_id = create_resp.json()[-1]["id"]

    # Elimina la reserva
    delete_resp = client.delete(f"/reservas/{reserva_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert isinstance(delete_resp.json(), list)