import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from api.services.user_service import UserService
from api.services.sala_service import SalaService
from api.services.reserva_service import ReservaService

def main():
    user_service = UserService()
    sala_service = SalaService()
    reserva_service = ReservaService()

    mediator = AppMediator()

    root = tk.Tk()
    root.withdraw() # Oculta la ventana raíz principal inicialmente

    def on_login(user):
        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify()
        root.state("zoomed") # Maximiza la ventana principal
        app = MainWindow(
            root,
            mediator,
            sala_service=sala_service,
            reserva_service=reserva_service,
            user=user,
            user_service=user_service,
            on_login=on_login
        )
        app.pack(fill="both", expand=True)

    try:
        LoginWindow(root, user_service, on_login)
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