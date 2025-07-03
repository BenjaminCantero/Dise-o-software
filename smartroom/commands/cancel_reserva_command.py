from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def undo(self):
        pass  # Opcional: implementar si quieres soporte para deshacer

class CancelReservaCommand(Command):
    def __init__(self, reserva_service, reserva_id):
        self.reserva_service = reserva_service
        self.reserva_id = reserva_id
        self._backup = None  # Para undo

    def execute(self):
        # Guarda el estado antes de cancelar para poder deshacer
        self._backup = self.reserva_service.obtener_reserva_por_id(self.reserva_id)
        self.reserva_service.delete(self.reserva_id)

    def undo(self):
        # Restaura la reserva si existe backup y el servicio tiene el método adecuado
        if self._backup and hasattr(self.reserva_service, "restaurar_reserva"):
            self.reserva_service.restaurar_reserva(self._backup)

class CreateReservaCommand(Command):
    def __init__(self, reserva_service, reserva_data):
        self.reserva_service = reserva_service
        self.reserva_data = reserva_data
        self._created_reserva = None

    def execute(self):
        self._created_reserva = self.reserva_service.create(**self.reserva_data)

    def undo(self):
        if self._created_reserva:
            self.reserva_service.eliminar_reserva(self._created_reserva.id)

class EditReservaCommand(Command):
    def __init__(self, reserva_service, reserva_id, new_data):
        self.reserva_service = reserva_service
        self.reserva_id = reserva_id
        self.new_data = new_data
        self._old_data = None

    def execute(self):
        # Guarda el estado anterior para undo
        old_reserva = self.reserva_service.obtener_reserva_por_id(self.reserva_id)
        if old_reserva:
            self._old_data = {
                "sala_id": old_reserva.get("sala_id"),
                "usuario_id": old_reserva.get("usuario_id"),
                "fecha_inicio": old_reserva.get("fecha_inicio"),
                "fecha_fin": old_reserva.get("fecha_fin")
            }
        self.reserva_service.update(self.reserva_id, **self.new_data)

    def undo(self):
        if self._old_data:
            self.reserva_service.editar_reserva(self.reserva_id, **self._old_data)