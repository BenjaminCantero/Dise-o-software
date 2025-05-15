import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from ui_componentes import UIComponentes
from utils import mostrar_mensaje, limpiar_frame, centrar_ventana, validar_entrada, formatear_fecha

class SistemaGestionSalas:
    def __init__(self, root, role, db, username):
        self.root = root
        self.role = role
        self.db = db
        self.username = username

        # Inicializar componentes de UI
        self.ui = UIComponentes()
        self.ui.configurar_estilos(ttk.Style())

        # Layout principal
        self.root.configure(bg=self.ui.color_fondo)
        self.main_frame = tk.Frame(self.root, bg=self.ui.color_fondo)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = self._crear_sidebar()
        # Contenido principal
        self.content_frame = tk.Frame(self.main_frame, bg=self.ui.color_fondo)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Datos iniciales
        self.salas = self.db.obtener_salas()
        self.reservas = self.db.obtener_reservas(self.role, self.username)
        self.mostrar_inicio()

    # --- COMPONENTES MODULARES ---
    def _crear_sidebar(self):
        sidebar = tk.Frame(self.main_frame, bg=self.ui.color_sidebar, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self.ui.crear_label(sidebar, "Salas U", fuente=("Segoe UI", 20, "bold"), color_fondo=self.ui.color_sidebar, color_texto="white").pack(pady=30)
        self._sidebar_button(sidebar, "Inicio", self.mostrar_inicio)
        self._sidebar_button(sidebar, "Reservas", self.mostrar_reservas)
        self._sidebar_button(sidebar, "Calendario", self.mostrar_calendario)
        self._sidebar_button(sidebar, "Reportes", self.mostrar_reportes)
        self._sidebar_button(sidebar, "Configuración", self.mostrar_config)
        self.ui.crear_boton(sidebar, "Cerrar sesión", self.root.destroy, color_fondo=self.ui.color_secundario).pack(side="bottom", pady=20, fill="x", padx=20)
        return sidebar

    def _sidebar_button(self, parent, text, command):
        self.ui.crear_boton(parent, text, command, color_fondo=self.ui.color_sidebar).pack(fill="x", padx=20, pady=2)

    def _tarjeta_resumen(self, parent, titulo, valor, color, col):
        frame = self.ui.crear_frame(parent, color_fondo=self.ui.color_tarjeta)
        frame.grid(row=0, column=col, padx=20, ipadx=30, ipady=20, sticky="nsew")
        self.ui.crear_label(frame, titulo, fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_texto).pack(anchor="w")
        self.ui.crear_label(frame, str(valor), fuente=("Segoe UI", 28, "bold"), color_fondo=self.ui.color_tarjeta, color_texto=color).pack(anchor="w")

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
        limpiar_frame(self.content_frame)

    # --- PANELES PRINCIPALES ---
    def mostrar_inicio(self):
        self.limpiar_contenido()
        # Tarjetas resumen
        resumen_frame = tk.Frame(self.content_frame, bg=self.ui.color_fondo)
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
        atajos = tk.Frame(self.content_frame, bg=self.ui.color_fondo)
        atajos.pack(fill="x", pady=10)
        self.ui.crear_label(atajos, "Atajos rápidos", fuente=self.ui.subtitulo_font, color_fondo=self.ui.color_fondo, color_texto=self.ui.color_texto).pack(anchor="w", padx=10)
        self.ui.crear_boton(atajos, "Reservar Sala", self.mostrar_reservas, color_fondo=self.ui.color_principal).pack(side="left", padx=10, ipadx=10)
        self.ui.crear_boton(atajos, "Ver Calendario", self.mostrar_calendario, color_fondo=self.ui.color_principal).pack(side="left", padx=10, ipadx=10)

        # --- Botones de gestión de salas ---
        gestion_frame = tk.Frame(self.content_frame, bg=self.ui.color_fondo)
        gestion_frame.pack(fill="x", pady=(10, 0), padx=20)
        self.ui.crear_boton(gestion_frame, "Añadir Sala", self.dialogo_añadir_sala, color_fondo="#28a745").pack(side="left", padx=5, ipadx=10)
        self.ui.crear_boton(gestion_frame, "Editar Sala", self.dialogo_editar_sala, color_fondo="#ffc107", color_texto="#22223b").pack(side="left", padx=5, ipadx=10)
        self.ui.crear_boton(gestion_frame, "Borrar Sala", self.dialogo_borrar_sala, color_fondo="#dc3545").pack(side="left", padx=5, ipadx=10)

        # Tabla de salas
        tabla_frame = tk.Frame(self.content_frame, bg=self.ui.color_tarjeta, bd=2, relief="groove")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.ui.crear_label(tabla_frame, "Todas las Salas", fuente=self.ui.subtitulo_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_texto).pack(anchor="w", pady=(10, 0), padx=10)
        columns = ("ID", "Nombre", "Capacidad", "Estado")
        self.salas_tree = self._tabla(tabla_frame, columns, self.salas, height=12)

    # --- DIALOGOS DE GESTION DE SALAS ---
    def dialogo_añadir_sala(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Añadir Sala")
        dialog.configure(bg=self.ui.color_tarjeta)
        self.ui.crear_label(dialog, "Nombre:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
        nombre = tk.Entry(dialog, font=self.ui.normal_font)
        nombre.pack(pady=5)
        self.ui.crear_label(dialog, "Capacidad:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
        capacidad = tk.Entry(dialog, font=self.ui.normal_font)
        capacidad.pack(pady=5)
        self.ui.crear_label(dialog, "Estado:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
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
        self.ui.crear_boton(dialog, "Guardar", guardar, color_fondo=self.ui.color_principal).pack(pady=10)

    def dialogo_editar_sala(self):
        item = self.salas_tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona una sala para editar.")
            return
        valores = self.salas_tree.item(item, "values")
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Sala")
        dialog.configure(bg=self.ui.color_tarjeta)
        self.ui.crear_label(dialog, "Nombre:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
        nombre = tk.Entry(dialog, font=self.ui.normal_font)
        nombre.insert(0, valores[1])
        nombre.pack(pady=5)
        self.ui.crear_label(dialog, "Capacidad:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
        capacidad = tk.Entry(dialog, font=self.ui.normal_font)
        capacidad.insert(0, valores[2])
        capacidad.pack(pady=5)
        self.ui.crear_label(dialog, "Estado:", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta).pack(pady=5)
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
        self.ui.crear_boton(dialog, "Guardar Cambios", guardar, color_fondo=self.ui.color_principal).pack(pady=10)

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
        frame = tk.Frame(self.content_frame, bg=self.ui.color_tarjeta, bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        self.ui.crear_label(frame, "Reservas Activas", fuente=self.ui.titulo_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_principal).pack(anchor="nw", pady=(0, 20), padx=10)
        columns = ("ID", "Sala", "Responsable", "Fecha", "Hora Inicio", "Hora Término", "Estado")
        self._tabla(frame, columns, self.reservas, height=15)

    def mostrar_calendario(self):
        self.limpiar_contenido()
        frame = tk.Frame(self.content_frame, bg=self.ui.color_tarjeta, bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        self.ui.crear_label(frame, "Calendario de Reservas", fuente=self.ui.titulo_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_principal).pack(anchor="nw", pady=(0, 20), padx=10)
        calendar = Calendar(frame, selectmode="day")
        calendar.pack(side="left", padx=20, pady=10)
        reservas_frame = tk.Frame(frame, bg=self.ui.color_tarjeta)
        reservas_frame.pack(side="left", fill="both", expand=True, padx=20)
        self.ui.crear_label(reservas_frame, "Reservas del día", fuente=self.ui.subtitulo_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_texto).pack(anchor="nw", pady=(0, 10))
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

        self.ui.crear_boton(frame, "Consultar Reservas", actualizar_tabla, color_fondo=self.ui.color_principal).pack(side="left", padx=20, pady=10)

    def mostrar_reportes(self):
        self.limpiar_contenido()
        self.ui.crear_label(self.content_frame, "Reportes del Sistema", fuente=self.ui.titulo_font, color_fondo=self.ui.color_fondo, color_texto=self.ui.color_principal).pack(anchor="nw", pady=(0, 20))
        report_frame = tk.Frame(self.content_frame, bg=self.ui.color_fondo, relief="groove", bd=2, padx=20, pady=20)
        report_frame.pack(fill="x", pady=(10, 20))
        self.ui.crear_label(report_frame, "Seleccione el tipo de reporte:", fuente=self.ui.subtitulo_font, color_fondo=self.ui.color_fondo, color_texto=self.ui.color_texto).pack(anchor="w", pady=(0, 10))
        self.ui.crear_boton(report_frame, "Reporte de Salas", self.generar_reporte_salas, color_fondo=self.ui.color_principal).pack(fill="x", pady=5, ipady=5)
        self.ui.crear_boton(report_frame, "Reporte de Reservas", self.generar_reporte_reservas, color_fondo=self.ui.color_principal).pack(fill="x", pady=5, ipady=5)

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
        self.ui.crear_label(self.content_frame, "Configuración del Sistema", fuente=self.ui.titulo_font, color_fondo=self.ui.color_fondo, color_texto=self.ui.color_principal).pack(anchor="nw", pady=(0, 20))
        config_frame = tk.Frame(self.content_frame, bg=self.ui.color_tarjeta, bd=2, relief="groove", padx=20, pady=20)
        config_frame.pack(fill="x", pady=(10, 20))
        self.ui.crear_label(config_frame, "(Opciones de configuración próximamente...)", fuente=self.ui.normal_font, color_fondo=self.ui.color_tarjeta, color_texto=self.ui.color_texto).pack(anchor="nw", pady=(10, 0))