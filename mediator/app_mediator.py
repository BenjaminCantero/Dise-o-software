class AppMediator:
    """
    Mediador para coordinar la comunicación entre los diferentes componentes de la aplicación.
    """

    def __init__(self):
        self.components = {}

    def register(self, name, component):
        """
        Registra un componente con un nombre único.
        """
        self.components[name] = component

    def notify(self, sender, event, data=None):
        """
        Notifica a los componentes registrados sobre un evento.
        """
        for name, component in self.components.items():
            # Evita notificar al componente que envió el evento
            if component is not sender and hasattr(component, "on_event"):
                component.on_event(sender, event, data)