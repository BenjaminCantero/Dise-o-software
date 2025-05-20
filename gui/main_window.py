import tkinter as tk
from tkinter import ttk
from gui.reservas_panel import ReservasPanel
from gui.salas_panel import SalasPanel
from gui.admin_panel import AdminPanel

class MainWindow(tk.Frame):
    def __init__(self, root, mediator, sala_service=None, reserva_service=None, user=None, user_service=None):
        super().__init__(root)
        self.root = root
        self.mediator = mediator
        self.sala_service = sala_service
        self.reserva_service = reserva_service
        self.user = user
        self.user_service = user_service
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Menú principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú de salas solo para admin
        if self.user and self.user.role == "admin":
            salas_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Salas", menu=salas_menu)
            salas_menu.add_command(label="Ver salas", command=self.ver_salas)

        reservas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reservas", menu=reservas_menu)
        reservas_menu.add_command(label="Ver reservas", command=self.ver_reservas)

        # Barra lateral mejorada
        sidebar = tk.Frame(self, width=220, bg="#232946")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo y nombre del sistema
        logo_frame = tk.Frame(sidebar, bg="#232946")
        logo_frame.pack(pady=(30, 10))
        logo_icon = tk.Label(logo_frame, text="🏢", font=("Arial", 32), bg="#232946", fg="#eebbc3")
        logo_icon.pack()
        logo_label = tk.Label(logo_frame, text="Smart-Rooms", font=("Arial", 18, "bold"), bg="#232946", fg="#eebbc3")
        logo_label.pack()

        # Botones de navegación
        nav_frame = tk.Frame(sidebar, bg="#232946")
        nav_frame.pack(pady=(40, 10), fill="x")

        if self.user and self.user.role == "admin":
            admin_btn = ttk.Button(nav_frame, text="Usuarios", style="Sidebar.TButton", command=self.ver_admin_panel)
            admin_btn.pack(fill="x", pady=8, padx=20)
            salas_btn = ttk.Button(nav_frame, text="Salas", style="Sidebar.TButton", command=self.ver_salas)
            salas_btn.pack(fill="x", pady=8, padx=20)

        reservas_btn = ttk.Button(nav_frame, text="Reservas", style="Sidebar.TButton", command=self.ver_reservas)
        reservas_btn.pack(fill="x", pady=8, padx=20)

        # Separador decorativo
        sep = tk.Frame(sidebar, bg="#eebbc3", height=2)
        sep.pack(fill="x", padx=20, pady=30)

        # Información o pie de página
        info_label = tk.Label(sidebar, text="© 2025 Smart-Rooms", font=("Arial", 9), bg="#232946", fg="#eebbc3")
        info_label.pack(side="bottom", pady=15)

        # Área principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="left", fill="both", expand=True)

        # Pantalla de bienvenida
        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        label = ttk.Label(self.main_frame, text="Bienvenido a Smart-Rooms", font=("Arial", 22, "bold"), foreground="#232946")
        label.pack(pady=60)
        ttk.Label(self.main_frame, text="Gestiona salas y reservas de manera inteligente.", font=("Arial", 14)).pack(pady=10)

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