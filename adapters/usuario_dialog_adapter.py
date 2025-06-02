class UsuarioDialogAdapter:
    """
    Adapter para extraer datos del diálogo de usuario y convertirlos
    al formato esperado por los comandos o servicios de usuario.
    """
    def __init__(self, dialog):
        self.dialog = dialog

    def get_data(self):
        return {
            "username": self.dialog.username_input.get(),
            "role": self.dialog.rol_input.get() if hasattr(self.dialog, "rol_input") else None,
        }