import tkinter as tk
from tkinter import ttk, messagebox

class MisReservasPanel(ttk.Frame):
    def __init__(self, parent, reserva_service, user):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.user = user
        self.create_widgets()
        self.cargar_reservas()

    def create_widgets(self):
        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(pady=10)
        ttk.Label(filtro_frame, text="Filtrar por fecha:").pack(side="left")
        self.fecha_entry = ttk.Entry(filtro_frame, width=12)
        self.fecha_entry.pack(side="left", padx=5)
        ttk.Button(filtro_frame, text="Buscar", command=self.cargar_reservas).pack(side="left")

        self.tree = ttk.Treeview(self, columns=("Sala", "Fecha", "Hora", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(self, text="Cancelar reserva seleccionada", command=self.cancelar_reserva).pack(pady=5)

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        fecha_filtro = self.fecha_entry.get().strip()
        reservas = self.reserva_service.obtener_reservas_por_usuario(self.user["id"])
        for reserva in reservas:
            if fecha_filtro and reserva["fecha"] != fecha_filtro:
                continue
            self.tree.insert("", "end", values=(reserva["sala"], reserva["fecha"], reserva["hora"], reserva["estado"]))

    def cancelar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva para cancelar.")
            return
        reserva = self.tree.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas cancelar esta reserva?")
        if respuesta:
            self.reserva_service.cancelar_reserva(self.user["id"], reserva[1], reserva[2])  # Ajusta según tu modelo
            messagebox.showinfo("Éxito", "Reserva cancelada.")
            self.cargar_reservas()