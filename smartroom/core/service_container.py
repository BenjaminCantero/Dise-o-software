from .singleton import SingletonMeta

class ServiceContainer(metaclass=SingletonMeta):
    """
    Contenedor simple para la inyección de dependencias.
    Permite registrar y resolver servicios por interfaz o nombre.
    """
    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        self._services[interface] = implementation

    def resolve(self, interface):
        impl = self._services.get(interface)
        if impl is None:
            raise ValueError(f"No se ha registrado un servicio para {interface}")
        return impl
