from repositories.models import Reserva

# builders/reserva_builder.py
class ReservaBuilder:
    def __init__(self):
        self.reserva = {}

    def set_usuario_id(self, usuario_id):
        self.reserva["usuario_id"] = usuario_id
        return self

    def set_sala_id(self, sala_id):
        self.reserva["sala_id"] = sala_id
        return self

    def set_fecha_inicio(self, fecha_inicio):
        self.reserva["fecha_inicio"] = fecha_inicio
        return self

    def set_fecha_fin(self, fecha_fin):
        self.reserva["fecha_fin"] = fecha_fin
        return self

    def build(self):
        return Reserva(**self.reserva)
