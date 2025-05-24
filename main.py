import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from services.user_service import UserService
from services.sala_service import SalaService
from services.reserva_service import ReservaService

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal hasta que se loguee

    user_service = UserService()
    sala_service = SalaService()         # <--- Instancia real
    reserva_service = ReservaService()   # <--- Instancia real
    mediator = AppMediator()

    def on_login(user):
        root.deiconify()
        app = MainWindow(root, mediator, sala_service=sala_service, reserva_service=reserva_service, user=user, user_service=user_service)
        app.pack(fill="both", expand=True)  # <-- ¡Agrega esta línea!

    login = LoginWindow(root, user_service, on_login)
    root.mainloop()

if __name__ == "__main__":
    main()