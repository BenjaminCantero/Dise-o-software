import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar


class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x400")
        self.root.configure(bg="#343a40")
        
        # Conexión a la base de datos
        self.conn = sqlite3.connect('gestion_salas.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla de usuarios si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        # Crear tabla de salas si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                capacidad INTEGER NOT NULL,
                estado TEXT NOT NULL
            )
        ''')
        
        # Crear tabla de reservas si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sala_id INTEGER NOT NULL,
                responsable TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_termino TEXT NOT NULL,
                motivo TEXT NOT NULL,
                FOREIGN KEY (sala_id) REFERENCES salas (id)
            )
        ''')
        self.conn.commit()
        
        # Insertar usuarios predeterminados si no existen
        self.cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('admin', 'admin123', 'admin')")
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('profesor', 'profesor123', 'profesor')")
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('estudiante', 'estudiante123', 'estudiante')")
            self.conn.commit()
        
        # Marco principal
        frame = tk.Frame(self.root, bg="#495057", padx=20, pady=20, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        tk.Label(frame, text="Inicio de Sesión", font=("Segoe UI", 18, "bold"), bg="#495057", fg="white").pack(pady=10)
        
        # Usuario
        tk.Label(frame, text="Usuario:", font=("Segoe UI", 12), bg="#495057", fg="white").pack(anchor="w", pady=(10, 5))
        self.entry_user = tk.Entry(frame, font=("Segoe UI", 12), relief="flat", bg="#e9ecef", fg="#495057")
        self.entry_user.pack(fill="x", pady=5)
        
        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 12), bg="#495057", fg="white").pack(anchor="w", pady=(10, 5))
        self.entry_pass = tk.Entry(frame, font=("Segoe UI", 12), show="*", relief="flat", bg="#e9ecef", fg="#495057")
        self.entry_pass.pack(fill="x", pady=5)
        
        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), bg="#007bff", fg="white", 
                  activebackground="#0056b3", activeforeground="white", relief="flat", 
                  command=self.validar_login).pack(pady=20, fill="x")
    
    def validar_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        # Validar credenciales
        self.cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        
        if result:
            role = result[0]
            messagebox.showinfo("Éxito", f"Bienvenido, {username} ({role})")
            self.root.destroy()  # Cerrar ventana de login
            
            # Abrir la aplicación principal
            main_root = tk.Tk()
            app = SistemaGestionSalas(main_root, role)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    
    def __del__(self):
        self.conn.close()

class SistemaGestionSalas:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        self.role = role

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

        # Inicializar la base de datos
        self.conectar_base_datos()
        self.cargar_salas()
        self.cargar_reservas()

        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()

    def crear_menu(self):
        # Limpiar el menú existente
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        menu_base = [
            ("Inicio", "home", self.mostrar_inicio),
            ("Calendario", "calendar", self.mostrar_calendario),
            ("Salas", "door-open", self.mostrar_salas)
        ]

        menu_admin = [
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas),
            ("Reportes", "file-text", self.mostrar_reportes),
            ("Configuración", "settings", self.mostrar_config)
        ]

        menu_profesor = [] # El profesor solo ve el menú base

        menu_estudiante = [
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas)
        ]

        menu_final = menu_base.copy()

        if self.role == "admin":
            menu_final.extend(menu_admin)
        elif self.role == "profesor":
            menu_final.extend(menu_profesor)
        elif self.role == "estudiante":
            # Insertar "Reservar Sala" después de "Inicio"
            menu_final.insert(1, ("Reservar Sala", "calendar-plus", self.mostrar_reservas))

        for texto, icono, comando in menu_final:
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

    def conectar_base_datos(self):
        self.conn = sqlite3.connect('gestion_salas.db')
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                capacidad INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Disponible'
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sala_id INTEGER NOT NULL,
                responsable TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_termino TEXT NOT NULL,
                motivo TEXT,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                FOREIGN KEY (sala_id) REFERENCES salas(id)
            )
        ''')
        self.conn.commit()

    def cargar_salas(self):
        self.cursor.execute("SELECT * FROM salas")
        self.salas = self.cursor.fetchall()

    def cargar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        self.reservas = self.cursor.fetchall()

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()

        # Título principal
        tk.Label(self.content_frame,
                 text="Panel Principal",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))

        # Tarjetas resumen
        resumen_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        resumen_frame.pack(fill="x", pady=(0, 30))

        salas_disponibles = len([sala for sala in self.salas if sala[3] == "Disponible"])
        reservas_hoy = len([reserva for reserva in self.reservas if reserva[3] == datetime.now().strftime("%Y-%m-%d")])
        en_mantenimiento = len([sala for sala in self.salas if sala[3] == "En Mantenimiento"])
        ocupacion_total = "N/A" # Necesitaríamos lógica más compleja para calcular esto

        resumen_data = [
            {"title": "Salas Disponibles", "value": str(salas_disponibles), "color": self.color_principal},
            {"title": "Reservas Hoy", "value": str(reservas_hoy), "color": self.color_exito},
            {"title": "En Mantenimiento", "value": str(en_mantenimiento), "color": self.color_advertencia},
            {"title": "Ocupación Total", "value": ocupacion_total, "color": "#6c757d"}
        ]

        for i, data in enumerate(resumen_data):
            card = tk.Frame(resumen_frame, bg="white", bd=1, relief="solid",
                            highlightbackground=self.color_borde, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=5)

            tk.Label(card,
                     text=data["title"],
                     font=self.normal_font,
                     bg="white").pack(pady=(15, 5), padx=10, anchor="w")

            tk.Label(card,
                     text=data["value"],
                     font=("Segoe UI", 24, "bold"),
                     fg=data["color"],
                     bg="white").pack(pady=(0, 15), padx=10, anchor="w")

        # Sección de acciones rápidas (dependiendo del rol)
        tk.Label(self.content_frame,
                 text="Acciones Rápidas",
                 font=self.subtitulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))

        acciones_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        acciones_frame.pack(fill="x", pady=(0, 30))

        acciones = []
        if self.role == "admin" or self.role == "estudiante":
            acciones.append({"text": "Nueva Reserva", "command": self.mostrar_reservas, "color": self.color_principal})
        acciones.append({"text": "Ver Calendario", "command": self.mostrar_calendario, "color": "#17a2b8"})
        acciones.append({"text": "Ver Salas", "command": self.mostrar_salas, "color": "#28a745"})
        if self.role == "admin":
            acciones.append({"text": "Reportar Problema", "command": self.reportar_problema, "color": self.color_advertencia})

        for accion in acciones:
            btn = tk.Button(acciones_frame,
                            text=accion["text"],
                            font=self.boton_font,
                            bg=accion["color"],
                            fg="white",
                            activebackground=accion["color"],
                            relief="solid",
                            padx=20,
                            pady=10,
                            command=accion["command"])
            btn.pack(side="left", padx=10)

        # Sección de últimas reservas
        tk.Label(self.content_frame,
                 text="Últimas Reservas",
                 font=self.subtitulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))

        # Tabla de reservas recientes
        columns = ("Sala", "Responsable", "Fecha", "Hora", "Estado")
        self.tree_reservas = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=120, anchor="center")

        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scrollbar.set)
        self.tree_reservas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar las reservas actuales
        for reserva in self.reservas:
            self.cursor.execute("SELECT nombre FROM salas WHERE id = ?", (reserva[1],))
            sala_nombre = self.cursor.fetchone()[0]
            self.tree_reservas.insert("", "end", values=(
                sala_nombre,
                reserva[2],
                reserva[3],
                f"{reserva[4]} - {reserva[5]}",
                reserva[6]
            ))

    def mostrar_reservas(self):
        self.limpiar_contenido()

        # Título
        tk.Label(self.content_frame,
                 text="Nueva Reserva de Sala",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))

        # Contenedor con scroll
        canvas = tk.Canvas(self.content_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        # Configurar el canvas y el frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Campos del formulario
        campos = [
            {"label": "Responsable", "type": "entry"},
            {"label": "Sala a Reservar", "type": "combobox", "values": [sala[1] for sala in self.salas]},
            {"label": "Fecha de Reserva", "type": "calendar"},
            {"label": "Hora Inicio", "type": "combobox", "values": [f"{h:02d}:00" for h in range(8, 21)]},
            {"label": "Hora Término", "type": "combobox", "values": [f"{h:02d}:00" for h in range(8, 21)]},
            {"label": "Motivo", "type": "text"}
        ]

        self.entries = {}
        for campo in campos:
            tk.Label(scrollable_frame, text=f"{campo['label']}:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5))

            if campo["type"] == "entry":
                entry = tk.Entry(scrollable_frame, font=self.normal_font)
            elif campo["type"] == "combobox":
                entry = ttk.Combobox(scrollable_frame, font=self.normal_font, values=campo.get("values", []))
            elif campo["type"] == "calendar":
                entry = Calendar(scrollable_frame, selectmode="day", date_pattern="yyyy-mm-dd") # Formato para la base de datos
            elif campo["type"] == "text":
                entry = tk.Text(scrollable_frame, font=self.normal_font, height=4, width=40)

            entry.pack(fill="x", pady=(0, 10))
            self.entries[campo["label"]] = entry

        # Botones del formulario
        btn_frame = tk.Frame(scrollable_frame, bg="white", pady=20)
        btn_frame.pack(fill="x", side="bottom")

        tk.Button(btn_frame, text="Cancelar", font=self.boton_font, bg="#6c757d", fg="white", padx=20, pady=8, command=self.mostrar_inicio).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Reservar Sala", font=self.boton_font, bg=self.color_principal, fg="white", padx=20, pady=8, command=self.guardar_reserva).pack(side="right", padx=10)

    def guardar_reserva(self):
        # Validar campos y guardar la reserva
        responsable = self.entries["Responsable"].get()
        sala_nombre = self.entries["Sala a Reservar"].get()
        fecha = self.entries["Fecha de Reserva"].get_date()
        hora_inicio = self.entries["Hora Inicio"].get()
        hora_termino = self.entries["Hora Término"].get()
        motivo = self.entries["Motivo"].get("1.0", "end").strip()

        # Validar campos obligatorios
        if not responsable or not sala_nombre or not fecha or not hora_inicio or not hora_termino:
            tk.messagebox.showerror("Error", "Todos los campos obligatorios deben ser completados")
            return

        # Validar que la hora de término sea posterior a la hora de inicio
        if hora_inicio >= hora_termino:
            tk.messagebox.showerror("Error", "La hora de término debe ser posterior a la hora de inicio")
            return

        try:
            # Obtener el ID de la sala
            self.cursor.execute("SELECT id FROM salas WHERE nombre = ?", (sala_nombre,))
            sala_id = self.cursor.fetchone()[0]

            # Insertar la reserva en la base de datos
            self.cursor.execute('''
                INSERT INTO reservas (sala_id, responsable, fecha, hora_inicio, hora_termino, motivo, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sala_id, responsable, fecha, hora_inicio, hora_termino, motivo, "Pendiente"))
            
            self.conn.commit()
            tk.messagebox.showinfo("Éxito", "Reserva creada correctamente")
            self.cargar_reservas()
            self.mostrar_inicio()
            
        except Exception as e:
            self.conn.rollback()
            tk.messagebox.showerror("Error", f"No se pudo crear la reserva: {str(e)}")

    def mostrar_calendario(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Calendario de Reservas",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Aquí iría la implementación del calendario

    def mostrar_salas(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Listado de Salas",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Aquí iría la implementación del listado de salas

    def mostrar_reportes(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Reportes",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Aquí iría la implementación de reportes

    def mostrar_config(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Configuración",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Aquí iría la implementación de configuración

    def reportar_problema(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Reportar Problema",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Aquí iría la implementación para reportar problemas


#---------------------------------------------------------------------------------------
# Clase para mostrar reportes y estadísticas
#---------------------------------------------------------------------------------------


    def mostrar_reportes(self):
        self.limpiar_contenido()
        
        tk.Label(self.content_frame, 
                 text="Reportes y Estadísticas", 
                 font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        tk.Label(self.content_frame, 
                 text="Ocupación Total: 78%", 
                 font=self.subtitulo_font, 
                 bg=self.color_fondo, 
                 fg=self.color_principal).pack(anchor="nw", pady=(10, 20))
        
        tk.Label(self.content_frame, 
                 text="Salas en Mantenimiento: 3", 
                 font=self.subtitulo_font, 
                 bg=self.color_fondo, 
                 fg=self.color_advertencia).pack(anchor="nw", pady=(10, 20))


#---------------------------------------------------------------------------------------
# Clase para mostrar configuración del sistema
#---------------------------------------------------------------------------------------


    def mostrar_config(self):
        self.limpiar_contenido()
        
        # Título
        tk.Label(self.content_frame, 
                 text="Configuración del Sistema", 
                 font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        config_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20, 
                                highlightbackground=self.color_borde, highlightthickness=1)
        config_frame.pack(fill="both", expand=True, pady=(10, 20))
        
        # Cambiar idioma
        tk.Label(config_frame, 
                 text="Idioma:", 
                 font=self.normal_font, 
                 bg="white").pack(anchor="nw", pady=(10, 5))
        
        idioma_combo = ttk.Combobox(config_frame, font=self.normal_font, values=["Español", "Inglés"])
        idioma_combo.set("Español")
        idioma_combo.pack(anchor="nw", pady=(0, 10))
        
        # Botón para guardar cambios
        tk.Button(config_frame, 
                  text="Guardar Cambios", 
                  font=self.boton_font, 
                  bg=self.color_principal, 
                  fg="white", 
                  padx=20, 
                  pady=10, 
                  command=lambda: self.guardar_idioma(idioma_combo.get())).pack(anchor="nw", pady=(20, 10))
        
        # Botón para restablecer configuración
        tk.Button(config_frame, 
                  text="Restablecer Configuración", 
                  font=self.boton_font, 
                  bg=self.color_advertencia, 
                  fg="white", 
                  padx=20, 
                  pady=10, 
                  command=self.restablecer_config).pack(anchor="nw", pady=(20, 10))

    def restablecer_config(self):
        self.color_principal = "#007bff"
        self.color_fondo = "#f8f9fa"
        self.root.configure(bg=self.color_fondo)
        messagebox.showinfo("Configuración", "Configuración restablecida a los valores predeterminados.")
        self.mostrar_inicio()

    def guardar_config(self, nuevo_color):
        self.color_principal = nuevo_color
        messagebox.showinfo("Configuración", "Cambios guardados correctamente.")
    
    def guardar_idioma(self, idioma):
        if idioma == "Español":
            messagebox.showinfo("Configuración", "Idioma cambiado a Español.")
        elif idioma == "Inglés":
            messagebox.showinfo("Configuración", "Language changed to English.")

#   --------------------------------------------------------------------------------------
#   Clase para reportar problemas
#   --------------------------------------------------------------------------------------

    def reportar_problema(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Reportar Problema", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación de reporte de problemas
        tk.Label(self.content_frame, 
                text="Formulario en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)

    def __del__(self):
        self.conn.close()  # Cerrar la conexión a la base de datos al destruir la instancia

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginSistema(root)
    root.mainloop()
