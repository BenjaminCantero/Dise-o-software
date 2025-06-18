from .base_command import Command

class CreateReservaCommand(Command):
    def __init__(self, reserva_service, reserva_data):
        self.reserva_service = reserva_service
        self.reserva_data = reserva_data

    def execute(self):
        return self.reserva_service.crear_reserva(
            self.reserva_service.db,  # Usa el atributo db
            **self.reserva_data
        )