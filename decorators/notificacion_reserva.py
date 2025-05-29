# decorators/notificacion_reserva.py
class ReservaNotificada:
    def __init__(self, reserva):
        self._reserva = reserva

    def confirmar(self):
        self._reserva.confirmar()
        self._enviar_notificacion()

    def _enviar_notificacion(self):
        print("Notificación enviada")
