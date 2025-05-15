import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar

class SistemaGestionSalas:
    def __init__(self, root, role, db, username):
        self.root = root
        self.role = role
        self.db = db
        self.username = username

        # Paleta y fuentes
        self.color_fondo = "#f7fafd"
        self.color_sidebar = "#1a1a2e"
        self.color_principal = "#0f3460"
        self.color_secundario = "#e94560"
        self.color_tarjeta = "#ffffff"
        self.color_borde = "#dbe2ef"
        self.color_texto = "#22223b"
        self.titulo_font = ("Segoe UI", 22, "bold")
        self.subtitulo_font = ("Segoe UI", 14, "bold")
        self.normal_font = ("Segoe UI", 11)
        self.boton_font = ("Segoe UI", 11, "bold")

        # Estilo ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=self.normal_font, rowheight=28, background=self.color_tarjeta, fieldbackground=self.color_tarjeta, bordercolor=self.color_borde)
        style.configure("Treeview.Heading", font=self.subtitulo_font, background=self.color_principal, foreground="white")
        style.map("Treeview", background=[("selected", self.color_secundario)])

        # Layout principal
        self.root.configure(bg=self.color_fondo)
        self.main_frame = tk.Frame(self.root, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = self._crear_sidebar()
        # Contenido principal
        self.content_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Datos iniciales
        self.salas = self.db.obtener_salas()
        self.reservas = self.db.obtener_reservas(self.role, self.username)
        self.mostrar_inicio()

    # --- COMPONENTES MODULARES ---
    def _crear_sidebar(self):
        sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="Salas U", font=("Segoe UI", 20, "bold"), bg=self.color_sidebar, fg="white", pady=30).pack()
        self._sidebar_button(sidebar, "Inicio", self.mostrar_inicio)
        self._sidebar_button(sidebar, "Reservas", self.mostrar_reservas)
        self._sidebar_button(sidebar, "Calendario", self.mostrar_calendario)
        self._sidebar_button(sidebar, "Reportes", self.mostrar_reportes)
        self._sidebar_button(sidebar, "Configuración", self.mostrar_config)
        tk.Button(sidebar, text="Cerrar sesión", font=self.boton_font, bg=self.color_secundario, fg="white", relief="flat", command=self.root.destroy).pack(side="bottom", pady=20, fill="x", padx=20)
        return sidebar

    def _sidebar_button(self, parent, text, command):
        tk.Button(parent, text=text, font=self.boton_font, bg=self.color_sidebar, fg="white",
                  activebackground=self.color_principal, activeforeground="white", relief="flat",
                  bd=0, pady=15, command=command).pack(fill="x", padx=20, pady=2)

    def _tarjeta_resumen(self, parent, titulo, valor, color, col):
        frame = tk.Frame(parent, bg=self.color_tarjeta, bd=0, relief="ridge", highlightbackground=self.color_borde, highlightthickness=1)
        frame.grid(row=0, column=col, padx=20, ipadx=30, ipady=20, sticky="nsew")
        tk.Label(frame, text=titulo, font=self.normal_font, bg=self.color_tarjeta, fg=self.color_texto).pack(anchor="w")
        tk.Label(frame, text=str(valor), font=("Segoe UI", 28, "bold"), bg=self.color_tarjeta, fg=color).pack(anchor="w")

    def _tabla(self, parent, columns, data, height=10):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=height)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for row in data:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- PANELES PRINCIPALES ---
    def mostrar_inicio(self):
        self.limpiar_contenido()
        # Tarjetas resumen
        resumen_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        resumen_frame.pack(fill="x", pady=20)
        total_salas = len(self.salas)
        salas_disponibles = sum(1 for sala in self.salas if sala[3] == "Disponible")
        salas_ocupadas = total_salas - salas_disponibles
        reservas_activas = len(self.reservas)
        for i, (titulo, valor, color) in enumerate([
            ("Salas Disponibles", salas_disponibles, "#28a745"),
            ("Salas Ocupadas", salas_ocupadas, "#e94560"),
            ("Reservas Activas", reservas_activas, "#0f3460")
        ]):
            self._tarjeta_resumen(resumen_frame, titulo, valor, color, i)

        # Atajos rápidos
        atajos = tk.Frame(self.content_frame, bg=self.color_fondo)
        atajos.pack(fill="x", pady=10)
        tk.Label(atajos, text="Atajos rápidos", font=self.subtitulo_font, bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", padx=10)
        tk.Button(atajos, text="Reservar Sala", font=self.boton_font, bg=self.color_principal, fg="white", relief="flat", command=self.mostrar_reservas).pack(side="left", padx=10, ipadx=10)
        tk.Button(atajos, text="Ver Calendario", font=self.boton_font, bg=self.color_principal, fg="white", relief="flat", command=self.mostrar_calendario).pack(side="left", padx=10, ipadx=10)

        # --- Botones de gestión de salas ---
        gestion_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        gestion_frame.pack(fill="x", pady=(10, 0), padx=20)
        tk.Button(gestion_frame, text="Añadir Sala", font=self.boton_font, bg="#28a745", fg="white", relief="flat", command=self.dialogo_añadir_sala).pack(side="left", padx=5, ipadx=10)
        tk.Button(gestion_frame, text="Editar Sala", font=self.boton_font, bg="#ffc107", fg="#22223b", relief="flat", command=self.dialogo_editar_sala).pack(side="left", padx=5, ipadx=10)
        tk.Button(gestion_frame, text="Borrar Sala", font=self.boton_font, bg="#dc3545", fg="white", relief="flat", command=self.dialogo_borrar_sala).pack(side="left", padx=5, ipadx=10)

        # Tabla de salas
        tabla_frame = tk.Frame(self.content_frame, bg=self.color_tarjeta, bd=2, relief="groove")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(tabla_frame, text="Todas las Salas", font=self.subtitulo_font, bg=self.color_tarjeta, fg=self.color_texto).pack(anchor="w", pady=(10, 0), padx=10)
        columns = ("ID", "Nombre", "Capacidad", "Estado")
        self.salas_tree = self._tabla(tabla_frame, columns, self.salas, height=12)

    # --- DIALOGOS DE GESTION DE SALAS ---
    def dialogo_añadir_sala(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Añadir Sala")
        dialog.configure(bg=self.color_tarjeta)
        tk.Label(dialog, text="Nombre:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        nombre = tk.Entry(dialog, font=self.normal_font)
        nombre.pack(pady=5)
        tk.Label(dialog, text="Capacidad:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        capacidad = tk.Entry(dialog, font=self.normal_font)
        capacidad.pack(pady=5)
        tk.Label(dialog, text="Estado:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        estado = ttk.Combobox(dialog, values=["Disponible", "Reservada"], state="readonly")
        estado.set("Disponible")
        estado.pack(pady=5)
        def guardar():
            if nombre.get() and capacidad.get().isdigit():
                self.db.cursor.execute("INSERT INTO salas (nombre, capacidad, estado) VALUES (?, ?, ?)", (nombre.get(), int(capacidad.get()), estado.get()))
                self.db.conn.commit()
                self.salas = self.db.obtener_salas()
                self.mostrar_inicio()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Datos inválidos.")
        tk.Button(dialog, text="Guardar", font=self.boton_font, bg=self.color_principal, fg="white", command=guardar).pack(pady=10)

    def dialogo_editar_sala(self):
        item = self.salas_tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona una sala para editar.")
            return
        valores = self.salas_tree.item(item, "values")
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Sala")
        dialog.configure(bg=self.color_tarjeta)
        tk.Label(dialog, text="Nombre:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        nombre = tk.Entry(dialog, font=self.normal_font)
        nombre.insert(0, valores[1])
        nombre.pack(pady=5)
        tk.Label(dialog, text="Capacidad:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        capacidad = tk.Entry(dialog, font=self.normal_font)
        capacidad.insert(0, valores[2])
        capacidad.pack(pady=5)
        tk.Label(dialog, text="Estado:", font=self.normal_font, bg=self.color_tarjeta).pack(pady=5)
        estado = ttk.Combobox(dialog, values=["Disponible", "Reservada"], state="readonly")
        estado.set(valores[3])
        estado.pack(pady=5)
        def guardar():
            if nombre.get() and capacidad.get().isdigit():
                self.db.cursor.execute("UPDATE salas SET nombre=?, capacidad=?, estado=? WHERE id=?", (nombre.get(), int(capacidad.get()), estado.get(), valores[0]))
                self.db.conn.commit()
                self.salas = self.db.obtener_salas()
                self.mostrar_inicio()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Datos inválidos.")
        tk.Button(dialog, text="Guardar Cambios", font=self.boton_font, bg=self.color_principal, fg="white", command=guardar).pack(pady=10)

    def dialogo_borrar_sala(self):
        item = self.salas_tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona una sala para borrar.")
            return
        valores = self.salas_tree.item(item, "values")
        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas borrar la sala '{valores[1]}'?")
        if confirm:
            self.db.cursor.execute("DELETE FROM salas WHERE id=?", (valores[0],))
            self.db.conn.commit()
            self.salas = self.db.obtener_salas()
            self.mostrar_inicio()

    def mostrar_reservas(self):
        self.limpiar_contenido()
        frame = tk.Frame(self.content_frame, bg=self.color_tarjeta, bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        tk.Label(frame, text="Reservas Activas", font=self.titulo_font, bg=self.color_tarjeta, fg=self.color_principal).pack(anchor="nw", pady=(0, 20), padx=10)
        columns = ("ID", "Sala", "Responsable", "Fecha", "Hora Inicio", "Hora Término", "Estado")
        self._tabla(frame, columns, self.reservas, height=15)

    def mostrar_calendario(self):
        self.limpiar_contenido()
        frame = tk.Frame(self.content_frame, bg=self.color_tarjeta, bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        tk.Label(frame, text="Calendario de Reservas", font=self.titulo_font, bg=self.color_tarjeta, fg=self.color_principal).pack(anchor="nw", pady=(0, 20), padx=10)
        calendar = Calendar(frame, selectmode="day")
        calendar.pack(side="left", padx=20, pady=10)
        reservas_frame = tk.Frame(frame, bg=self.color_tarjeta)
        reservas_frame.pack(side="left", fill="both", expand=True, padx=20)
        tk.Label(reservas_frame, text="Reservas del día", font=self.subtitulo_font, bg=self.color_tarjeta, fg=self.color_texto).pack(anchor="nw", pady=(0, 10))
        columns = ("ID", "Sala", "Responsable", "Hora Inicio", "Hora Término", "Estado")
        tree = self._tabla(reservas_frame, columns, [], height=12)

        def actualizar_tabla():
            for i in tree.get_children():
                tree.delete(i)
            fecha = calendar.get_date()
            if self.role == "admin":
                reservas_fecha = [reserva for reserva in self.reservas if reserva[3] == fecha]
            else:
                reservas_fecha = [reserva for reserva in self.reservas if reserva[3] == fecha and reserva[2] == self.username]
            for reserva in reservas_fecha:
                tree.insert("", "end", values=(reserva[0], reserva[1], reserva[2], reserva[4], reserva[5], reserva[6]))
            if not reservas_fecha:
                tree.insert("", "end", values=("", "", "No hay reservas para esta fecha.", "", "", ""))

        tk.Button(frame, text="Consultar Reservas", font=self.boton_font, bg=self.color_principal, fg="white",
                  activebackground=self.color_secundario, activeforeground="white", relief="flat",
                  command=actualizar_tabla).pack(side="left", padx=20, pady=10)

    def mostrar_reportes(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Reportes del Sistema", font=self.titulo_font, bg=self.color_fondo, fg=self.color_principal).pack(anchor="nw", pady=(0, 20))
        report_frame = tk.Frame(self.content_frame, bg=self.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        report_frame.pack(fill="x", pady=(10, 20))
        tk.Label(report_frame, text="Seleccione el tipo de reporte:", font=self.subtitulo_font, bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 10))
        tk.Button(report_frame, text="Reporte de Salas", font=self.boton_font, bg=self.color_principal, fg="white",
                  activebackground=self.color_secundario, activeforeground="white", relief="flat",
                  command=self.generar_reporte_salas).pack(fill="x", pady=5, ipady=5)
        tk.Button(report_frame, text="Reporte de Reservas", font=self.boton_font, bg=self.color_principal, fg="white",
                  activebackground=self.color_secundario, activeforeground="white", relief="flat",
                  command=self.generar_reporte_reservas).pack(fill="x", pady=5, ipady=5)

    def generar_reporte_salas(self):
        try:
            salas = self.db.obtener_salas()
            reporte = "Reporte de Salas:\n\n"
            for sala in salas:
                reporte += f"ID: {sala[0]}, Nombre: {sala[1]}, Capacidad: {sala[2]}, Estado: {sala[3]}\n"
            messagebox.showinfo("Reporte de Salas", reporte)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte de salas: {e}")

    def generar_reporte_reservas(self):
        try:
            reservas = self.db.obtener_reservas(self.role, self.username)
            reporte = "Reporte de Reservas:\n\n"
            for reserva in reservas:
                reporte += f"ID: {reserva[0]}, Sala: {reserva[1]}, Responsable: {reserva[2]}, Fecha: {reserva[3]}, " \
                           f"Hora Inicio: {reserva[4]}, Hora Término: {reserva[5]}, Estado: {reserva[6]}\n"
            messagebox.showinfo("Reporte de Reservas", reporte)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte de reservas: {e}")

    def mostrar_config(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, text="Configuración del Sistema", font=self.titulo_font, bg=self.color_fondo, fg=self.color_principal).pack(anchor="nw", pady=(0, 20))
        config_frame = tk.Frame(self.content_frame, bg=self.color_tarjeta, bd=2, relief="groove", padx=20, pady=20)
        config_frame.pack(fill="x", pady=(10, 20))
        tk.Label(config_frame, text="(Opciones de configuración próximamente...)", font=self.normal_font, bg=self.color_tarjeta, fg=self.color_texto).pack(anchor="nw", pady=(10, 0))