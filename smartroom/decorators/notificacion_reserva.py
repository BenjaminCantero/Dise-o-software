from abc import ABC, abstractmethod

# 1. Interfaz base para los componentes
class Componente(ABC):
    @abstractmethod
    def operacion(self, datos):
        pass

# 2. Componente concreto
class ComponenteConcreto(Componente):
    def operacion(self, datos):
        print(f"Operacion principal ejecutada con datos: {datos}")
        # Simula un resultado
        return {"resultado": "exito", "datos": datos}

class ReservaNotificada:
    def __init__(self, reserva):
        self._reserva = reserva

    def confirmar(self):
        self._reserva.confirmar()
        self._enviar_notificacion()

    def _enviar_notificacion(self):
        print("Notificación enviada")
