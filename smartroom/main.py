import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from core.service_container import ServiceContainer
from smartroom.services.interfaces import IUsuarioCRUDService, ISalaCRUDService, IReservaCRUDService
from smartroom.services.user_service import UserService
from smartroom.services.sala_service import SalaService
from smartroom.services.reserva_service import ReservaService
from gui.reservas_panel import ReservasPanel

def main():
    # Configuración del contenedor de servicios
    container = ServiceContainer()
    container.register(IUsuarioCRUDService, UserService())
    container.register(ISalaCRUDService, SalaService())
    container.register(IReservaCRUDService, ReservaService())

    # Obtén la instancia de ReservaService
    reserva_service = container.resolve(IReservaCRUDService)

    # Crea el observer (panel) y suscríbelo
    # OJO: El panel debe ser el mismo que usas en tu MainWindow
    # Así que la suscripción final debe hacerse después de crear el panel en MainWindow

    mediator = AppMediator()

    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz principal inicialmente

    def on_login(user):
        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify()
        root.state("zoomed")  # Maximiza la ventana principal
        app = MainWindow(
            root,
            mediator,
            sala_service=container.resolve(ISalaCRUDService),
            reserva_service=reserva_service,
            user=user,
            user_service=container.resolve(IUsuarioCRUDService),
            on_login=on_login
        )
        app.pack(fill="both", expand=True)

        # --- Aquí suscribes el observer después de crear el panel ---
        # Si MainWindow tiene un atributo reservas_panel:
        if hasattr(app, "reservas_panel"):
            reserva_service.attach(app.reservas_panel)

    try:
        LoginWindow(root, container.resolve(IUsuarioCRUDService), on_login)
    except Exception as e:
        import traceback
        traceback.print_exc()

    try:
        root.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()