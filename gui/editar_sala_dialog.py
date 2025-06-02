import tkinter as tk
from tkinter import ttk, messagebox
from adapters.sala_dialog_adapter import SalaDialogAdapter

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
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, sala["nombre"])

        tk.Label(frame, text="Capacidad:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.capacidad_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.capacidad_entry.pack(ipady=3)
        self.capacidad_entry.delete(0, tk.END)
        self.capacidad_entry.insert(0, str(sala["capacidad"]))

        tk.Label(frame, text="Estado:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.estado_var = tk.StringVar(value=sala.get("estado", "disponible"))
        self.estado_combo = ttk.Combobox(frame, textvariable=self.estado_var, values=["disponible", "ocupada"], state="readonly", width=22)
        self.estado_combo.pack(ipady=3)

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Panel.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Panel.TButton", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.nombre_entry.focus_set()

    def guardar(self):
        adapter = SalaDialogAdapter(self)
        data = adapter.get_data()

        # Validaciones
        self.nombre_entry.configure(background="white")
        self.capacidad_entry.configure(background="white")
        error = False

        if not data["nombre"].strip():
            self.nombre_entry.configure(background="#ffcccc")
            error = True

        if data["capacidad"] is None or not isinstance(data["capacidad"], int) or data["capacidad"] <= 0:
            self.capacidad_entry.configure(background="#ffcccc")
            messagebox.showerror("Error", "La capacidad debe ser un número entero positivo")
            return

        if error:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        estado = self.estado_var.get()
        try:
            # Aquí deberías llamar a tu servicio para editar la sala, por ejemplo:
            # self.sala_service.editar_sala(self.sala["id"], data["nombre"], data["capacidad"], estado)
            pass
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Sala guardada correctamente")
        if self.on_save:
            self.on_save(data["nombre"], data["capacidad"], estado)
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