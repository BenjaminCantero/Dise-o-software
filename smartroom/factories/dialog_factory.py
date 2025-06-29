from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog
from gui.nueva_sala_dialog import NuevaSalaDialog
from gui.editar_sala_dialog import EditarSalaDialog
from gui.editar_usuario_dialog import EditarUsuarioDialog
#trabajar
class DialogFactory:
    """
    Fábrica centralizada para la creación de diálogos.
    Permite crear diferentes tipos de diálogos de forma flexible y escalable.
    """
    def __init__(self, sala_service=None, user_service=None, reserva_service=None):
        self.sala_service = sala_service
        self.user_service = user_service
        self.reserva_service = reserva_service
        self._dialog_map = {
            "nueva_reserva": NuevaReservaDialog,
            "editar_reserva": EditarReservaDialog,
            "nueva_sala": NuevaSalaDialog,
            "editar_sala": EditarSalaDialog,
            "editar_usuario": EditarUsuarioDialog,
        }

    def create_dialog(self, dialog_type, *args, **kwargs):
        """
        Crea una instancia del diálogo solicitado.
        Inyecta dependencias automáticamente según el tipo de diálogo.

        :param dialog_type: str, tipo de diálogo (clave del mapa)
        :param args: argumentos posicionales para el constructor del diálogo
        :param kwargs: argumentos nombrados para el constructor del diálogo
        :return: instancia del diálogo solicitado
        """
        dialog_class = self._dialog_map.get(dialog_type)
        if not dialog_class:
            raise ValueError(f"Tipo de diálogo desconocido: {dialog_type}")
        # Inyección automática de servicios según el tipo de diálogo
        if dialog_type == "editar_sala":
            # Solo inyectar sala_service si no está ya en args o kwargs
            if "sala_service" not in kwargs:
                return dialog_class(args[0], args[1], self.sala_service, **kwargs)
            else:
                return dialog_class(*args, **kwargs)
        if dialog_type == "nueva_sala":
            if "sala_service" not in kwargs:
                return dialog_class(args[0], self.sala_service, **kwargs)
            else:
                return dialog_class(*args, **kwargs)
        # Otros diálogos pueden requerir lógica similar
        return dialog_class(*args, **kwargs)
