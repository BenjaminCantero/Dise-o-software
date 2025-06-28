import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.editar_sala_dialog import EditarSalaDialog
from gui.nueva_sala_dialog import NuevaSalaDialog
from factories.dialog_factory import DialogFactory
from mediator.app_mediator import EventListener
from commands.sala_commands import DeleteSalaCommand  # Debes tener este comando implementado

class SalasPanel(EventListener, ttk.Frame):
    def __init__(self, parent, mediator=None, sala_service=None, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.sala_service = sala_service
        self.on_volver = on_volver
        self.dialog_factory = DialogFactory(sala_service=self.sala_service)
        self.create_widgets()
        if self.mediator:
            self.mediator.register("salas_panel", self)

    def update(self, event, data):
        if event in ("sala_creada", "sala_eliminada", "sala_editada"):
            self.cargar_salas()

    def on_event(self, sender, event, data):
        if event in ("sala_creada", "sala_eliminada", "sala_editada"):
            self.cargar_salas()

    def destroy(self):
        if self.mediator:
            self.mediator.unregister("salas_panel")
        super().destroy()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Segoe UI", 22, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Segoe UI Emoji", 32), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Custom.Treeview", font=("Segoe UI", 13), rowheight=32, background="#f4f4f8", fieldbackground="#f4f4f8", borderwidth=0)
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 14, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Modern.TButton", font=("Segoe UI", 12, "bold"), background="#eebbc3", foreground="#232946", borderwidth=0, padding=8)
        style.map("Modern.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(18, 0), padx=18)
        icon = ttk.Label(top_frame, text="🏢", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 12))
        label = ttk.Label(top_frame, text="Gestión de Salas", style="PanelTitle.TLabel")
        label.pack(side="left")

        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=40, pady=24)
        columns = ("id", "nombre", "capacidad", "estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14, style="Custom.Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("capacidad", text="Capacidad")
        self.tree.heading("estado", text="Estado")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=180, anchor="center")
        self.tree.column("capacidad", width=120, anchor="center")
        self.tree.column("estado", width=120, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Nueva Sala", style="Modern.TButton", width=18, command=self.nueva_sala).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Sala", style="Modern.TButton", width=18, command=self.eliminar_sala).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Sala", style="Modern.TButton", width=18, command=self.editar_sala).pack(side="left", padx=8)
        ttk.Button(self, text="Volver al inicio", style="Modern.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_salas()

    def cargar_salas(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return  # El widget ya no existe, no intentes actualizarlo
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            salas = self.sala_service.get_all()
            for sala in salas:
                self.tree.insert("", "end", values=(sala["id"], sala["nombre"], sala["capacidad"], sala["estado"]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las salas:\n{e}")

    def filtrar_salas(self):
        filtro = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.sala_service:
            salas = self.sala_service.get_all()
            for sala in salas:
                if filtro in str(sala["nombre"]).lower():
                    self.tree.insert("", "end", values=(sala["id"], sala["nombre"], sala["capacidad"], sala["estado"]))

    def nueva_sala(self):
        def on_save(nombre, capacidad, estado):
            # Solo refresca la lista o muestra mensaje, NO crees la sala aquí
            self.cargar_salas()
            if self.mediator:
                self.mediator.notify(self, "sala_creada")
            messagebox.showinfo("Éxito", "Sala creada correctamente.")
        self.dialog_factory.create_dialog(
            "nueva_sala",
            self,
            sala_service=self.sala_service,
            on_success=on_save
        )

    def editar_sala(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una sala para editar.")
            return
        sala_id = self.tree.item(selected[0])["values"][0]
        salas = self.sala_service.get_all()
        sala = next((s for s in salas if s["id"] == sala_id), None)
        if sala:
            def on_save(nombre, capacidad, estado):
                try:
                    self.sala_service.update(sala_id, nombre, capacidad, estado)
                    self.cargar_salas()
                    if self.mediator:
                        self.mediator.notify(self, "sala_editada")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo editar la sala:\n{e}")
            self.dialog_factory.create_dialog("editar_sala", self, sala, on_save=on_save)

    def eliminar_sala(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una sala para eliminar.")
            return
        sala_id = self.tree.item(selected[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta sala?")
        if respuesta:
            try:
                # --- Command: ejecuta la acción de eliminar sala ---
                command = DeleteSalaCommand(self.sala_service, sala_id)
                command.execute()
                self.cargar_salas()
                if self.mediator:
                    self.mediator.notify(self, "sala_eliminada")
                messagebox.showinfo("Éxito", "Sala eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la sala:\n{e}")