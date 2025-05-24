import tkinter as tk
from tkinter import ttk, messagebox
import re

class EditarUsuarioDialog(tk.Toplevel):
    def __init__(self, parent, usuario, on_save=None):
        super().__init__(parent)
        self.title("Editar Usuario")
        self.geometry("350x320")
        self.usuario = usuario
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

        tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.nombre_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.nombre_entry.pack(ipady=3)
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, usuario["nombre"])

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.correo_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.correo_entry.pack(ipady=3)
        self.correo_entry.delete(0, tk.END)
        self.correo_entry.insert(0, usuario["correo"])

        tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.rol_var = tk.StringVar(value=usuario.get("role", "estudiante"))
        rol_combo = ttk.Combobox(frame, textvariable=self.rol_var, values=["admin", "profesor", "estudiante"], state="readonly", width=22)
        rol_combo.pack(ipady=3)
        self.rol_var.set(usuario["rol"])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Panel.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Panel.TButton", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.nombre_entry.focus_set()

    def es_correo_valido(self, correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, correo) is not None

    def guardar(self):
        error = False
        self.nombre_entry.configure(background="white")
        self.correo_entry.configure(background="white")

        if not self.nombre_entry.get().strip():
            self.nombre_entry.configure(background="#ffcccc")
            error = True
        correo = self.correo_entry.get().strip()
        if not correo:
            self.correo_entry.configure(background="#ffcccc")
            error = True
        elif not self.es_correo_valido(correo):
            self.correo_entry.configure(background="#ffcccc")
            messagebox.showerror("Error", "El correo no tiene un formato válido")
            return

        if error:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        nombre = self.nombre_entry.get().strip()
        rol = self.rol_var.get()
        if self.on_save:
            self.on_save(nombre, correo, rol)
        messagebox.showinfo("Éxito", "Usuario guardado correctamente")  # Mensaje de éxito
        self.destroy()