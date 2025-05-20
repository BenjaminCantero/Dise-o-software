import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from services.user_service import UserService

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal hasta que se loguee

    user_service = UserService()
    mediator = AppMediator()

    def on_login(user):
        root.deiconify()
        app = MainWindow(root, mediator, sala_service=None, reserva_service=None, user=user, user_service=user_service)
        mediator.register("main_window", app)

    login = LoginWindow(root, user_service, on_login)
    root.mainloop()

if __name__ == "__main__":
    main()