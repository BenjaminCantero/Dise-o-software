import tkinter as tk
from tkinter import ttk, messagebox

class NuevaReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva_service, on_success=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.geometry("420x370")
        self.reserva_service = reserva_service
        self.on_success = on_success
        self.configure(bg="#232946")

        # Marco central con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)
        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=330, height=260)

        # Título
        title = tk.Label(frame, text="Nueva Reserva", font=("Arial", 18, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(18, 10))

        # Sala
        sala_label = tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        sala_label.pack(pady=(5, 0))
        self.sala_entry = ttk.Entry(frame, width=26, font=("Arial", 11))
        self.sala_entry.pack(ipady=3)

        # Usuario
        usuario_label = tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        usuario_label.pack(pady=(10, 0))
        self.usuario_entry = ttk.Entry(frame, width=26, font=("Arial", 11))
        self.usuario_entry.pack(ipady=3)

        # Fecha
        fecha_label = tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        fecha_label.pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(frame, width=26, font=("Arial", 11))
        self.fecha_entry.pack(ipady=3)

        # Hora
        hora_label = tk.Label(frame, text="Hora (HH:MM):", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        hora_label.pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(frame, width=26, font=("Arial", 11))
        self.hora_entry.pack(ipady=3)

        # Botón de crear reserva
        style = ttk.Style()
        style.configure("Reserva.TButton", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946", padding=8)
        style.map("Reserva.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        crear_btn = ttk.Button(frame, text="Crear Reserva", style="Reserva.TButton", command=self.crear_reserva)
        crear_btn.pack(pady=18, ipadx=8, ipady=2)

        self.bind("<Return>", lambda event: self.crear_reserva())
        self.sala_entry.focus_set()

    def crear_reserva(self):
        sala = self.sala_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        if not sala or not usuario or not fecha or not hora:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.reserva_service:
            self.reserva_service.crear_reserva(sala, usuario, fecha, hora)
            if self.on_success:
                self.on_success()
            self.destroy()