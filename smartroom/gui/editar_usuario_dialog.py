import tkinter as tk
from tkinter import ttk, messagebox
from adapters.usuario_dialog_adapter import UsuarioDialogAdapter

class EditarUsuarioDialog(tk.Toplevel):
    def __init__(self, parent, usuario, on_save=None):
        super().__init__(parent)
        self.title("Editar Usuario" if usuario else "Crear Usuario")
        self.geometry("370x320")
        self.usuario = usuario
        self.on_save = on_save
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)

        tk.Label(frame, text="Nombre de usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.username_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.username_entry.pack(ipady=3)
        self.username_entry.delete(0, tk.END)
        if usuario:
            username = usuario.get("username") if isinstance(usuario, dict) else getattr(usuario, "username", "")
            self.username_entry.insert(0, username)
        self.password_entry = None
        if not usuario:
            tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
            self.password_entry = ttk.Entry(frame, width=30, font=("Arial", 11), show="*")
            self.password_entry.pack(ipady=3)

        tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        role = usuario.get("role") if usuario and isinstance(usuario, dict) else getattr(usuario, "role", "estudiante")
        self.role_var = tk.StringVar(value=role if role else "estudiante")
        self.role_combo = ttk.Combobox(frame, textvariable=self.role_var, values=["admin", "profesor", "estudiante"], state="readonly", width=28)
        self.role_combo.pack(ipady=3)

        style = ttk.Style()
        style.configure("Dialog.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("Dialog.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Dialog.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Dialog.TButton", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.username_entry.focus_set()

    def guardar(self):
        adapter = UsuarioDialogAdapter(self)
        data = adapter.get_data()
        password = self.password_entry.get().strip() if self.password_entry else None

        if (
            not data["username"].strip()
            or not data["role"].strip()
            or (self.password_entry and not password)
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if self.on_save:
            self.on_save(data["username"].strip(), password, data["role"].strip())
        self.destroy()

    @property
    def username_input(self):
        return self.username_entry

    @property
    def role_input(self):
        return self.role_combo