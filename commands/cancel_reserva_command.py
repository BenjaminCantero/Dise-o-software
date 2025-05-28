class CancelReservaCommand:
    def __init__(self, reserva_service, reserva_id):
        self.reserva_service = reserva_service
        self.reserva_id = reserva_id

    def execute(self):
        self.reserva_service.cancelar_reserva(self.reserva_id)