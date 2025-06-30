import tkinter as tk
import sys
import os

# --- Bloque para asegurar que la raíz del proyecto esté en el path ---
# Este bloque es una salvaguarda para encontrar la carpeta 'api'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --------------------------------------------------------------------

# ¡IMPORTANTE! Nota el punto (.) antes de cada módulo local.
from .gui.main_window import MainWindow
from .services.sala_service import SalaService
from .services.reserva_service import ReservaService
from .services.user_service import UserService
from .factories.dialog_factory import DialogFactory

def main():
    """
    Punto de entrada principal para la aplicación de escritorio SmartRoom.
    
    Este método inicializa los servicios, las fábricas y la ventana principal
    de la aplicación, y luego inicia el bucle de eventos de la GUI.
    """
    # Se asegura de que la ruta a la base de datos sea correcta.
    db_path = os.path.join(project_root, 'api.db')
    
    # Inicialización de servicios
    sala_service = SalaService(db_path)
    user_service = UserService(db_path)
    reserva_service = ReservaService(db_path)

    # Inicialización de la fábrica de diálogos con los servicios
    dialog_factory = DialogFactory(
        sala_service=sala_service,
        user_service=user_service,
        reserva_service=reserva_service
    )
    
    # Creación y ejecución de la ventana principal
    root = tk.Tk()
    app = MainWindow(
        root,
        sala_service=sala_service,
        reserva_service=reserva_service,
        user_service=user_service,
        dialog_factory=dialog_factory
    )
    root.mainloop()

if __name__ == "__main__":
    main()
