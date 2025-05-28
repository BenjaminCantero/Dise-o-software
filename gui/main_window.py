import tkinter as tk
from tkinter import ttk
from gui.reservas_panel import ReservasPanel
from gui.salas_panel import SalasPanel
from gui.admin_panel import AdminPanel
from gui.dashboard_panel import DashboardPanel
from gui.mis_reservas_panel import MisReservasPanel
from gui.horario_panel import HorarioPanel

class MainWindow(tk.Frame):
    def __init__(self, root, mediator, sala_service=None, reserva_service=None, user=None, user_service=None, on_login=None):
        super().__init__(root)
        self.root = root
        self.mediator = mediator
        self.sala_service = sala_service
        self.reserva_service = reserva_service
        self.user = user
        self.user_service = user_service
        self.on_login = on_login
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

        # Barra lateral mejorada y moderna
        sidebar = tk.Frame(self, width=240, bg="#232946")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo y nombre del sistema
        logo_frame = tk.Frame(sidebar, bg="#232946")
        logo_frame.pack(pady=(30, 10))
        logo_icon = tk.Label(logo_frame, text="🏢", font=("Arial", 38), bg="#232946", fg="#eebbc3")
        logo_icon.pack()
        logo_label = tk.Label(logo_frame, text="Smart-Rooms", font=("Arial", 20, "bold"), bg="#232946", fg="#eebbc3")
        logo_label.pack()

        # Línea decorativa
        tk.Frame(sidebar, bg="#eebbc3", height=2).pack(fill="x", padx=30, pady=(10, 20))

        # Botones de navegación con iconos y estilos
        style = ttk.Style()
        style.configure("Sidebar.TButton",
                        font=("Arial", 13, "bold"),
                        foreground="#232946",
                        background="#eebbc3",
                        padding=10,
                        borderwidth=0)
        style.map("Sidebar.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        nav_frame = tk.Frame(sidebar, bg="#232946")
        nav_frame.pack(pady=(10, 10), fill="x")

        if self.user and self.user.role == "admin":
            dashboard_btn = ttk.Button(nav_frame, text="📊 Dashboard", style="Sidebar.TButton", command=self.ver_dashboard)
            dashboard_btn.pack(fill="x", pady=8, padx=30)
            admin_btn = ttk.Button(nav_frame, text="👤 Usuarios", style="Sidebar.TButton", command=self.ver_admin_panel)
            admin_btn.pack(fill="x", pady=8, padx=30)
            salas_btn = ttk.Button(nav_frame, text="🏢 Salas", style="Sidebar.TButton", command=self.ver_salas)
            salas_btn.pack(fill="x", pady=8, padx=30)

        reservas_btn = ttk.Button(nav_frame, text="📅 Reservas", style="Sidebar.TButton", command=self.ver_reservas)
        reservas_btn.pack(fill="x", pady=8, padx=30)

        # Botón Horario entre Reservas y Salir
        horario_btn = ttk.Button(nav_frame, text="⏰ Horario", style="Sidebar.TButton", command=self.ver_horario)
        horario_btn.pack(fill="x", pady=8, padx=30)

        salir_btn = ttk.Button(nav_frame, text="🚪 Salir", style="Sidebar.TButton", command=self.salir_sistema)
        salir_btn.pack(fill="x", pady=8, padx=30)

        # Separador decorativo
        sep = tk.Frame(sidebar, bg="#eebbc3", height=2)
        sep.pack(fill="x", padx=30, pady=30)

        # Información o pie de página
        info_label = tk.Label(sidebar, text="© 2025 Smart-Rooms", font=("Arial", 10), bg="#232946", fg="#eebbc3")
        info_label.pack(side="bottom", pady=18)

        # Área principal con fondo y bienvenida
        self.main_frame = tk.Frame(self, bg="#f4f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True)
        self.mostrar_bienvenida()

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
        salas_panel = SalasPanel(
            self.main_frame,
            self.mediator,
            self.sala_service,
            on_volver=lambda: self.seleccionar_seccion("dashboard")
        )
        salas_panel.pack(fill="both", expand=True)

    def ver_reservas(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        if self.user and self.user.role in ("estudiante", "profesor"):
            reservas_panel = MisReservasPanel(self.main_frame, self.reserva_service, self.user)
        else:
            reservas_panel = ReservasPanel(
                parent=self.main_frame,
                mediator=self.mediator,
                sala_service=self.sala_service,
                user_service=self.user_service,
                reserva_service=self.reserva_service
            )
        reservas_panel.pack(fill="both", expand=True)

    def ver_admin_panel(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        admin_panel = AdminPanel(
            self.main_frame,
            self.mediator,
            self.user_service,
            on_volver=lambda: self.seleccionar_seccion("dashboard")
        )
        admin_panel.pack(fill="both", expand=True)

    def ver_dashboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        dashboard = DashboardPanel(self.main_frame, sala_service=self.sala_service, reserva_service=self.reserva_service, user_service=self.user_service)
        dashboard.pack(fill="both", expand=True)

    def salir_sistema(self):
        self.root.destroy()

    def cerrar_sesion(self):
        self.root.withdraw()  # Oculta la ventana principal
        from gui.login_window import LoginWindow
        LoginWindow(self.root, self.user_service, self.on_login)
        self.destroy()  # Destruye el frame actual, pero NO root

    def seleccionar_seccion(self, seccion):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        panel = None

        if seccion == "dashboard":
            panel = DashboardPanel(self.main_frame, self.sala_service)
        elif seccion == "reservas":
            if self.user and self.user.role in ("estudiante", "profesor"):
                panel = MisReservasPanel(self.main_frame, self.reserva_service, self.user)
            else:
                panel = ReservasPanel(self.main_frame, self.mediator, self.reserva_service, on_volver=lambda: self.seleccionar_seccion("dashboard"))
        elif seccion == "salas":
            panel = SalasPanel(self.main_frame, self.mediator, self.sala_service, on_volver=lambda: self.seleccionar_seccion("dashboard"))
        elif seccion == "usuarios":
            panel = AdminPanel(self.main_frame, self.mediator, self.user_service, on_volver=lambda: self.seleccionar_seccion("dashboard"))
        # ...otros paneles si tienes...

        if panel is not None:
            panel.pack(fill="both", expand=True)

    def ver_horario(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        panel = HorarioPanel(self.main_frame, reserva_service=self.reserva_service, user=self.user)
        panel.pack(fill="both", expand=True)

    def ver_mis_reservas(self):
        # Elimina el panel actual si es necesario
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Crea el panel de reservas del usuario actual
        panel = MisReservasPanel(self.main_frame, self.reserva_service, self.user)
        panel.pack(fill="both", expand=True)