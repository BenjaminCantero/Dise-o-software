import tkinter as tk
from tkinter import ttk, messagebox
from adapters.sala_dialog_adapter import SalaDialogAdapter
from commands.sala_commands import EditSalaCommand  # Debes tener este comando implementado

class EditarSalaDialog(tk.Toplevel):
    def __init__(self, parent, sala, sala_service, on_save=None):
        super().__init__(parent)
        self.title("Editar Sala")
        self.sala = sala
        self.sala_service = sala_service
        self.on_save = on_save

        self.nombre_var = tk.StringVar(value=sala["nombre"])
        self.capacidad_var = tk.IntVar(value=sala["capacidad"])
        self.estado_var = tk.StringVar(value=sala["estado"])

        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(self, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Capacidad:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.capacidad_entry = ttk.Entry(self, textvariable=self.capacidad_var)
        self.capacidad_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Estado:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.estado_combo = ttk.Combobox(self, textvariable=self.estado_var, values=["disponible", "ocupada"])
        self.estado_combo.grid(row=2, column=1, padx=10, pady=5)

        guardar_btn = ttk.Button(self, text="Guardar", command=self.guardar)
        guardar_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def guardar(self):
        # --- Adapter: extrae y adapta los datos del diálogo ---
        adapter = SalaDialogAdapter(self)
        data = adapter.get_data()

        nombre = data.get("nombre")
        try:
            capacidad = int(data.get("capacidad"))
        except Exception:
            messagebox.showerror("Error", "La capacidad debe ser un número entero.")
            return
        estado = data.get("estado")

        if not nombre:
            messagebox.showerror("Error", "El nombre de la sala es obligatorio.")
            return
        if capacidad <= 0:
            messagebox.showerror("Error", "La capacidad debe ser mayor a cero.")
            return
        if not estado:
            messagebox.showerror("Error", "Debe seleccionar un estado.")
            return

        try:
            # --- Command: ejecuta la acción de editar sala ---
            command = EditSalaCommand(self.sala_service, self.sala["id"], nombre, capacidad, estado)
            command.execute()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la sala:\n{e}")
            return

        messagebox.showinfo("Éxito", "Sala editada correctamente.")
        if self.on_save:
            self.on_save(nombre, capacidad, estado)
        self.destroy()