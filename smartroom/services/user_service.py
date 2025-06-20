import requests

class UserService:
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    def get_usuarios(self):
        resp = requests.get(f"{self.API_URL}/usuarios/", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def create_usuario(self, username, password, role):
        data = {"username": username, "password": password, "role": role}
        resp = requests.post(f"{self.API_URL}/usuarios/", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def update_usuario(self, user_id, username, role):
        data = {"username": username, "role": role}
        resp = requests.put(f"{self.API_URL}/usuarios/{user_id}", json=data, headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def delete_usuario(self, user_id):
        resp = requests.delete(f"{self.API_URL}/usuarios/{user_id}", headers=self.HEADERS)
        resp.raise_for_status()
        return resp.json()

    def autenticar(self, username, password):
        data = {"username": username, "password": password}
        resp = requests.post(f"{self.API_URL}/login", json=data, headers=self.HEADERS)
        if resp.status_code == 200:
            return resp.json()
        return None