import tkinter as tk
from tkinter import ttk, messagebox
from adapters.sala_dialog_adapter import SalaDialogAdapter
from smartroom.services import sala_service

class NuevaSalaDialog(tk.Toplevel):
    def __init__(self, parent, sala_service, on_success=None):
        super().__init__(parent)
        self.title("Nueva Sala")
        self.geometry("370x320")
        self.sala_service = sala_service
        self.on_success = on_success
        self.configure(bg="#232946")

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
        self.estado_combo['values'] = ("Disponible", "Ocupada", "Mantenimiento")
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
        adapter = SalaDialogAdapter(self)
        data = adapter.get_data()
        if not data["nombre"]:
            messagebox.showerror("Error", "El nombre de la sala es obligatorio.")
            return
        if data["capacidad"] is None or not isinstance(data["capacidad"], int) or data["capacidad"] <= 0:
            messagebox.showerror("Error", "La capacidad debe ser un número positivo.")
            return
        if not self.estado_var.get():
            messagebox.showerror("Error", "Debe seleccionar un estado.")
            return
        try:
            sala_service.crear_sala(data["nombre"], data["capacidad"], self.estado_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Sala creada correctamente.")
        if self.on_success:
            self.on_success(data["nombre"], data["capacidad"], self.estado_var.get())
        self.destroy()

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