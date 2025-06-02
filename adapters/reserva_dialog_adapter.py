# adapters/tkinter_to_command_adapter.py
class ReservaDialogAdapter:
    """
    Adapter para extraer datos del diálogo de reserva y convertirlos
    al formato esperado por los comandos o servicios de reserva.
    """
    def __init__(self, dialog):
        self.dialog = dialog

    def get_data(self):
        return {
            "usuario": self.dialog.usuario_input.get(),
            "sala": self.dialog.sala_input.get(),
            "fecha_inicio": self.dialog.fecha_inicio_input.get() if hasattr(self.dialog, "fecha_inicio_input") else None,
            "fecha_fin": self.dialog.fecha_fin_input.get() if hasattr(self.dialog, "fecha_fin_input") else None,
        }
