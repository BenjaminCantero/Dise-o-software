import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database_setup import DatabaseSetup  # Importar la clase de configuración de la base de datos


class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("500x500")
        self.root.configure(bg="#2c3e50")  # Fondo más oscuro para elegancia

        # Inicializar la base de datos
        self.db = DatabaseSetup()
        self.db.inicializar_base_datos()

        # Marco principal con bordes redondeados
        frame = tk.Frame(self.root, bg="#ecf0f1", padx=30, pady=30, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(frame, text="Inicio de Sesión", font=("Segoe UI", 20, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Segoe UI", 12), bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(10, 5))
        self.entry_user = tk.Entry(frame, font=("Segoe UI", 12), relief="flat", bg="#dfe6e9", fg="#2c3e50", insertbackground="#2c3e50")
        self.entry_user.pack(fill="x", pady=5, ipady=5)

        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 12), bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(10, 5))
        self.entry_pass = tk.Entry(frame, font=("Segoe UI", 12), show="*", relief="flat", bg="#dfe6e9", fg="#2c3e50", insertbackground="#2c3e50")
        self.entry_pass.pack(fill="x", pady=5, ipady=5)

        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white",
                  activebackground="#2980b9", activeforeground="white", relief="flat",
                  command=self.validar_login).pack(pady=20, fill="x", ipady=5)

        # Pie de página
        tk.Label(self.root, text="© 2025 Gestión de Salas", font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7").pack(side="bottom", pady=10)

    def validar_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # Validar credenciales
        result = self.db.obtener_usuario(username, password)

        if result:
            role = result[0]
            messagebox.showinfo("Éxito", f"Bienvenido, {username} ({role})")
            self.root.destroy()  # Cerrar ventana de login

            # Abrir la aplicación principal
            main_root = tk.Tk()
            app = SistemaGestionSalas(main_root, role, self.db)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def __del__(self):
        self.db.cerrar_conexion()


class SistemaGestionSalas:
    def __init__(self, root, role, db):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        self.role = role
        self.db = db  # Reutilizar la conexión a la base de datos

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
        self.reservas = self.db.obtener_reservas()

        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()

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

    def mostrar_inicio(self):
        self.limpiar_contenido()

        # Título del módulo de inicio
        tk.Label(self.content_frame,
                 text="Bienvenido al Sistema de Gestión de Salas",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # ===== REPORTE COMPLETO DEL SISTEMA =====
        report_frame = tk.Frame(self.content_frame, bg=self.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        report_frame.pack(fill="x", pady=(10, 20))

        tk.Label(report_frame,
                 text="Reporte Completo del Sistema",
                 font=self.subtitulo_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="w", pady=(0, 10))

        total_salas = len(self.salas)
        salas_disponibles = sum(1 for sala in self.salas if sala[3] == "Disponible")
        salas_ocupadas = total_salas - salas_disponibles
        reservas_activas = len(self.reservas)

        tk.Label(report_frame,
                 text=f"Total de Salas: {total_salas}",
                 font=self.normal_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="w", pady=5)

        tk.Label(report_frame,
                 text=f"Salas Disponibles: {salas_disponibles}",
                 font=self.normal_font,
                 bg=self.color_fondo,
                 fg=self.color_exito).pack(anchor="w", pady=5)

        tk.Label(report_frame,
                 text=f"Salas Ocupadas: {salas_ocupadas}",
                 font=self.normal_font,
                 bg=self.color_fondo,
                 fg=self.color_advertencia).pack(anchor="w", pady=5)

        tk.Label(report_frame,
                 text=f"Reservas Activas: {reservas_activas}",
                 font=self.normal_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="w", pady=5)

        # ===== ATAJOS RÁPIDOS =====
        shortcuts_frame = tk.Frame(self.content_frame, bg=self.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        shortcuts_frame.pack(fill="x", pady=(10, 20))

        tk.Label(shortcuts_frame,
                 text="Atajos Rápidos",
                 font=self.subtitulo_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="w", pady=(0, 10))

        tk.Button(shortcuts_frame,
                  text="Reservar Sala",
                  font=self.boton_font,
                  bg=self.color_principal,
                  fg="white",
                  activebackground=self.color_secundario,
                  activeforeground="white",
                  relief="flat",
                  command=self.mostrar_reservas).pack(fill="x", pady=5, ipady=5)

        tk.Button(shortcuts_frame,
                  text="Ver Calendario",
                  font=self.boton_font,
                  bg=self.color_principal,
                  fg="white",
                  activebackground=self.color_secundario,
                  activeforeground="white",
                  relief="flat",
                  command=self.mostrar_calendario).pack(fill="x", pady=5, ipady=5)

        # ===== TABLA DE TODAS LAS SALAS =====
        table_frame = tk.Frame(self.content_frame, bg=self.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, pady=(10, 20))

        tk.Label(table_frame,
                 text="Todas las Salas",
                 font=self.subtitulo_font,
                 bg=self.color_fondo,
                 fg=self.color_texto).pack(anchor="w", pady=(0, 10))

        columns = ("ID", "Nombre", "Capacidad", "Estado")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        tree.pack(fill="both", expand=True, pady=10)

        # Configurar encabezados
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Capacidad", text="Capacidad")
        tree.heading("Estado", text="Estado")

        # Configurar ancho de columnas
        tree.column("ID", width=50, anchor="center")
        tree.column("Nombre", width=200, anchor="w")
        tree.column("Capacidad", width=100, anchor="center")
        tree.column("Estado", width=150, anchor="center")

        # Insertar datos en la tabla
        for sala in self.salas:
            tree.insert("", "end", values=sala)

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def mostrar_reservas(self):
        self.limpiar_contenido()

        # Título del módulo de reservas
        tk.Label(self.content_frame,
                 text="Reservar Sala",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Filtros
        filter_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(filter_frame, text="Filtrar por Estado:", font=self.normal_font, bg=self.color_fondo).pack(side="left", padx=5)
        estado_combo = ttk.Combobox(filter_frame, values=["Todos", "Pendiente", "Confirmada", "Cancelada"], state="readonly")
        estado_combo.set("Todos")
        estado_combo.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Fecha:", font=self.normal_font, bg=self.color_fondo).pack(side="left", padx=5)
        fecha_calendar = Calendar(filter_frame, selectmode="day", year=2025, month=4, day=22)
        fecha_calendar.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Aplicar Filtros", font=self.boton_font, bg=self.color_principal, fg="white",
                  command=lambda: self.aplicar_filtros_reservas(estado_combo.get(), fecha_calendar.get_date())).pack(side="left", padx=10)

        # Crear tabla de reservas
        self.crear_tabla_reservas()

    def aplicar_filtros_reservas(self, estado, fecha):
        reservas_filtradas = [reserva for reserva in self.reservas if
                              (estado == "Todos" or reserva[6] == estado) and reserva[3] == fecha]
        self.limpiar_contenido()
        self.crear_tabla_reservas(reservas_filtradas)

    def crear_tabla_reservas(self, reservas=None):
        if reservas is None:
            reservas = self.reservas

        # Crear tabla
        columns = ("ID", "Sala", "Responsable", "Fecha", "Hora Inicio", "Hora Término", "Estado")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, pady=10)

        # Configurar encabezados
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Insertar datos en la tabla
        for reserva in reservas:
            tree.insert("", "end", values=reserva)

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def realizar_reserva(self, sala, responsable, fecha, hora_inicio, hora_termino):
        if not sala or not responsable or not fecha or not hora_inicio or not hora_termino:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        sala_id = next((s[0] for s in self.salas if s[1] == sala), None)
        if not sala_id:
            messagebox.showerror("Error", "La sala seleccionada no es válida.")
            return

        # Validar conflictos de horario
        for reserva in self.reservas:
            if reserva[1] == sala and reserva[3] == fecha:
                if not (hora_termino <= reserva[4] or hora_inicio >= reserva[5]):
                    messagebox.showerror("Error", "La sala ya está reservada en este horario.")
                    return

        try:
            # Insertar la reserva con estado inicial "Pendiente"
            self.db.insertar_reserva(sala_id, responsable, fecha, hora_inicio, hora_termino, "Pendiente", self.role)
            messagebox.showinfo("Éxito", f"Reserva realizada para la sala {sala}. Estado: Pendiente.")
            self.salas = self.db.obtener_salas()
            self.reservas = self.db.obtener_reservas()
            self.mostrar_inicio()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la reserva: {e}")

    def mostrar_calendario(self):
        self.limpiar_contenido()

        # Título del módulo de calendario
        tk.Label(self.content_frame,
                 text="Calendario de Reservas",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Crear un calendario interactivo
        calendar = Calendar(self.content_frame, selectmode="day", year=2025, month=4, day=21)
        calendar.pack(pady=20)

        # Botón para consultar reservas en la fecha seleccionada
        tk.Button(self.content_frame,
                  text="Consultar Reservas",
                  font=self.boton_font,
                  bg=self.color_principal,
                  fg="white",
                  activebackground=self.color_secundario,
                  activeforeground="white",
                  relief="flat",
                  command=lambda: self.consultar_reservas_fecha(calendar.get_date())).pack(pady=10)

    def consultar_reservas_fecha(self, fecha):
        self.limpiar_contenido()

        # Título del módulo de reservas por fecha
        tk.Label(self.content_frame,
                 text=f"Reservas para la Fecha: {fecha}",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Crear tabla para mostrar reservas
        columns = ("ID", "Sala", "Responsable", "Hora Inicio", "Hora Término", "Estado")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, pady=10)

        # Configurar encabezados y ancho de columnas
        for col in columns:
            tree.heading(col, text=col)
            if col in ["Hora Inicio", "Hora Término"]:
                tree.column(col, width=120, anchor="center")  # Ajustar ancho para mostrar horas completas
            else:
                tree.column(col, width=100, anchor="center", stretch=True)  # Otras columnas con ajuste flexible

        # Filtrar reservas por la fecha seleccionada
        reservas_fecha = [reserva for reserva in self.reservas if reserva[3] == fecha]

        # Depurar datos
        print("Reservas filtradas:", reservas_fecha)

        # Insertar datos en la tabla
        for reserva in reservas_fecha:
            # Asegúrate de que los datos estén en el orden correcto
            tree.insert("", "end", values=(reserva[0], reserva[1], reserva[2], reserva[4], reserva[5], reserva[6]))

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Mostrar mensaje si no hay reservas
        if not reservas_fecha:
            tk.Label(self.content_frame,
                     text="No hay reservas para esta fecha.",
                     font=self.normal_font,
                     bg=self.color_fondo,
                     fg=self.color_advertencia).pack(anchor="nw", pady=(10, 0))

    def mostrar_salas(self):
        self.limpiar_contenido()

        # Título del módulo de salas
        tk.Label(self.content_frame,
                 text="Salas Disponibles y Reservadas",
                 font=self.titulo_font,
                 bg=self.color_fondo,
                 fg=self.color_principal).pack(anchor="nw", pady=(0, 20))

        # Crear tabla
        columns = ("ID", "Nombre", "Capacidad", "Estado")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, pady=10)

        # Configurar encabezados
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Capacidad", text="Capacidad")
        tree.heading("Estado", text="Estado")

        # Configurar ancho de columnas
        tree.column("ID", width=50, anchor="center")
        tree.column("Nombre", width=200, anchor="w")
        tree.column("Capacidad", width=100, anchor="center")
        tree.column("Estado", width=150, anchor="center")

        # Obtener datos de las salas
        for sala in self.salas:
            tree.insert("", "end", values=sala)

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

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
        # Generar un reporte básico de salas
        reporte = "Reporte de Salas:\n\n"
        for sala in self.salas:
            reporte += f"ID: {sala[0]}, Nombre: {sala[1]}, Capacidad: {sala[2]}, Estado: {sala[3]}\n"

        # Mostrar el reporte en un cuadro de diálogo
        messagebox.showinfo("Reporte de Salas", reporte)

    def generar_reporte_reservas(self):
        # Generar un reporte básico de reservas
        reporte = "Reporte de Reservas:\n\n"
        for reserva in self.reservas:
            reporte += f"ID: {reserva[0]}, Sala: {reserva[1]}, Responsable: {reserva[2]}, Fecha: {reserva[3]}, " \
                       f"Hora Inicio: {reserva[4]}, Hora Término: {reserva[5]}, Estado: {reserva[6]}\n"

        # Mostrar el reporte en un cuadro de diálogo
        messagebox.showinfo("Reporte de Reservas", reporte)

    def mostrar_config(self):
        pass  # Implementar lógica para mostrar configuración

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    login = LoginSistema(root)
    root.mainloop()
