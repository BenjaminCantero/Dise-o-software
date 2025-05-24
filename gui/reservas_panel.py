import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog

class ReservasPanel(ttk.Frame):
    def __init__(self, parent, reserva_service, mediator=None):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.mediator = mediator
        self.reserva_service.add_observer(self)
        self.create_widgets()

    #patron observer#
    
    def update(self, event, data):
        # Se llama automáticamente cuando el servicio notifica un cambio
        if event in ("reserva_creada", "reserva_eliminada"):
            self.cargar_reservas()  # Método que refresca la tabla de reservas

    def destroy(self):
        # Importante: quitar el observer al cerrar el panel
        self.reserva_service.remove_observer(self)
        super().destroy()

    def create_widgets(self):
        # Estilos coherentes
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 18, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 22), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        # Marco superior con título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Filtro de búsqueda
        filter_frame = ttk.Frame(self, style="Panel.TFrame")
        filter_frame.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(filter_frame, text="Buscar por usuario:", background="#f4f4f8", foreground="#232946", font=("Arial", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Buscar", style="Panel.TButton", command=self.filtrar_reservas).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Limpiar", style="Panel.TButton", command=self.cargar_reservas).pack(side="left", padx=5)

        # Tabla de reservas con scrollbar
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("id", "sala", "usuario", "fecha", "hora")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col, ancho in zip(columns, [50, 120, 120, 100, 80]):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=ancho, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Nueva Reserva", style="Panel.TButton", command=self.nueva_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Reserva", style="Panel.TButton", command=self.eliminar_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Reserva", style="Panel.TButton", command=self.editar_reserva, width=18).pack(side="left", padx=8)

        self.cargar_reservas()

    def cargar_reservas(self):
        # Limpia la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Carga las reservas desde el servicio (si está disponible)
        if self.reserva_service:
            reservas = self.reserva_service.listar_reservas()
            for reserva in reservas:
                self.tree.insert("", "end", values=(reserva.id, reserva.sala, reserva.usuario, reserva.fecha, reserva.hora))

    def filtrar_reservas(self):
        filtro = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.reserva_service:
            reservas = self.reserva_service.listar_reservas()
            for reserva in reservas:
                if filtro in str(reserva.usuario).lower():
                    self.tree.insert("", "end", values=(reserva.id, reserva.sala, reserva.usuario, reserva.fecha, reserva.hora))

    def nueva_reserva(self):
        def refrescar():
            self.cargar_reservas()
        NuevaReservaDialog(self, self.reserva_service, on_success=refrescar)

    def eliminar_reserva(self):
        selected = self.tree.selection()
        if selected and self.reserva_service:
            respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta reserva?")
            if respuesta:
                reserva_id = self.tree.item(selected[0])["values"][0]
                self.reserva_service.eliminar_reserva(reserva_id)
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_eliminada")

    def editar_reserva(self):
        selected = self.tree.selection()
        if selected and self.reserva_service:
            reserva_id = self.tree.item(selected[0])["values"][0]
            reserva = next((r for r in self.reserva_service.listar_reservas() if r["id"] == reserva_id), None)
            if reserva:
                # Obtener listas de salas y usuarios para los combobox
                salas = [s["nombre"] for s in self.mediator.sala_service.listar_salas()]
                usuarios = [u["nombre"] for u in self.mediator.user_service.listar_usuarios()]
                def on_save(sala, usuario, fecha, hora):
                    reserva["sala"] = sala
                    reserva["usuario"] = usuario
                    reserva["fecha"] = fecha
                    reserva["hora"] = hora
                    self.reserva_service.notify_observers(event="reserva_editada", data=reserva)
                    self.cargar_reservas()
                EditarReservaDialog(self, reserva, salas, usuarios, on_save=on_save)