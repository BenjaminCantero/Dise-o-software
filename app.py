import tkinter as tk
from login import LoginSistema

def main():
    # Crear la ventana principal
    root = tk.Tk()
    
    # Inicializar el sistema de login
    login_app = LoginSistema(root)
    
    # Configuración adicional de la ventana
    root.resizable(False, False)  # Para que no se pueda redimensionar
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
