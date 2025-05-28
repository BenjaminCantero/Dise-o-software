# adapters/tkinter_to_command_adapter.py
class ReservaDialogAdapter:
    def __init__(self, dialog):
        self.dialog = dialog

    def get_data(self):
        return {
            "usuario": self.dialog.usuario_input.get(),
            "sala": self.dialog.sala_input.get(),
        }
