import tkinter as tk
from tkinter import ttk, messagebox

class EditarReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva, salas, usuarios, on_save=None):
        super().__init__(parent)
        self.title("Editar Reserva")
        self.geometry("370x350")
        self.reserva = reserva
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=300)

        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.sala_var = tk.StringVar(value=reserva["sala"])
        sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=salas, state="readonly", width=28)
        sala_combo.pack(ipady=3)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar(value=reserva["usuario"])
        usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=usuarios, state="readonly", width=28)
        usuario_combo.pack(ipady=3)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.fecha_entry.pack(ipady=3)
        self.fecha_entry.insert(0, reserva["fecha"])

        tk.Label(frame, text="Hora:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.hora_entry.pack(ipady=3)
        self.hora_entry.insert(0, reserva["hora"])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.fecha_entry.focus_set()

    def guardar(self):
        sala = self.sala_var.get()
        usuario = self.usuario_var.get()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        if not sala or not usuario or not fecha or not hora:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.on_save:
            self.on_save(sala, usuario, fecha, hora)
        self.destroy()