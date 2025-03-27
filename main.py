import ttkbootstrap as ttk
from ui import RoomManagementApp
from database import create_tables

if __name__ == "__main__":
    create_tables()

    root = ttk.Window(themename="superhero")
    root.title("Sistema de Gestión de Salas Universitarias")
    root.geometry("800x500")

    app = RoomManagementApp(root)

    root.mainloop()
