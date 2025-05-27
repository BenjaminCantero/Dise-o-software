import tkinter as tk
from tkinter import ttk, messagebox

class EditarUsuarioDialog(tk.Toplevel):
    def __init__(self, parent, usuario, on_save=None):
        super().__init__(parent)
        self.title("Editar Usuario" if usuario else "Crear Usuario")
        self.geometry("350x280")
        self.usuario = usuario
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=220)

        tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.username_entry = ttk.Entry(frame, width=24, font=("Arial", 11))
        self.username_entry.pack(ipady=3)
        self.username_entry.delete(0, tk.END)
        if usuario:
            self.username_entry.insert(0, getattr(usuario, "username", ""))

        # Campo para contraseña solo al crear usuario
        self.password_entry = None
        if not usuario:
            tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
            self.password_entry = ttk.Entry(frame, width=24, font=("Arial", 11), show="*")
            self.password_entry.pack(ipady=3)

        tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.role_var = tk.StringVar(value=getattr(usuario, "role", "estudiante") if usuario else "estudiante")
        self.role_combo = ttk.Combobox(frame, textvariable=self.role_var, values=["admin", "profesor", "estudiante"], state="readonly", width=22)
        self.role_combo.pack(ipady=3)

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Panel.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Panel.TButton", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.username_entry.focus_set()

    def guardar(self):
        username = self.username_entry.get()
        role = self.role_var.get()
        # Si es creación, pide contraseña
        if self.password_entry:
            password = self.password_entry.get()
            if not username or not password or not role:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if self.on_save:
                self.on_save(username, password, role)
        else:
            if not username or not role:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if self.on_save:
                self.on_save(username, role)
        self.destroy()