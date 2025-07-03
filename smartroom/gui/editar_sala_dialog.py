import tkinter as tk
from tkinter import ttk, messagebox
from adapters.sala_dialog_adapter import SalaDialogAdapter
from commands.sala_commands import EditSalaCommand  # Debes tener este comando implementado

class EditarSalaDialog(tk.Toplevel):
    def __init__(self, parent, sala, sala_service, on_save=None):
        super().__init__(parent)
        self.title("Editar Sala")
        self.geometry("370x320")
        self.sala = sala
        self.sala_service = sala_service
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)

        tk.Label(frame, text="Nombre de la sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.nombre_var = tk.StringVar(value=sala["nombre"])
        self.nombre_entry = ttk.Entry(frame, textvariable=self.nombre_var, width=30, font=("Arial", 11))
        self.nombre_entry.pack(ipady=3)

        tk.Label(frame, text="Capacidad:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.capacidad_var = tk.IntVar(value=sala["capacidad"])
        self.capacidad_entry = ttk.Entry(frame, textvariable=self.capacidad_var, width=30, font=("Arial", 11))
        self.capacidad_entry.pack(ipady=3)

        tk.Label(frame, text="Estado:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.estado_var = tk.StringVar(value=sala["estado"])
        self.estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=["disponible", "ocupada"], state="readonly", width=28)
        self.estado_combo.pack(ipady=3)

        style = ttk.Style()
        style.configure("Dialog.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("Dialog.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Dialog.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Dialog.TButton", command=self.destroy).pack(side="left", padx=8)

        self.nombre_entry.focus_set()

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

    @property
    def nombre_input(self):
        return self.nombre_entry

    @property
    def capacidad_input(self):
        return self.capacidad_entry

    @property
    def estado_input(self):
        return self.estado_combo