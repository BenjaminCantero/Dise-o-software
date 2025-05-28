from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog

# factories/dialog_factory.py
class DialogFactory:
    def create_nueva_reserva_dialog(self, root, mediator):
        return NuevaReservaDialog(root, mediator)

    def create_editar_reserva_dialog(self, root, mediator):
        return EditarReservaDialog(root, mediator)
