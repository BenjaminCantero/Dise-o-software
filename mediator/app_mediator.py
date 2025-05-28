from core.singleton import SingletonMeta

class AppMediator(metaclass=SingletonMeta):
    """
    Mediador para coordinar la comunicación entre los diferentes componentes de la aplicación.
    Permite registrar componentes y notificar eventos entre ellos de forma desacoplada.
    """

    def __init__(self):
        self.components = {}

    def register(self, name, component):
        """
        Registra un componente con un nombre único.
        """
        self.components[name] = component

    def unregister(self, name):
        """
        Elimina un componente registrado.
        """
        if name in self.components:
            del self.components[name]

    def notify(self, sender, event, data=None, target=None):
        """
        Notifica a los componentes registrados sobre un evento.
        Si se especifica 'target', solo notifica a ese componente.
        """
        if target:
            component = self.components.get(target)
            if component and hasattr(component, "on_event"):
                component.on_event(sender, event, data)
        else:
            for name, component in self.components.items():
                # Evita notificar al componente que envió el evento
                if component is not sender and hasattr(component, "on_event"):
                    component.on_event(sender, event, data)