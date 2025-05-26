import tkinter as tk
from tkinter import ttk, messagebox

class NuevaSalaDialog(tk.Toplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.title("Nueva Sala")
        self.geometry("300x180")
        self.on_save = on_save

        tk.Label(self, text="Nombre de la sala:").pack(pady=5)
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.pack(pady=5)

        tk.Label(self, text="Capacidad:").pack(pady=5)
        self.capacidad_entry = ttk.Entry(self)
        self.capacidad_entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        capacidad = self.capacidad_entry.get().strip()
        if not nombre or not capacidad.isdigit():
            messagebox.showerror("Error", "Completa todos los campos correctamente.")
            return
        if self.on_save:
            self.on_save(nombre, int(capacidad))
        self.destroy()