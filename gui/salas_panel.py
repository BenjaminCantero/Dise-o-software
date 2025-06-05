import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.editar_sala_dialog import EditarSalaDialog
from gui.nueva_sala_dialog import NuevaSalaDialog

class SalasPanel(ttk.Frame):
    def __init__(self, parent, mediator, sala_service=None, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.sala_service = sala_service
        self.on_volver = on_volver
        self.sala_service.add_observer(self)
        self.create_widgets()
        # --- PATRÓN MEDIATOR: Registrar el panel ---
        if self.mediator:
            self.mediator.register("salas_panel", self)

    #patron observer#

    def update(self, event, data):
        if event in ("sala_creada", "sala_eliminada", "sala_editada"):
            self.cargar_salas()

    # --- PATRÓN MEDIATOR: Método para recibir eventos ---
    def on_event(self, sender, event, data):
        if event in ("sala_creada", "sala_eliminada", "sala_editada"):
            self.cargar_salas()

    def destroy(self):
        # --- PATRÓN MEDIATOR: Desregistrar el panel ---
        if self.mediator:
            self.mediator.unregister("salas_panel")
        self.sala_service.remove_observer(self)
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
        icon = ttk.Label(top_frame, text="🏢", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Salas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Filtro de búsqueda
        filter_frame = ttk.Frame(self, style="Panel.TFrame")
        filter_frame.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(filter_frame, text="Buscar por nombre:", background="#f4f4f8", foreground="#232946", font=("Arial", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Buscar", style="Panel.TButton", command=self.filtrar_salas).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Limpiar", style="Panel.TButton", command=self.cargar_salas).pack(side="left", padx=5)

        # Tabla de salas con scrollbar
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("id", "nombre", "capacidad", "estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col, ancho in zip(columns, [50, 150, 100, 100]):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=ancho, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Nueva Sala", style="Panel.TButton", command=self.nueva_sala, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Sala", style="Panel.TButton", command=self.editar_sala, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Sala", style="Panel.TButton", command=self.eliminar_sala, width=18).pack(side="left", padx=8)

        ttk.Button(self, text="Volver al inicio", style="Panel.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_salas()

    def cargar_salas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.sala_service:
            salas = self.sala_service.listar_salas()
            for sala in salas:
                self.tree.insert("", "end", values=(sala["id"], sala["nombre"], sala["capacidad"], sala["estado"]))

    def filtrar_salas(self):
        filtro = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.sala_service:
            salas = self.sala_service.listar_salas()
            for sala in salas:
                if filtro in str(sala["nombre"]).lower():
                    self.tree.insert("", "end", values=(sala["id"], sala["nombre"], sala["capacidad"], sala["estado"]))

    def nueva_sala(self):
        def on_save(nombre, capacidad):
            self.sala_service.crear_sala(nombre, capacidad)
            self.cargar_salas()
            # --- PATRÓN MEDIATOR: Notificar evento ---
            if self.mediator:
                self.mediator.notify(self, "sala_creada")
        NuevaSalaDialog(self, sala_service=self.sala_service, on_success=on_save)

    def editar_sala(self):
        selected = self.tree.selection()
        if selected and self.sala_service:
            sala_id = self.tree.item(selected[0])["values"][0]
            sala = next((s for s in self.sala_service.listar_salas() if s["id"] == sala_id), None)
            if sala:
                def on_save(nombre, capacidad, estado):
                    self.sala_service.editar_sala(sala_id, nombre, capacidad, estado)
                    self.cargar_salas()
                    # --- PATRÓN MEDIATOR: Notificar evento ---
                    if self.mediator:
                        self.mediator.notify(self, "sala_editada")
                EditarSalaDialog(self, sala, on_save=on_save)

    def eliminar_sala(self):
        selected = self.tree.selection()
        if selected and self.sala_service:
            sala_id = self.tree.item(selected[0])["values"][0]
            respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta sala?")
            if respuesta:
                self.sala_service.eliminar_sala(sala_id)
                self.cargar_salas()
                # --- PATRÓN MEDIATOR: Notificar evento ---
                if self.mediator:
                    self.mediator.notify(self, "sala_eliminada")
                messagebox.showinfo("Éxito", "Sala eliminada correctamente")

