import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar  # Asegúrate de importar Calendar

class SistemaGestionSalas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        
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
        menu_opciones = [
            ("Inicio", "home", self.mostrar_inicio),
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas),
            ("Calendario", "calendar", self.mostrar_calendario),
            ("Salas", "door-open", self.mostrar_salas),
            ("Reportes", "file-text", self.mostrar_reportes),
            ("Configuración", "settings", self.mostrar_config)
        ]
        
        for texto, icono, comando in menu_opciones:
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
        
        # Inicializar la lista de salas
        self.salas = [
            (1, "A101", 30, "Disponible"),
            (2, "B205", 50, "En Mantenimiento"),
            (3, "C302", 20, "Disponible")
        ]
        
        # Inicializar la lista de reservas
        self.reservas = []  # Aquí se guardarán las reservas realizadas
        
        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()
    
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
        
        resumen_data = [
            {"title": "Salas Disponibles", "value": "24", "color": self.color_principal},
            {"title": "Reservas Hoy", "value": "18", "color": self.color_exito},
            {"title": "En Mantenimiento", "value": "3", "color": self.color_advertencia},
            {"title": "Ocupación Total", "value": "78%", "color": "#6c757d"}
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
        
        # Sección de acciones rápidas
        tk.Label(self.content_frame, 
                text="Acciones Rápidas", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))
        
        acciones_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        acciones_frame.pack(fill="x", pady=(0, 30))
        
        acciones = [
            {"text": "Nueva Reserva", "command": self.mostrar_reservas, "color": self.color_principal},
            {"text": "Ver Calendario", "command": self.mostrar_calendario, "color": "#17a2b8"},
            {"text": "Reportar Problema", "command": self.reportar_problema, "color": self.color_advertencia}
        ]
        
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
        
        # Datos de ejemplo
        reservas = [
            ("A101", "Juan Pérez", "15/06/2023", "08:00-10:00", "Confirmada"),
            ("B205", "María Gómez", "15/06/2023", "10:00-12:00", "Pendiente"),
            ("C302", "Carlos Ruiz", "16/06/2023", "14:00-16:00", "Confirmada")
        ]
        
        for reserva in reservas:
            self.tree_reservas.insert("", "end", values=reserva)
    
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
            {"label": "Sala a Reservar", "type": "combobox", "values": ["A101", "B205", "C302", "D404"]},
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
                entry = Calendar(scrollable_frame, selectmode="day", date_pattern="dd/mm/yyyy")
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
        sala = self.entries["Sala a Reservar"].get()
        fecha = self.entries["Fecha de Reserva"].get_date()
        hora_inicio = self.entries["Hora Inicio"].get()
        hora_termino = self.entries["Hora Término"].get()
        motivo = self.entries["Motivo"].get("1.0", "end").strip()
        
        if not responsable or not sala or not fecha or not hora_inicio or not hora_termino or not motivo:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return
        
        # Validar que la hora de inicio sea anterior a la hora de término
        try:
            hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
            hora_termino_dt = datetime.strptime(hora_termino, "%H:%M")
            if hora_inicio_dt >= hora_termino_dt:
                messagebox.showerror("Error", "La hora de inicio debe ser anterior a la hora de término.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Usa HH:MM.")
            return
        
        # Verificar conflictos de reserva
        if not self.verificar_conflictos(sala, fecha, hora_inicio, hora_termino):
            messagebox.showerror("Error", "Conflicto de horario con otra reserva existente.")
            return
        
        # Guardar la reserva en la lista
        nueva_reserva = {
            "sala": sala,
            "responsable": responsable,
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_termino": hora_termino,
            "motivo": motivo
        }
        self.reservas.append(nueva_reserva)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Reserva Guardada", f"Reserva para la sala {sala} creada correctamente.")
        self.mostrar_inicio()
    
    def verificar_conflictos(self, sala, fecha, hora_inicio, hora_termino):
        # Verificar si hay conflictos con las reservas existentes
        for reserva in self.reservas:
            if reserva["sala"] == sala and reserva["fecha"] == fecha:
                inicio_reserva = datetime.strptime(reserva["hora_inicio"], "%H:%M")
                termino_reserva = datetime.strptime(reserva["hora_termino"], "%H:%M")
                nuevo_inicio = datetime.strptime(hora_inicio, "%H:%M")
                nuevo_termino = datetime.strptime(hora_termino, "%H:%M")
                
                if not (nuevo_termino <= inicio_reserva or nuevo_inicio >= termino_reserva):
                    return False  # Hay conflicto
        return True  # No hay conflicto

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_calendario(self):
        self.limpiar_contenido()
        
        # Título
        tk.Label(self.content_frame, 
                 text="Reservas", 
                 font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Tabla de reservas
        columns = ("Sala", "Responsable", "Fecha", "Hora", "Motivo")
        tree_reservas = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree_reservas.heading(col, text=col)
            tree_reservas.column(col, width=120, anchor="center")
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree_reservas.yview)
        tree_reservas.configure(yscrollcommand=scrollbar.set)
        tree_reservas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar las reservas actuales
        for reserva in self.reservas:
            tree_reservas.insert("", "end", values=(
                reserva["sala"],
                reserva["responsable"],
                reserva["fecha"],
                f"{reserva['hora_inicio']} - {reserva['hora_termino']}",
                reserva["motivo"]
            ))
    
    def mostrar_salas(self):
        self.limpiar_contenido()
        
        # Título
        tk.Label(self.content_frame, 
                 text="Gestión de Salas", 
                 font=self.titulo_font, 
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Tabla de salas
        columns = ("ID", "Nombre", "Capacidad", "Estado")
        self.tree_salas = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree_salas.heading(col, text=col)
            self.tree_salas.column(col, width=120, anchor="center")
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_salas.yview)
        self.tree_salas.configure(yscrollcommand=scrollbar.set)
        self.tree_salas.pack(fill="both", expand=True, pady=(10, 20))
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar las salas actuales
        for sala in self.salas:
            self.tree_salas.insert("", "end", values=sala)
        
        # Botones para agregar, editar y eliminar salas
        btn_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, 
                  text="Agregar Sala", 
                  font=self.boton_font, 
                  bg=self.color_principal, 
                  fg="white", 
                  padx=20, 
                  pady=10, 
                  command=self.agregar_sala).pack(side="left", padx=10)
        
        tk.Button(btn_frame, 
                  text="Editar Sala", 
                  font=self.boton_font, 
                  bg="#ffc107", 
                  fg="white", 
                  padx=20, 
                  pady=10, 
                  command=self.editar_sala).pack(side="left", padx=10)
        
        tk.Button(btn_frame, 
                  text="Eliminar Sala", 
                  font=self.boton_font, 
                  bg=self.color_advertencia, 
                  fg="white", 
                  padx=20, 
                  pady=10, 
                  command=self.eliminar_sala).pack(side="left", padx=10)

    def agregar_sala(self):
        def guardar_nueva_sala():
            nombre = entry_nombre.get()
            capacidad = entry_capacidad.get()
            estado = combo_estado.get()
            
            if not nombre or not capacidad or not estado:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            nueva_sala = (len(self.salas) + 1, nombre, int(capacidad), estado)
            self.salas.append(nueva_sala)
            self.tree_salas.insert("", "end", values=nueva_sala)
            top.destroy()
            messagebox.showinfo("Éxito", "Sala agregada correctamente.")
        
        top = tk.Toplevel(self.root)
        top.title("Agregar Sala")
        top.geometry("400x300")
        top.configure(bg="white")
        
        tk.Label(top, text="Nombre de la Sala:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        entry_nombre = tk.Entry(top, font=self.normal_font)
        entry_nombre.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(top, text="Capacidad:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        entry_capacidad = tk.Entry(top, font=self.normal_font)
        entry_capacidad.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(top, text="Estado:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        combo_estado = ttk.Combobox(top, font=self.normal_font, values=["Disponible", "En Mantenimiento"])
        combo_estado.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Button(top, text="Guardar", font=self.boton_font, bg=self.color_principal, fg="white", 
                  command=guardar_nueva_sala).pack(pady=20)

    def editar_sala(self):
        selected_item = self.tree_salas.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona una sala para editar.")
            return

        # Obtener el ID de la sala seleccionada
        sala_id = self.tree_salas.item(selected_item, "values")[0]
        sala = next((s for s in self.salas if str(s[0]) == sala_id), None)

        if not sala:
            messagebox.showerror("Error", "No se encontró la sala seleccionada.")
            return

        def guardar_cambios():
            # Obtener los valores actualizados del formulario
            nuevo_nombre = entry_nombre.get()
            nueva_capacidad = entry_capacidad.get()
            nuevo_estado = combo_estado.get()

            if not nuevo_nombre or not nueva_capacidad or not nuevo_estado:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nueva_capacidad = int(nueva_capacidad)
            except ValueError:
                messagebox.showerror("Error", "La capacidad debe ser un número.")
                return

            # Actualizar la sala en la lista self.salas
            for i, s in enumerate(self.salas):
                if s[0] == sala[0]:  # Comparar por ID
                    self.salas[i] = (s[0], nuevo_nombre, nueva_capacidad, nuevo_estado)
                    break

            # Actualizar la sala en el Treeview
            self.tree_salas.item(selected_item, values=(sala[0], nuevo_nombre, nueva_capacidad, nuevo_estado))

            # Cerrar la ventana y mostrar mensaje de éxito
            top.destroy()
            messagebox.showinfo("Éxito", "Sala editada correctamente.")

        # Crear ventana para editar la sala
        top = tk.Toplevel(self.root)
        top.title("Editar Sala")
        top.geometry("400x300")
        top.configure(bg="white")

        tk.Label(top, text="Nombre de la Sala:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        entry_nombre = tk.Entry(top, font=self.normal_font)
        entry_nombre.insert(0, sala[1])  # Nombre actual
        entry_nombre.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(top, text="Capacidad:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        entry_capacidad = tk.Entry(top, font=self.normal_font)
        entry_capacidad.insert(0, sala[2])  # Capacidad actual
        entry_capacidad.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(top, text="Estado:", font=self.normal_font, bg="white").pack(anchor="w", pady=(10, 5), padx=10)
        combo_estado = ttk.Combobox(top, font=self.normal_font, values=["Disponible", "En Mantenimiento"])
        combo_estado.set(sala[3])  # Estado actual
        combo_estado.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(top, text="Guardar", font=self.boton_font, bg=self.color_principal, fg="white",
                  command=guardar_cambios).pack(pady=20)

    def eliminar_sala(self):
        selected_item = self.tree_salas.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona una sala para eliminar.")
            return
        
        sala_id = self.tree_salas.item(selected_item, "values")[0]
        self.salas = [s for s in self.salas if str(s[0]) != sala_id]
        self.tree_salas.delete(selected_item)
        messagebox.showinfo("Éxito", "Sala eliminada correctamente.")
    
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

    def mostrar_reservas_existentes(self, sala, fecha):
        # Ejemplo de reservas existentes
        reservas = [
            {"sala": "A101", "fecha": "15/06/2023", "hora": "08:00-10:00", "responsable": "Juan Pérez"},
            {"sala": "A101", "fecha": "15/06/2023", "hora": "10:00-12:00", "responsable": "María Gómez"}
        ]
        
        reservas_filtradas = [r for r in reservas if r["sala"] == sala and r["fecha"] == fecha]
        
        if reservas_filtradas:
            messagebox.showinfo("Reservas Existentes", "\n".join([f"{r['hora']} - {r['responsable']}" for r in reservas_filtradas]))
        else:
            messagebox.showinfo("Reservas Existentes", "No hay reservas para esta sala en la fecha seleccionada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionSalas(root)
    root.mainloop()