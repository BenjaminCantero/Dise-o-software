import tkinter as tk
from tkinter import ttk, messagebox

class ReservaApp(tk.Tk):
    def __init__(self, reserva_service, mediator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reserva_service = reserva_service
        self.mediator = mediator
        self.title("Reservas")
        self.geometry("800x600")
        self.configure(bg="#232946")

        # Marco principal con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.pack(fill="both", expand=True, padx=10, pady=10)
        frame = tk.Frame(shadow, bg="#f4f4f8")
        frame.pack(fill="both", expand=True)

        # Título
        title = tk.Label(frame, text="Gestión de Reservas", font=("Arial", 24, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(20, 10))

        # Botón de nueva reserva
        style = ttk.Style()
        style.configure("NuevaReserva.TButton", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946", padding=8)
        style.map("NuevaReserva.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        nueva_reserva_btn = ttk.Button(frame, text="Nueva Reserva", style="NuevaReserva.TButton", command=self.nueva_reserva)
        nueva_reserva_btn.pack(pady=(0, 20), ipadx=8, ipady=2)

        # Tabla de reservas
        self.reservas_tree = None
        self.cargar_reservas()

    def nueva_reserva(self):
        # Obtén las listas de nombres de salas y usuarios
        salas = [s["nombre"] for s in self.mediator.sala_service.listar_salas()]
        usuarios = [u["nombre"] for u in self.mediator.user_service.listar_usuarios()]
        NuevaReservaDialog(self, self.reserva_service, salas, usuarios, on_success=self.cargar_reservas)

    def cargar_reservas(self):
        # Implementa la carga de reservas en la tabla
        pass

class NuevaReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva_service, salas, usuarios, on_success=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.geometry("370x350")
        self.reserva_service = reserva_service
        self.on_success = on_success
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=300)

        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.sala_var = tk.StringVar()
        self.sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=salas, state="readonly", width=28)
        self.sala_combo.pack(ipady=3)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar()
        self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=usuarios, state="readonly", width=28)
        self.usuario_combo.pack(ipady=3)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.fecha_entry.pack(ipady=3)

        tk.Label(frame, text="Hora:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.hora_entry.pack(ipady=3)

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.fecha_entry.focus_set()

    def guardar(self):
        error = False

        # Resetear colores
        self.sala_combo.configure(background="white")
        self.usuario_combo.configure(background="white")
        self.fecha_entry.configure(background="white")
        self.hora_entry.configure(background="white")

        # Validar campos
        if not self.sala_var.get():
            self.sala_combo.configure(background="#ffcccc")
            error = True
        if not self.usuario_var.get():
            self.usuario_combo.configure(background="#ffcccc")
            error = True
        if not self.fecha_entry.get().strip():
            self.fecha_entry.configure(background="#ffcccc")
            error = True
        if not self.hora_entry.get().strip():
            self.hora_entry.configure(background="#ffcccc")
            error = True

        if error:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Guardar la reserva si todo está bien
        sala = self.sala_var.get().strip()
        usuario = self.usuario_var.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        self.reserva_service.crear_reserva(sala, usuario, fecha, hora)
        if self.on_success:
            self.on_success()
        self.destroy()

if __name__ == "__main__":
    app = ReservaApp(reserva_service=None, mediator=None)
    app.mainloop()