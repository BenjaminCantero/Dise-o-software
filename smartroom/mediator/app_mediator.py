from core.singleton import SingletonMeta

class EventListener:
    def on_event(self, sender, event, data):
        raise NotImplementedError("Debe implementar on_event en el componente que recibe eventos.")

class AppMediator(metaclass=SingletonMeta):
    """
    Mediador para coordinar la comunicación entre los diferentes componentes de la aplicación.
    Permite registrar componentes y notificar eventos entre ellos de forma desacoplada.
    """

    def __init__(self):
        self._components = {}

    def register(self, name, component):
        self._components[name] = component

    def unregister(self, name):
        if name in self._components:
            del self._components[name]

    def notify(self, sender, event, data=None):
        for component in list(self._components.values()): 
            if isinstance(component, EventListener):
                component.on_event(sender, event, data)