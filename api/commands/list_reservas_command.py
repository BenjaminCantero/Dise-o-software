from api.commands.base_command import Command

class ListReservasCommand(Command):
    def __init__(self, reserva_service):
        self.reserva_service = reserva_service

    def execute(self):
        return self.reserva_service.listar_reservas(self.reserva_service.db)