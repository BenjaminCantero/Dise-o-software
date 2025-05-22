import tkinter as tk
from tkinter import ttk, messagebox

class NuevaReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva_service, on_success=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.geometry("350x300")
        self.reserva_service = reserva_service
        self.on_success = on_success

        ttk.Label(self, text="Sala:").pack(pady=(20, 0))
        self.sala_entry = ttk.Entry(self, width=30)
        self.sala_entry.pack()

        ttk.Label(self, text="Usuario:").pack(pady=(10, 0))
        self.usuario_entry = ttk.Entry(self, width=30)
        self.usuario_entry.pack()

        ttk.Label(self, text="Fecha (YYYY-MM-DD):").pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(self, width=30)
        self.fecha_entry.pack()

        ttk.Label(self, text="Hora (HH:MM):").pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(self, width=30)
        self.hora_entry.pack()

        ttk.Button(self, text="Crear Reserva", command=self.crear_reserva).pack(pady=20)

    def crear_reserva(self):
        sala = self.sala_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        if not sala or not usuario or not fecha or not hora:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        # Aquí deberías validar y crear la reserva usando el reserva_service
        if self.reserva_service:
            self.reserva_service.crear_reserva(sala, usuario, fecha, hora)
            if self.on_success:
                self.on_success()
            self.destroy()