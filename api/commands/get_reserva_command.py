from .base_command import Command

class GetReservaCommand(Command):
    def __init__(self, reserva_service, reserva_id):
        self.reserva_service = reserva_service
        self.reserva_id = reserva_id

    def execute(self):
        return self.reserva_service.obtener_reserva_por_id(
            self.reserva_service.db, self.reserva_id
        )