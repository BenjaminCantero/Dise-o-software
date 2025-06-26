from tkcalendar import DateEntry
from tkinter import ttk, messagebox
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
        self.create_widgets()
        if self.mediator:
            self.mediator.register("reservas_panel", self)

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("id", "usuario", "sala", "inicio", "fin"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("sala", text="Sala")
        self.tree.heading("inicio", text="Fecha Inicio")
        self.tree.heading("fin", text="Fecha Fin")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Nueva Reserva", command=self.nueva_reserva).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Editar Reserva", command=self.editar_reserva).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar Reserva", command=self.eliminar_reserva).pack(side="left", padx=5)
        if self.on_volver:
            ttk.Button(btn_frame, text="Volver", command=self.on_volver).pack(side="left", padx=5)

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
            # Prepara los datos para el diálogo
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