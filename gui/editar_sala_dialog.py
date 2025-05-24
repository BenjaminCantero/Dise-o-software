import tkinter as tk
from tkinter import ttk, messagebox

class EditarSalaDialog(tk.Toplevel):
    def __init__(self, parent, sala, on_save=None):
        super().__init__(parent)
        self.title("Editar Sala")
        self.geometry("350x260")
        self.sala = sala
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=210)

        tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.nombre_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.nombre_entry.pack(ipady=3)
        self.nombre_entry.insert(0, sala["nombre"])

        tk.Label(frame, text="Capacidad:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.capacidad_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.capacidad_entry.pack(ipady=3)
        self.capacidad_entry.insert(0, sala["capacidad"])

        tk.Label(frame, text="Estado:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.estado_var = tk.StringVar(value=sala.get("estado", "disponible"))
        estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=["disponible", "ocupada"], state="readonly", width=22)
        estado_combo.pack(ipady=3)

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.nombre_entry.focus_set()

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        capacidad = self.capacidad_entry.get().strip()
        estado = self.estado_var.get()
        if not nombre or not capacidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            capacidad = int(capacidad)
        except ValueError:
            messagebox.showerror("Error", "Capacidad debe ser un número")
            return
        if self.on_save:
            self.on_save(nombre, capacidad, estado)
        self.destroy()