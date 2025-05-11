import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar


class SistemaGestionSalas:
    def __init__(self, root, role, db, username):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        self.role = role
        self.db = db  # Reutilizar la conexión a la base de datos
        self.username = username

        # Inicializar datos
        self.salas = self.db.obtener_salas()
        self.reservas = self.db.obtener_reservas(self.role, self.username)

        # Paleta de colores mejorada
        self.color_fondo = "#f8f9fa"
        self.color_sidebar = "#343a40"
        self.color_principal = "#007bff"
        self.color_secundario = "#0056b3"
        self.color_exito = "#28a745"
        self.color_advertencia = "#dc3545"
        self.color_texto = "#212529"
        self.color_borde = "#dee2e6"

        # Fuentes mejoradas
        self.titulo_font = ("Segoe UI", 18, "bold")
        self.subtitulo_font = ("Segoe UI", 14)
        self.normal_font = ("Segoe UI", 11)
        self.boton_font = ("Segoe UI", 10, "bold")

        # Configurar el estilo general
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configurar estilos personalizados
        self.style.configure("TFrame", background=self.color_fondo)
        self.style.configure("TLabel", background=self.color_fondo,
                             foreground=self.color_texto, font=self.normal_font)
        self.style.configure("TButton", font=self.boton_font,
                             borderwidth=1, relief="solid")
        self.style.map("TButton",
                       foreground=[("active", "white")],
                       background=[("active", self.color_secundario)])

        # Contenedor principal
        self.main_frame = tk.Frame(root, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)

        # ===== SIDEBAR MEJORADO =====
        self.sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo o título
        tk.Label(self.sidebar,
                 text="Gestión de Salas",
                 font=("Segoe UI", 16, "bold"),
                 bg=self.color_sidebar,
                 fg="white",
                 pady=20).pack(fill="x")

        # Separador
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Opciones del menú
        self.menu_opciones = []
        self.crear_menu()

        # Separador final
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Versión del sistema
        tk.Label(self.sidebar,
                 text="v2.0",
                 font=("Segoe UI", 8),
                 bg=self.color_sidebar,
                 fg="#adb5bd").pack(side="bottom", pady=10)

        # ===== CONTENIDO PRINCIPAL =====
        self.content_frame = tk.Frame(self.main_frame, bg=self.color_fondo, padx=30, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Cargar datos iniciales
        self.salas = self.db.obtener_salas()
        self.reservas = self.db.obtener_reservas(self.role, self.username)

        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()

    # Métodos de SistemaGestionSalas
    # (Incluye todos los métodos como mostrar_inicio, mostrar_reservas, realizar_reserva, etc.)
    # Copia aquí todos los métodos de la clase SistemaGestionSalas desde el archivo original.