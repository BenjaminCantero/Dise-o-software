class AppMediator:
    def __init__(self):
        self.components = {}

    def register(self, name, component):
        self.components[name] = component

    def notify(self, sender, event, data=None):
        if event == "sala_actualizada":
            self.components["main_panel"].actualizar_salas()
        elif event == "reserva_actualizada":
            self.components["main_panel"].actualizar_reservas()
        # Agrega más eventos según crezca tu app
