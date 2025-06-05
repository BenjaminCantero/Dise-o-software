from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog

class DialogFactory:
    """
    Fábrica centralizada para la creación de diálogos.
    Permite crear diferentes tipos de diálogos de forma flexible y escalable.
    """
    def __init__(self):
        self._dialog_map = {
            "nueva_reserva": NuevaReservaDialog,
            "editar_reserva": EditarReservaDialog,
            # Agrega aquí más diálogos si los tienes
        }

    def create_dialog(self, dialog_type, *args, **kwargs):
        """
        Crea una instancia del diálogo solicitado.

        :param dialog_type: str, tipo de diálogo (clave del mapa)
        :param args: argumentos posicionales para el constructor del diálogo
        :param kwargs: argumentos nombrados para el constructor del diálogo
        :return: instancia del diálogo solicitado
        """
        dialog_class = self._dialog_map.get(dialog_type)
        if not dialog_class:
            raise ValueError(f"Tipo de diálogo desconocido: {dialog_type}")
        return dialog_class(*args, **kwargs)
