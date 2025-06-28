import tkinter as tk
from tkinter import ttk, messagebox
from adapters.sala_dialog_adapter import SalaDialogAdapter
from commands.sala_commands import CreateSalaCommand  # Debes tener este comando implementado

class NuevaSalaDialog(tk.Toplevel):
    def __init__(self, parent, sala_service, on_success=None):
        super().__init__(parent)
        self.title("Nueva Sala")
        self.geometry("370x320")
        self.sala_service = sala_service
        self.on_success = on_success
        self.configure(bg="#232946")
        self._guardando = False  # <-- Flag para evitar doble ejecución

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)

        tk.Label(frame, text="Nombre de la sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.nombre_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.nombre_entry.pack(ipady=3)

        tk.Label(frame, text="Capacidad:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.capacidad_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.capacidad_entry.pack(ipady=3)

        tk.Label(frame, text="Estado:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.estado_var = tk.StringVar()
        self.estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, state="readonly", width=28)
        self.estado_combo['values'] = ("disponible", "ocupada")
        self.estado_combo.pack(ipady=3)
        self.estado_combo.current(0)

        style = ttk.Style()
        style.configure("SalaForm.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("SalaForm.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="SalaForm.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="SalaForm.TButton", command=self.destroy).pack(side="left", padx=8)

        self.nombre_entry.focus_set()

    def guardar(self):
        if self._guardando:
            return
        self._guardando = True
        nombre = self.nombre_entry.get().strip()
        capacidad = self.capacidad_entry.get().strip()
        estado = self.estado_var.get().strip()

        # Validaciones antes de llamar al adapter
        if not nombre:
            messagebox.showerror("Error", "El nombre de la sala es obligatorio.")
            self._guardando = False
            return
        if not capacidad:
            messagebox.showerror("Error", "La capacidad es obligatoria.")
            self._guardando = False
            return
        try:
            capacidad_int = int(capacidad)
            if capacidad_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número entero positivo.")
            self._guardando = False
            return

        # Si pasa la validación, usa el adapter normalmente
        adapter = SalaDialogAdapter(self)
        data = adapter.get_data()
        try:
            command = CreateSalaCommand(self.sala_service, data["nombre"], data["capacidad"], data["estado"])
            command.execute()
            messagebox.showinfo("Éxito", "Sala creada correctamente.")
            if self.on_success:
                self.on_success(data["nombre"], data["capacidad"], data["estado"])
            self.destroy()
        except Exception as e:
            # Solo muestra el error si ocurre una excepción real
            messagebox.showerror("Error", str(e))
            self._guardando = False

    @property
    def nombre_input(self):
        return self.nombre_entry

    @property
    def capacidad_input(self):
        return self.capacidad_entry

    @property
    def ubicacion_input(self):
        # Si tienes un campo de ubicación, retorna el widget aquí. Si no, retorna None.
        return None