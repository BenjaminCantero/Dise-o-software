from tkinter import ttk
import tkinter as tk
from gui.reservas_panel import ReservasPanel
from gui.salas_panel import SalasPanel
from gui.admin_panel import AdminPanel
from gui.dashboard_panel import DashboardPanel

class MainWindow(tk.Frame):
    def __init__(self, root, mediator, sala_service=None, reserva_service=None, user=None, user_service=None):
        super().__init__(root)
        self.root = root
        self.mediator = mediator
        self.sala_service = sala_service
        self.reserva_service = reserva_service
        self.user = user
        self.user_service = user_service

        # Estilos para los botones de la barra lateral
        style = ttk.Style()
        style.configure("Sidebar.TButton", font=("Arial", 12), background="#232946", foreground="#eebbc3")
        style.configure("SidebarActive.TButton", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946")

        # Crear barra lateral y botones
        sidebar = ttk.Frame(self)
        sidebar.pack(side="left", fill="y")

        self.btn_dashboard = ttk.Button(sidebar, text="Dashboard", style="Sidebar.TButton", command=lambda: self.seleccionar_seccion("dashboard"))
        self.btn_dashboard.pack(fill="x")
        self.btn_reservas = ttk.Button(sidebar, text="Reservas", style="Sidebar.TButton", command=lambda: self.seleccionar_seccion("reservas"))
        self.btn_reservas.pack(fill="x")
        self.btn_salas = ttk.Button(sidebar, text="Salas", style="Sidebar.TButton", command=lambda: self.seleccionar_seccion("salas"))
        self.btn_salas.pack(fill="x")
        # Agrega más botones si tienes más secciones

        self.seleccionar_seccion("dashboard")  # Por defecto

    def seleccionar_seccion(self, seccion):
        # Quitar resaltado de todos
        self.btn_dashboard.configure(style="Sidebar.TButton")
        self.btn_reservas.configure(style="Sidebar.TButton")
        self.btn_salas.configure(style="Sidebar.TButton")
        # ...otros botones...

        # Resaltar el botón activo
        if seccion == "dashboard":
            self.btn_dashboard.configure(style="SidebarActive.TButton")
        elif seccion == "reservas":
            self.btn_reservas.configure(style="SidebarActive.TButton")
        elif seccion == "salas":
            self.btn_salas.configure(style="SidebarActive.TButton")
        # ...otros botones...

        # Aquí puedes cambiar el panel mostrado según la sección
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        if seccion == "dashboard":
            dashboard = DashboardPanel(self.main_frame, sala_service=self.sala_service, reserva_service=self.reserva_service, user_service=self.user_service)
            dashboard.pack(fill="both", expand=True)
        elif seccion == "reservas":
            reservas_panel = ReservasPanel(self.main_frame, reserva_service=self.reserva_service, mediator=self.mediator)
            reservas_panel.pack(fill="both", expand=True)
        elif seccion == "salas":
            salas_panel = SalasPanel(self.main_frame, sala_service=self.sala_service, mediator=self.mediator)
            salas_panel.pack(fill="both", expand=True)

    def mostrar_bienvenida(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        bienvenida_frame = tk.Frame(self.main_frame, bg="#f4f4f8")
        bienvenida_frame.pack(expand=True)
        label = tk.Label(bienvenida_frame, text="Bienvenido a Smart-Rooms", font=("Arial", 26, "bold"), bg="#f4f4f8", fg="#232946")
        label.pack(pady=40)
        subtitulo = tk.Label(bienvenida_frame, text="Gestiona salas y reservas de manera inteligente.", font=("Arial", 15), bg="#f4f4f8", fg="#232946")
        subtitulo.pack(pady=10)

    def ver_salas(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        salas_panel = SalasPanel(self.main_frame, sala_service=self.sala_service, mediator=self.mediator)
        salas_panel.pack(fill="both", expand=True)

    def ver_reservas(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        reservas_panel = ReservasPanel(self.main_frame, reserva_service=self.reserva_service, mediator=self.mediator)
        reservas_panel.pack(fill="both", expand=True)

    def ver_admin_panel(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        admin_panel = AdminPanel(self.main_frame, user_service=self.user_service, mediator=self.mediator)
        admin_panel.pack(fill="both", expand=True)

    def ver_dashboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        dashboard = DashboardPanel(self.main_frame, sala_service=self.sala_service, reserva_service=self.reserva_service, user_service=self.user_service)
        dashboard.pack(fill="both", expand=True)

    def salir_sistema(self):
        self.root.destroy()