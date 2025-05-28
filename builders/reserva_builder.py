from repositories.models import Reserva

# builders/reserva_builder.py
class ReservaBuilder:
    def __init__(self):
        self.reserva = {}

    def set_usuario(self, usuario):
        self.reserva["usuario"] = usuario
        return self

    def set_sala(self, sala):
        self.reserva["sala"] = sala
        return self

    def build(self):
        return Reserva(**self.reserva)
