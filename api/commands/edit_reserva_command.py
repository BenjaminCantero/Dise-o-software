from .base_command import Command

class EditReservaCommand(Command):
    def __init__(self, reserva_service, reserva_id, reserva_data):
        self.reserva_service = reserva_service
        self.reserva_id = reserva_id
        self.reserva_data = reserva_data
        self._backup = None  # Para undo, si lo deseas

    def execute(self):
        # Guarda el estado anterior si quieres soporte de undo
        self._backup = self.reserva_service.obtener_reserva_por_id(
            self.reserva_service.db, self.reserva_id
        )
        return self.reserva_service.editar_reserva(
            self.reserva_service.db,
            self.reserva_id,
            **self.reserva_data
        )

    def undo(self):
        if self._backup:
            self.reserva_service.editar_reserva(
                self.reserva_service.db,
                self.reserva_id,
                usuario_id=self._backup.usuario_id,
                sala_id=self._backup.sala_id,
                fecha_inicio=self._backup.fecha_inicio,
                fecha_fin=self._backup.fecha_fin
            )