from fastapi.testclient import TestClient
from api.main import app
import uuid

client = TestClient(app)
headers = {"Authorization": "Bearer secrettoken"}

def test_get_usuarios():
    response = client.get("/usuarios/", headers=headers)
    assert response.status_code == 200

def test_create_usuario():
    unique_username = f"testuser_{uuid.uuid4()}"
    data = {"username": unique_username, "password": "testpass", "role": "estudiante"}
    response = client.post("/usuarios/", json=data, headers=headers)
    if response.status_code != 201:
        print("Usuario data:", data)
        print("Respuesta:", response.json())
    assert response.status_code == 201
    assert response.json()["username"] == unique_username

def test_get_usuario_by_id():
    unique_username = f"testuser_{uuid.uuid4()}"
    data = {"username": unique_username, "password": "testpass", "role": "profesor"}
    create_resp = client.post("/usuarios/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Usuario data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]
    response = client.get(f"/usuarios/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == unique_username

def test_update_usuario():
    unique_username = f"testuser_{uuid.uuid4()}"
    data = {"username": unique_username, "password": "testpass", "role": "admin"}
    create_resp = client.post("/usuarios/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Usuario data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]
    update_data = {"username": f"updated_{unique_username}", "password": "newpass", "role": "admin"}
    response = client.put(f"/usuarios/{user_id}", json=update_data, headers=headers)
    if response.status_code != 200:
        print("Update data:", update_data)
        print("Respuesta:", response.json())
    assert response.status_code == 200
    assert response.json()["username"] == f"updated_{unique_username}"

def test_delete_usuario():
    unique_username = f"testuser_{uuid.uuid4()}"
    data = {"username": unique_username, "password": "testpass", "role": "estudiante"}
    create_resp = client.post("/usuarios/", json=data, headers=headers)
    if create_resp.status_code != 201:
        print("Usuario data:", data)
        print("Respuesta:", create_resp.json())
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]
    response = client.delete(f"/usuarios/{user_id}", headers=headers)
    if response.status_code != 200:
        print("Delete user id:", user_id)
        print("Respuesta:", response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)