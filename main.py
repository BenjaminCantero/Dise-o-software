import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from services.user_service import UserService
from services.sala_service import SalaService
from services.reserva_service import ReservaService

def main():
    root = tk.Tk()
    root.withdraw()
    root.state('zoomed')  # Pantalla completa al iniciar

    user_service = UserService()
    sala_service = SalaService()         
    reserva_service = ReservaService()   
    mediator = AppMediator()

    def on_login(user):
        
        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify()
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
        
        app.on_login = on_login

    LoginWindow(root, user_service, on_login)
    root.mainloop()

if __name__ == "__main__":
    main()