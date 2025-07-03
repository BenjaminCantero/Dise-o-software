class UsuarioBuilder:
    def __init__(self):
        self._username = None
        self._password = None
        self._role = None

    def set_username(self, username):
        self._username = username
        return self

    def set_password(self, password):
        self._password = password
        return self

    def set_role(self, role):
        self._role = role
        return self

    def build(self):
        if self._username is None:
            raise ValueError("El username es obligatorio")
        if self._role is None:
            raise ValueError("El rol es obligatorio")
        data = {
            "username": self._username,
            "role": self._role
        }
        if self._password is not None:
            data["password"] = self._password
        return data
