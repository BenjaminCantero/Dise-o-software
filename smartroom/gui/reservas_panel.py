from tkcalendar import DateEntry
from tkinter import ttk, messagebox, Toplevel, StringVar, Label, Entry, Button
from datetime import datetime
from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog

class ReservasPanel(ttk.Frame):
    def __init__(self, parent, mediator=None, reserva_service=None, sala_service=None, user_service=None, user=None, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.user = user
        self.on_volver = on_volver
        self._setup_styles()
        self.create_widgets()
        if self.mediator:
            self.mediator.register("reservas_panel", self)

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 20, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 28), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

    def create_widgets(self):
        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Tabla de reservas
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("id", "usuario", "sala", "inicio", "fin")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("sala", text="Sala")
        self.tree.heading("inicio", text="Fecha Inicio")
        self.tree.heading("fin", text="Fecha Fin")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("usuario", width=120, anchor="center")
        self.tree.column("sala", width=120, anchor="center")
        self.tree.column("inicio", width=150, anchor="center")
        self.tree.column("fin", width=150, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Nueva Reserva", style="Panel.TButton", width=18, command=self.nueva_reserva).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Reserva", style="Panel.TButton", width=18, command=self.eliminar_reserva).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Reserva", style="Panel.TButton", width=18, command=self.editar_reserva).pack(side="left", padx=8)

        ttk.Button(self, text="Volver al inicio", style="Panel.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            reservas = self.reserva_service.get_all()
            usuarios = {u["id"]: u["username"] for u in self.user_service.get_all()}
            salas = {s["id"]: s["nombre"] for s in self.sala_service.get_all()}
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

    def nueva_reserva(self):
        def on_success(*_):
            self.cargar_reservas()
            if self.mediator:
                self.mediator.notify(self, "reserva_creada", None)
        NuevaReservaDialog(self, self.reserva_service, self.sala_service, self.user_service, on_success=on_success)

    def editar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        reservas = self.reserva_service.get_all()
        reserva = next((r for r in reservas if r["id"] == reserva_id), None)
        if reserva:
            def on_save(*_):
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_editada", None)
            usuarios = {u["id"]: u["username"] for u in self.user_service.get_all()}
            salas = {s["id"]: s["nombre"] for s in self.sala_service.get_all()}
            reserva_dialog_data = {
                "id": reserva["id"],
                "usuario": usuarios.get(reserva["usuario_id"], ""),
                "sala": salas.get(reserva["sala_id"], ""),
                "fecha": reserva["fecha_inicio"][:10],
                "hora": reserva["fecha_inicio"][11:16]
            }
            EditarReservaDialog(self, reserva_dialog_data, self.reserva_service, self.sala_service, self.user_service, on_save=on_save)

    def eliminar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta reserva?")
        if respuesta:
            try:
                self.reserva_service.delete(reserva_id)
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_eliminada", None)
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la reserva:\n{e}")

    def on_event(self, sender, event, data):
        if event in ("reserva_creada", "reserva_eliminada", "reserva_editada"):
            self.cargar_reservas()