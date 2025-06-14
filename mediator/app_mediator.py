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

    def notify(self, sender, event, data=None):
        """
        Notifica a los componentes registrados sobre un evento.
        Si se especifica 'target', solo notifica a ese componente.
        """
        # Copia los items para evitar el error si se modifica el diccionario durante la iteración
        for name, component in list(self.components.items()):
            if component != sender:
                component.on_event(sender, event, data)