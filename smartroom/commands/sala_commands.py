class CreateSalaCommand:
    def __init__(self, sala_service, nombre, capacidad, estado):
        self.sala_service = sala_service
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = estado

    def execute(self):
        self.sala_service.create(self.nombre, self.capacidad, self.estado)

class EditSalaCommand:
    def __init__(self, sala_service, sala_id, nombre, capacidad, estado):
        self.sala_service = sala_service
        self.sala_id = sala_id
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = estado

    def execute(self):
        self.sala_service.update(self.sala_id, self.nombre, self.capacidad, self.estado)

class DeleteSalaCommand:
    def __init__(self, sala_service, sala_id):
        self.sala_service = sala_service
        self.sala_id = sala_id

    def execute(self):
        self.sala_service.delete(self.sala_id)