from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from smartroom.services import reserva_service, sala_service, user_service
from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog

class ReservasPanel(ttk.Frame):
    def __init__(self, parent, mediator=None, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.on_volver = on_volver
        self.create_widgets()
        self.cargar_reservas()
        if self.mediator:
            self.mediator.register("reservas_panel", self)

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 18, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 22), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        filter_frame = ttk.Frame(self, style="Panel.TFrame")
        filter_frame.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(filter_frame, text="Buscar por usuario:", background="#f4f4f8", foreground="#232946", font=("Arial", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Buscar", style="Panel.TButton", command=self.filtrar_reservas).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Limpiar", style="Panel.TButton", command=self.cargar_reservas).pack(side="left", padx=5)

        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("id", "sala_nombre", "usuario_username", "fecha_inicio", "fecha_fin")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col, ancho in zip(columns, [50, 120, 120, 140, 140]):
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
            self.tree.column(col, width=ancho, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Nueva Reserva", style="Panel.TButton", command=self.nueva_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Reserva", style="Panel.TButton", command=self.eliminar_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Reserva", style="Panel.TButton", command=self.editar_reserva, width=18).pack(side="left", padx=8)

        ttk.Button(self, text="Volver al inicio", style="Panel.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            reservas = reserva_service.listar_reservas()
            usuarios = {u["id"]: u["username"] for u in user_service.get_usuarios()}
            salas = {s["id"]: s["nombre"] for s in sala_service.get_salas()}
            for reserva in reservas:
                usuario = usuarios.get(reserva["usuario_id"], "Desconocido")
                sala = salas.get(reserva["sala_id"], "Desconocida")
                self.tree.insert(
                    "", "end",
                    values=(
                        reserva["id"],
                        usuario,
                        sala,
                        reserva["fecha_inicio"].replace("T", " ")[:16],
                        reserva["fecha_fin"].replace("T", " ")[:16]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las reservas:\n{e}")

    def filtrar_reservas(self):
        filtro = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if reserva_service:
            reservas = reserva_service.listar_reservas()
            for reserva in reservas:
                if filtro in str(reserva["usuario_username"]).lower():
                    self.tree.insert("", "end", values=(
                        reserva["id"],
                        reserva["sala_nombre"],
                        reserva["usuario_username"],
                        str(reserva["fecha_inicio"])[:16],
                        str(reserva["fecha_fin"])[:16]
                    ))

    def nueva_reserva(self):
        def on_success():
            self.cargar_reservas()
            if self.mediator:
                self.mediator.notify(self, "reserva_creada")
        NuevaReservaDialog(self, on_success=on_success)

    def editar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        reservas = reserva_service.listar_reservas()
        reserva = next((r for r in reservas if r["id"] == reserva_id), None)
        if reserva:
            def on_save():
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_editada")
            EditarReservaDialog(self, reserva, on_save=on_save)

    def eliminar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta reserva?")
        if respuesta:
            try:
                reserva_service.eliminar_reserva(reserva_id)
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_eliminada")
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la reserva:\n{e}")
