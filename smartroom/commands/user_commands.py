class CreateUsuarioCommand:
    def __init__(self, user_service, usuario_data):
        self.user_service = user_service
        self.usuario_data = usuario_data

    def execute(self):
        self.user_service.create(
            self.usuario_data["username"],
            self.usuario_data["password"],
            self.usuario_data["role"]
        )

class EditUsuarioCommand:
    def __init__(self, user_service, usuario_id, usuario_data):
        self.user_service = user_service
        self.usuario_id = usuario_id
        self.usuario_data = usuario_data

    def execute(self):
        self.user_service.update(
            self.usuario_id,
            self.usuario_data["username"],
            self.usuario_data["role"]
        )

class DeleteUsuarioCommand:
    def __init__(self, user_service, usuario_id):
        self.user_service = user_service
        self.usuario_id = usuario_id

    def execute(self):
        self.user_service.delete(self.usuario_id)