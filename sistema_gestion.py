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
        self.reservas = self.db.obtener_reservas(self.role, self.username)  # Pasar role y username

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

    def configurar_interfaz(self):
        # Implementar la configuración de la interfaz aquí
        pass

    def mostrar_inicio(self):
        # Implementar la lógica para mostrar el inicio
        pass

    def mostrar_reservas(self):
        # Implementar la lógica para mostrar reservas
        pass

    def mostrar_calendario(self):
        # Implementar la lógica para mostrar el calendario
        pass

    def limpiar_contenido(self):
        # Implementar la lógica para limpiar el contenido
        pass

    def crear_menu(self):
        # Limpiar el menú existente
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Opciones base para todos los usuarios
        menu_base = [
            ("Inicio", self.mostrar_inicio),
            ("Calendario", self.mostrar_calendario)
        ]

        # Opciones específicas por rol
        menu_admin = [
            ("Reservar Sala", self.mostrar_reservas),
            ("Reportes", self.mostrar_reportes),
            ("Configuración", self.mostrar_config)
        ]

        menu_profesor = [
            ("Reservar Sala", self.mostrar_reservas)
        ]

        menu_estudiante = [
            ("Reservar Sala", self.mostrar_reservas)
        ]

        # Construir el menú final según el rol
        menu_final = menu_base.copy()

        if self.role == "admin":
            menu_final.extend(menu_admin)
        elif self.role == "profesor":
            menu_final.extend(menu_profesor)
        elif self.role == "estudiante":
            menu_final.insert(1, ("Reservar Sala", self.mostrar_reservas))

        # Crear los botones del menú
        for texto, comando in menu_final:
            btn = tk.Button(self.sidebar,
                            text=f"  {texto}",
                            font=self.normal_font,
                            bg=self.color_sidebar,
                            fg="white",
                            activebackground=self.color_secundario,
                            activeforeground="white",
                            anchor="w",
                            padx=15,
                            pady=12,
                            relief="flat",
                            command=comando)
            btn.pack(fill="x", padx=5)

    def mostrar_reportes(self):
        self.limpiar_contenido()

        # Título del módulo de reportes
        tk.Label(self.content_frame,
                 text="Reportes del Sistema",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Panel para mostrar opciones de reportes
        report_frame = tk.Frame(self.content_frame, bg=self.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        report_frame.pack(fill="x", pady=(10, 20))

        tk.Label(report_frame,
                 text="Seleccione el tipo de reporte:",
                 font=self.subtitulo_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="w", pady=(0, 10))

        # Botones para generar reportes
        tk.Button(report_frame,
                  text="Reporte de Salas",
                  font=self.boton_font,
                  bg=self.color_principal,
                  fg="white",
                  activebackground=self.color_secundario,
                  activeforeground="white",
                  relief="flat",
                  command=self.generar_reporte_salas).pack(fill="x", pady=5, ipady=5)

        tk.Button(report_frame,
                  text="Reporte de Reservas",
                  font=self.boton_font,
                  bg=self.color_principal,
                  fg="white",
                  activebackground=self.color_secundario,
                  activeforeground="white",
                  relief="flat",
                  command=self.generar_reporte_reservas).pack(fill="x", pady=5, ipady=5)

    def generar_reporte_salas(self):
        try:
            # Obtener datos de las salas desde la base de datos
            salas = self.db.obtener_salas()

            # Generar el reporte
            reporte = "Reporte de Salas:\n\n"
            for sala in salas:
                reporte += f"ID: {sala[0]}, Nombre: {sala[1]}, Capacidad: {sala[2]}, Estado: {sala[3]}\n"

            # Mostrar el reporte en un cuadro de diálogo
            messagebox.showinfo("Reporte de Salas", reporte)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte de salas: {e}")

    def generar_reporte_reservas(self):
        try:
            # Obtener reservas según el rol del usuario
            reservas = self.db.obtener_reservas(self.role, self.username)

            # Generar el reporte
            reporte = "Reporte de Reservas:\n\n"
            for reserva in reservas:
                reporte += f"ID: {reserva[0]}, Sala: {reserva[1]}, Responsable: {reserva[2]}, Fecha: {reserva[3]}, " \
                           f"Hora Inicio: {reserva[4]}, Hora Término: {reserva[5]}, Estado: {reserva[6]}\n"

            # Mostrar el reporte en un cuadro de diálogo
            messagebox.showinfo("Reporte de Reservas", reporte)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte de reservas: {e}")

    def mostrar_config(self):
        self.limpiar_contenido()

        # Título del módulo de configuración
        tk.Label(self.content_frame,
                 text="Configuración del Sistema",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Implementar lógica de configuración aquí
        tk.Label(self.content_frame,
                 text="(Opciones de configuración próximamente...)",
                 font=self.normal_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="nw", pady=(10, 0))