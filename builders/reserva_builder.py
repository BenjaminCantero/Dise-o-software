from repositories.models import Reserva

# builders/reserva_builder.py
class ReservaBuilder:
    def __init__(self):
        self._data = {}

    def set_usuario(self, usuario):
        self._data["usuario_id"] = usuario.id if hasattr(usuario, "id") else usuario
        return self

    def set_sala(self, sala):
        self._data["sala_id"] = sala.id if hasattr(sala, "id") else sala
        return self

    def set_fecha_inicio(self, fecha_inicio):
        self._data["fecha_inicio"] = fecha_inicio
        return self

    def set_fecha_fin(self, fecha_fin):
        self._data["fecha_fin"] = fecha_fin
        return self

    def build(self):
        # Validación básica
        if "usuario_id" not in self._data or "sala_id" not in self._data:
            raise ValueError("usuario_id y sala_id son obligatorios")
        return Reserva(**self._data)
