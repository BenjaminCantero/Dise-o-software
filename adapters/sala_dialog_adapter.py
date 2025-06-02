class SalaDialogAdapter:
    """
    Adapter para extraer datos del diálogo de sala y convertirlos
    al formato esperado por los comandos o servicios de sala.
    """
    def __init__(self, dialog):
        self.dialog = dialog

    def get_data(self):
        return {
            "nombre": self.dialog.nombre_input.get(),
            "capacidad": int(self.dialog.capacidad_input.get()) if hasattr(self.dialog, "capacidad_input") else None,
        }