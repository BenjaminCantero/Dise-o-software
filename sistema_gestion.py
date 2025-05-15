# proyecto_gestion_salas/sistema_gestion.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar # type: ignore
import sqlite3
from database_setup import get_db_connection # Using the centralized connection getter
from utils import color_palette, font_styles

class SistemaGestionSalas:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg=color_palette["fondo"])
        self.role = role

        # Paleta de colores y fuentes desde utils
        self.color_fondo = color_palette["fondo"]
        self.color_sidebar = color_palette["sidebar"]
        self.color_principal = color_palette["principal"]
        self.color_secundario = color_palette["secundario"]
        self.color_exito = color_palette["exito"]
        self.color_advertencia = color_palette["advertencia"]
        self.color_texto = color_palette["texto"]
        self.color_borde = color_palette["borde"]

        self.titulo_font = font_styles["titulo"]
        self.subtitulo_font = font_styles["subtitulo"]
        self.normal_font = font_styles["normal"]
        self.boton_font = font_styles["boton"]

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.color_fondo)
        self.style.configure("TLabel", background=self.color_fondo,
                             foreground=self.color_texto, font=self.normal_font)
        self.style.configure("TButton", font=self.boton_font,
                             borderwidth=1, relief="solid")
        self.style.map("TButton",
                       foreground=[("active", "white")],
                       background=[("active", self.color_secundario)])

        self.main_frame = tk.Frame(root, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Gestión de Salas", font=font_styles["sidebar_titulo"],
                 bg=self.color_sidebar, fg="white", pady=20).pack(fill="x")
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)
        self.crear_menu()
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)
        tk.Label(self.sidebar, text="v2.0", font=font_styles["sidebar_version"],
                 bg=self.color_sidebar, fg="#adb5bd").pack(side="bottom", pady=10)

        self.content_frame = tk.Frame(self.main_frame, bg=self.color_fondo, padx=30, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.conectar_base_datos() # Connects and gets cursor
        self.cargar_salas_data() # Renamed from cargar_salas to avoid conflict with method name
        self.cargar_reservas_data() # Renamed from cargar_reservas

        self.mostrar_inicio()

    def crear_menu(self):
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
        menu_profesor = []
        # menu_estudiante defined inline below

        menu_final = menu_base.copy()

        if self.role == "admin":
            menu_final.extend(menu_admin)
        elif self.role == "profesor":
            menu_final.extend(menu_profesor) # effectively does nothing as menu_profesor is empty
        elif self.role == "estudiante":
            menu_final.insert(1, ("Reservar Sala", "calendar-plus", self.mostrar_reservas))

        for texto, icono, comando in menu_final: # icono not used currently
            btn = tk.Button(self.sidebar, text=f"  {texto}", font=self.normal_font,
                            bg=self.color_sidebar, fg="white",
                            activebackground=self.color_secundario, activeforeground="white",
                            anchor="w", padx=15, pady=12, relief="flat", command=comando)
            btn.pack(fill="x", padx=5)

    def conectar_base_datos(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        # Table creation is handled by LoginSistema or database_setup.initialize_database()
        # No need for self.crear_tablas() here if initialized before.

    def cargar_salas_data(self):
        self.cursor.execute("SELECT * FROM salas")
        self.salas_data = self.cursor.fetchall() # Stored in self.salas_data

    def cargar_reservas_data(self):
        self.cursor.execute("SELECT * FROM reservas")
        self.reservas_data = self.cursor.fetchall() # Stored in self.reservas_data

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Panel Principal", font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))

        resumen_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        resumen_frame.pack(fill="x", pady=(0, 30))

        # Ensure data is loaded
        if not hasattr(self, 'salas_data'): self.cargar_salas_data()
        if not hasattr(self, 'reservas_data'): self.cargar_reservas_data()


        salas_disponibles = len([sala for sala in self.salas_data if sala[3] == "Disponible"])
        reservas_hoy = len([reserva for reserva in self.reservas_data if reserva[3] == datetime.now().strftime("%Y-%m-%d")])
        en_mantenimiento = len([sala for sala in self.salas_data if sala[3] == "En Mantenimiento"])
        ocupacion_total = "N/A" 

        resumen_data = [
            {"title": "Salas Disponibles", "value": str(salas_disponibles), "color": self.color_principal},
            {"title": "Reservas Hoy", "value": str(reservas_hoy), "color": self.color_exito},
            {"title": "En Mantenimiento", "value": str(en_mantenimiento), "color": self.color_advertencia},
            {"title": "Ocupación Total", "value": ocupacion_total, "color": "#6c757d"}
        ]

        for data in resumen_data:
            card = tk.Frame(resumen_frame, bg="white", bd=1, relief="solid",
                            highlightbackground=self.color_borde, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=5)
            tk.Label(card, text=data["title"], font=self.normal_font, bg="white").pack(pady=(15, 5), padx=10, anchor="w")
            tk.Label(card, text=data["value"], font=("Segoe UI", 24, "bold"), fg=data["color"],
                     bg="white").pack(pady=(0, 15), padx=10, anchor="w")

        tk.Label(self.content_frame, text="Acciones Rápidas", font=self.subtitulo_font,
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
            btn = tk.Button(acciones_frame, text=accion["text"], font=self.boton_font, bg=accion["color"],
                            fg="white", activebackground=accion["color"], relief="solid",
                            padx=20, pady=10, command=accion["command"])
            btn.pack(side="left", padx=10)

        tk.Label(self.content_frame, text="Últimas Reservas", font=self.subtitulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))
        columns = ("Sala", "Responsable", "Fecha", "Hora", "Estado")
        self.tree_reservas = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scrollbar.set)
        self.tree_reservas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for reserva in self.reservas_data: # Use self.reservas_data
            self.cursor.execute("SELECT nombre FROM salas WHERE id = ?", (reserva[1],))
            sala_nombre_tuple = self.cursor.fetchone()
            sala_nombre = sala_nombre_tuple[0] if sala_nombre_tuple else "Sala Desconocida"
            self.tree_reservas.insert("", "end", values=(
                sala_nombre, reserva[2], reserva[3], f"{reserva[4]} - {reserva[5]}", reserva[7] # estado is at index 7 in new schema
            ))

    def mostrar_reservas(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Nueva Reserva de Sala", font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))

        canvas = tk.Canvas(self.content_frame, bg="white", highlightthickness=0)
        scrollbar_canvas = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview) # Renamed to avoid conflict
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_canvas.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_canvas.pack(side="right", fill="y")

        if not hasattr(self, 'salas_data'): self.cargar_salas_data()
        campos = [
            {"label": "Responsable", "type": "entry"},
            {"label": "Sala a Reservar", "type": "combobox", "values": [sala[1] for sala in self.salas_data]},
            {"label": "Fecha de Reserva", "type": "calendar"},
            {"label": "Hora Inicio", "type": "combobox", "values": [f"{h:02d}:00" for h in range(8, 21)]},
            {"label": "Hora Término", "type": "combobox", "values": [f"{h:02d}:00" for h in range(8, 21)]},
            {"label": "Motivo", "type": "text"}
        ]
        self.entries = {}
        for campo in campos:
            tk.Label(scrollable_frame, text=f"{campo['label']}:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5))
            entry_widget = None # PEP 8: assignment to entry, but never used for some types before.
            if campo["type"] == "entry":
                entry_widget = tk.Entry(scrollable_frame, font=self.normal_font)
            elif campo["type"] == "combobox":
                entry_widget = ttk.Combobox(scrollable_frame, font=self.normal_font, values=campo.get("values", []))
            elif campo["type"] == "calendar":
                entry_widget = Calendar(scrollable_frame, selectmode="day", date_pattern="yyyy-mm-dd")
            elif campo["type"] == "text":
                entry_widget = tk.Text(scrollable_frame, font=self.normal_font, height=4, width=40)
            
            if entry_widget: # Check if entry_widget was assigned
                entry_widget.pack(fill="x", pady=(0, 10))
                self.entries[campo["label"]] = entry_widget


        btn_frame = tk.Frame(scrollable_frame, bg="white", pady=20)
        btn_frame.pack(fill="x", side="bottom")
        tk.Button(btn_frame, text="Cancelar", font=self.boton_font, bg="#6c757d", fg="white", 
                  padx=20, pady=8, command=self.mostrar_inicio).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Reservar Sala", font=self.boton_font, bg=self.color_principal, 
                  fg="white", padx=20, pady=8, command=self.guardar_reserva).pack(side="right", padx=10)

    def guardar_reserva(self):
        responsable = self.entries["Responsable"].get()
        sala_nombre = self.entries["Sala a Reservar"].get()
        fecha_obj = self.entries["Fecha de Reserva"].get_date() # This is likely a datetime.date object
        fecha = fecha_obj.strftime("%Y-%m-%d") if hasattr(fecha_obj, 'strftime') else str(fecha_obj)

        hora_inicio = self.entries["Hora Inicio"].get()
        hora_termino = self.entries["Hora Término"].get()
        motivo = self.entries["Motivo"].get("1.0", "end-1c").strip() # Use end-1c to avoid extra newline

        if not all([responsable, sala_nombre, fecha, hora_inicio, hora_termino]): # motivo is optional
            messagebox.showerror("Error", "Todos los campos obligatorios (excepto motivo) deben ser completados.")
            return
        if hora_inicio >= hora_termino:
            messagebox.showerror("Error", "La hora de término debe ser posterior a la hora de inicio.")
            return

        try:
            self.cursor.execute("SELECT id FROM salas WHERE nombre = ?", (sala_nombre,))
            sala_id_tuple = self.cursor.fetchone()
            if not sala_id_tuple:
                messagebox.showerror("Error", f"Sala '{sala_nombre}' no encontrada.")
                return
            sala_id = sala_id_tuple[0]

            self.cursor.execute('''
                INSERT INTO reservas (sala_id, responsable, fecha, hora_inicio, hora_termino, motivo, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sala_id, responsable, fecha, hora_inicio, hora_termino, motivo, "Pendiente"))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Reserva creada correctamente.")
            self.cargar_reservas_data() # Recargar datos de reservas
            self.mostrar_inicio()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"No se pudo crear la reserva: {str(e)}")

    def mostrar_calendario(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Calendario de Reservas", font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        # Placeholder
        tk.Label(self.content_frame, text="Implementación del calendario en desarrollo.",
                 font=self.subtitulo_font, bg=self.color_fondo).pack(pady=100)


    def mostrar_salas(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Listado de Salas", font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        if not hasattr(self, 'salas_data'): self.cargar_salas_data()

        # Frame para la tabla de salas
        salas_table_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        salas_table_frame.pack(fill="both", expand=True, pady=(10,0))

        columns = ("ID", "Nombre", "Capacidad", "Estado")
        tree_salas = ttk.Treeview(salas_table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            tree_salas.heading(col, text=col)
            tree_salas.column(col, width=150, anchor="center")
            if col == "Nombre":
                tree_salas.column(col, width=250)

        scrollbar_salas = ttk.Scrollbar(salas_table_frame, orient="vertical", command=tree_salas.yview)
        tree_salas.configure(yscrollcommand=scrollbar_salas.set)
        
        tree_salas.pack(side="left", fill="both", expand=True)
        scrollbar_salas.pack(side="right", fill="y")

        for sala_entry in self.salas_data:
            tree_salas.insert("", "end", values=sala_entry)

        # Potentially add buttons for Add/Edit/Delete sala if admin
        if self.role == "admin":
            admin_actions_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
            admin_actions_frame.pack(pady=10)
            # Placeholder for buttons:
            # tk.Button(admin_actions_frame, text="Agregar Sala", ...).pack(side="left", padx=5)
            # tk.Button(admin_actions_frame, text="Editar Sala", ...).pack(side="left", padx=5)
            # tk.Button(admin_actions_frame, text="Eliminar Sala", ...).pack(side="left", padx=5)
            pass


    # Using the more complete definitions for reportes, config, reportar_problema
    def mostrar_reportes(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Reportes y Estadísticas", font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Example static data - In a real app, this would be calculated
        tk.Label(self.content_frame, text="Ocupación Total: 78%", font=self.subtitulo_font, 
                 bg=self.color_fondo, fg=self.color_principal).pack(anchor="nw", pady=(10, 20))
        
        if not hasattr(self, 'salas_data'): self.cargar_salas_data()
        en_mantenimiento = len([sala for sala in self.salas_data if sala[3] == "En Mantenimiento"]) # sala[3] is estado
        tk.Label(self.content_frame, text=f"Salas en Mantenimiento: {en_mantenimiento}", font=self.subtitulo_font, 
                 bg=self.color_fondo, fg=self.color_advertencia).pack(anchor="nw", pady=(10, 20))
        
        # Placeholder for more complex reports or charts
        tk.Label(self.content_frame, text="Más reportes en desarrollo.",
                 font=self.normal_font, bg=self.color_fondo).pack(pady=50)


    def mostrar_config(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Configuración del Sistema", font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        config_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20, 
                                highlightbackground=self.color_borde, highlightthickness=1)
        config_frame.pack(fill="both", expand=True, pady=(10, 20))
        
        tk.Label(config_frame, text="Idioma:", font=self.normal_font, 
                 bg="white").pack(anchor="nw", pady=(10, 5))
        
        idioma_combo = ttk.Combobox(config_frame, font=self.normal_font, values=["Español", "Inglés"])
        idioma_combo.set("Español") # Default
        idioma_combo.pack(anchor="nw", pady=(0, 10))
        
        tk.Button(config_frame, text="Guardar Cambios de Idioma", font=self.boton_font, 
                  bg=self.color_principal, fg="white", padx=20, pady=10, 
                  command=lambda: self.guardar_idioma(idioma_combo.get())).pack(anchor="nw", pady=(20, 10))
        
        # Example: Theme color change - this is simplistic
        tk.Label(config_frame, text="Color Principal (Hex):", font=self.normal_font, 
                 bg="white").pack(anchor="nw", pady=(20, 5))
        self.color_entry = tk.Entry(config_frame, font=self.normal_font)
        self.color_entry.insert(0, self.color_principal)
        self.color_entry.pack(anchor="nw", pady=(0,10))
        tk.Button(config_frame, text="Aplicar Color", font=self.boton_font, 
                  bg=self.color_principal, fg="white", padx=20, pady=10, 
                  command=lambda: self.guardar_config_color(self.color_entry.get())).pack(anchor="nw", pady=(10,10))


        tk.Button(config_frame, text="Restablecer Configuración", font=self.boton_font, 
                  bg=self.color_advertencia, fg="white", padx=20, pady=10, 
                  command=self.restablecer_config).pack(anchor="nw", pady=(20, 10))

    def restablecer_config(self):
        # Resetting color palette values from utils
        self.color_principal = color_palette["principal"] 
        self.color_fondo = color_palette["fondo"]
        # Re-configure root and potentially other elements if needed
        self.root.configure(bg=self.color_fondo) 
        # Potentially re-render or update styles
        messagebox.showinfo("Configuración", "Configuración restablecida a los valores predeterminados.")
        self.mostrar_config() # Refresh the config page to show restored values

    def guardar_config_color(self, nuevo_color):
        # Basic validation for hex color
        if not (nuevo_color.startswith("#") and len(nuevo_color) == 7):
            try:
                int(nuevo_color[1:], 16) # Check if rest is hex
            except ValueError:
                messagebox.showerror("Error", "Formato de color Hex inválido (ej: #007bff).")
                return

        self.color_principal = nuevo_color
        # Here you would update styles of relevant widgets if they don't use dynamic references
        # For simplicity, we are just storing it. A full theme change is more complex.
        messagebox.showinfo("Configuración", "Color principal actualizado. Puede requerir reiniciar para ver todos los cambios.")
        # Update button color on config page itself as an example
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, tk.Frame): # Find config_frame
                for btn_widget in widget.winfo_children():
                    if isinstance(btn_widget, tk.Button) and "Guardar" in btn_widget.cget("text") or "Aplicar" in btn_widget.cget("text"):
                        btn_widget.configure(bg=self.color_principal)
                break


    def guardar_idioma(self, idioma):
        # This is a placeholder. True internationalization is complex.
        if idioma == "Español":
            messagebox.showinfo("Configuración", "Idioma cambiado a Español.")
        elif idioma == "Inglés":
            messagebox.showinfo("Configuración", "Language changed to English.")
        # Here you would typically reload UI elements with new language strings.


    def reportar_problema(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Reportar Problema", font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Placeholder form
        tk.Label(self.content_frame, text="Tipo de Problema:", font=self.normal_font, bg=self.color_fondo).pack(anchor="nw", pady=(10,5))
        problema_tipo = ttk.Combobox(self.content_frame, font=self.normal_font, values=["Equipo Dañado", "Software", "Limpieza", "Otro"])
        problema_tipo.pack(anchor="nw", fill="x", pady=(0,10))

        tk.Label(self.content_frame, text="Descripción Detallada:", font=self.normal_font, bg=self.color_fondo).pack(anchor="nw", pady=(10,5))
        desc_text = tk.Text(self.content_frame, font=self.normal_font, height=8)
        desc_text.pack(anchor="nw", fill="both", expand=True, pady=(0,10))
        
        tk.Button(self.content_frame, text="Enviar Reporte", font=self.boton_font,
                  bg=self.color_exito, fg="white", padx=20, pady=10,
                  command=lambda: messagebox.showinfo("Reporte", "Reporte enviado (simulación).")).pack(anchor="nw", pady=(20,10))


    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()