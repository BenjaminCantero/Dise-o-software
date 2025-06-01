import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from mediator.app_mediator import AppMediator
from services.user_service import UserService
from services.sala_service import SalaService
from services.reserva_service import ReservaService

def main():
    print("--- Iniciando main() ---") # Nuevo print

    print("Inicializando servicios...")
    user_service = UserService()
    sala_service = SalaService()
    reserva_service = ReservaService()
    print("Servicios inicializados.")

    print("Creando AppMediator...")
    mediator = AppMediator()
    print("AppMediator creado.")

    print("Creando ventana raíz Tk (root)...")
    root = tk.Tk()
    print("Ventana raíz Tk creada.")
    root.withdraw() # Oculta la ventana raíz principal inicialmente
    print("Ventana raíz (root) oculta.")

    # Define la función on_login aquí para que LoginWindow la pueda usar
    def on_login(user):
        print(f"--- on_login llamado para el usuario: {user.username} ---") # Nuevo print
        for widget in root.winfo_children():
            widget.destroy() # Limpia widgets anteriores (como LoginWindow)
        
        print("Mostrando MainWindow...") # Nuevo print
        root.deiconify() # Muestra la ventana raíz ahora que el login fue exitoso
        app = MainWindow(
            root,
            mediator,
            sala_service=sala_service,
            reserva_service=reserva_service,
            user=user,
            user_service=user_service,
            on_login=on_login # Pasa la referencia a on_login nuevamente si es necesario para cerrar sesión
        )
        app.pack(fill="both", expand=True)
        print("MainWindow empaquetada.") # Nuevo print

    print("Creando y mostrando LoginWindow...")
    try:
        LoginWindow(root, user_service, on_login)
        print("LoginWindow instanciada (debería estar visible o en proceso de mostrarse).")
    except Exception as e:
        print(f"ERROR al instanciar LoginWindow: {e}") # Para capturar errores aquí
        import traceback
        traceback.print_exc() # Imprime el traceback completo

    print("Iniciando root.mainloop()... La aplicación debería estar interactiva ahora.")
    try:
        root.mainloop()
    except Exception as e:
        print(f"ERROR durante root.mainloop(): {e}") # Para capturar errores aquí
        import traceback
        traceback.print_exc() # Imprime el traceback completo
    
    print("--- main() ha terminado (después de cerrar la GUI) ---") # Nuevo print

if __name__ == "__main__":
    main()
