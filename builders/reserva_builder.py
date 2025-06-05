from repositories.models import Reserva

# builders/reserva_builder.py
class ReservaBuilder:
    def __init__(self):
        self._usuario = None
        self._sala = None
        self._fecha_inicio = None
        self._fecha_fin = None

    def set_usuario(self, usuario):
        self._usuario = usuario.id if hasattr(usuario, "id") else usuario
        return self

    def set_sala(self, sala):
        self._sala = sala.id if hasattr(sala, "id") else sala
        return self

    def set_fecha_inicio(self, fecha_inicio):
        self._fecha_inicio = fecha_inicio
        return self

    def set_fecha_fin(self, fecha_fin):
        self._fecha_fin = fecha_fin
        return self

    def build(self):
        # Validación robusta
        if self._usuario is None:
            raise ValueError("usuario_id es obligatorio")
        if self._sala is None:
            raise ValueError("sala_id es obligatorio")
        if self._fecha_inicio is None:
            raise ValueError("fecha_inicio es obligatorio")
        if self._fecha_fin is None:
            raise ValueError("fecha_fin es obligatorio")
        return Reserva(
            usuario_id=self._usuario,
            sala_id=self._sala,
            fecha_inicio=self._fecha_inicio,
            fecha_fin=self._fecha_fin
        )
