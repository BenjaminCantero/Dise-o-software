import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, root, user_service, on_login):
        super().__init__(root)
        self.title("Iniciar Sesión - Smart-Rooms")
        self.geometry("520x600")  # Aumentado para mejor visibilidad de botones y campos
        self.resizable(False, False)
        self.user_service = user_service
        self.on_login = on_login

        # Fondo principal
        self.configure(bg="#232946")

        # Marco central con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=430, height=480)
        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=470)

        # Logo y título
        logo = tk.Label(frame, text="🏢", font=("Arial", 44), bg="#f4f4f8", fg="#eebbc3")
        logo.pack(pady=(25, 0))
        title = tk.Label(frame, text="Smart-Rooms", font=("Arial", 22, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(0, 16))

        # Usuario
        user_label = tk.Label(frame, text="Usuario:", font=("Arial", 13), bg="#f4f4f8", fg="#232946")
        user_label.pack(pady=(4, 0))
        self.username_entry = ttk.Entry(frame, width=28, font=("Arial", 13))
        self.username_entry.pack(ipady=5, pady=(0, 10))

        # Contraseña
        pass_label = tk.Label(frame, text="Contraseña:", font=("Arial", 13), bg="#f4f4f8", fg="#232946")
        pass_label.pack(pady=(4, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=28, font=("Arial", 13))
        self.password_entry.pack(ipady=5, pady=(0, 16))

        # Estilo para el botón principal
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 14, "bold"), background="#eebbc3", foreground="#232946", padding=10)
        style.map("Accent.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        # Botón de inicio de sesión
        login_btn = ttk.Button(frame, text="Iniciar sesión", style="Accent.TButton", command=self.login)
        login_btn.pack(pady=(4, 8), ipadx=12, ipady=4, fill="x", padx=30)

        # Mejor diseño para el botón 'Agregar usuario', igual tamaño y estilo que 'Iniciar sesión'
        style.configure("Accent2.TButton", font=("Arial", 14, "bold"), background="#eebbc3", foreground="#232946", padding=10)
        style.map("Accent2.TButton", background=[("active", "#f4f4f8")], foreground=[("active", "#232946")])

        add_user_btn = ttk.Button(frame, text="➕  Crear usuario", style="Accent2.TButton", command=self.add_user_dialog)
        add_user_btn.pack(pady=(8, 0), ipadx=12, ipady=4, fill="x", padx=30)

        # Permite presionar Enter para iniciar sesión
        self.bind("<Return>", lambda event: self.login())
        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.user_service.autenticar(username, password)
        if user:
            self.on_login(user)
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def edit_user_info(self):
        # Ventana para editar información del usuario actual
        user = getattr(self, 'current_user', None)
        if not user:
            messagebox.showinfo("Información", "Debes iniciar sesión para editar tus datos.")
            return
        def guardar_cambios():
            nuevo_username = username_entry.get().strip()
            nueva_contraseña = password_entry.get().strip()
            nuevo_rol = role_var.get().strip()
            if not nuevo_username or not nuevo_rol:
                messagebox.showerror("Error", "El nombre de usuario y el rol son obligatorios.")
                return
            try:
                self.user_service.update(user['id'], nuevo_username, nueva_contraseña, nuevo_rol)
                messagebox.showinfo("Éxito", "Información actualizada correctamente.")
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la información: {e}")

        edit_win = tk.Toplevel(self)
        edit_win.title("Editar mi información")
        edit_win.geometry("370x320")
        edit_win.configure(bg="#232946")
        edit_win.resizable(False, False)
        edit_win.transient(self)
        edit_win.grab_set()

        frame = tk.Frame(edit_win, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)
        frame.pack_propagate(False)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        username_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        username_entry.pack(ipady=3)
        username_entry.insert(0, user['username'])

        tk.Label(frame, text="Nueva contraseña (opcional):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        password_entry = ttk.Entry(frame, show="*", width=30, font=("Arial", 11))
        password_entry.pack(ipady=3)

        tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        role_var = tk.StringVar(value=user.get('role', 'estudiante'))
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=["admin", "profesor", "estudiante"], state="readonly", width=28)
        role_combo.pack(ipady=3)
        role_combo.current(["admin", "profesor", "estudiante"].index(user.get('role', 'estudiante')))

        style = ttk.Style()
        style.configure("Dialog.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("Dialog.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar cambios", style="Dialog.TButton", command=guardar_cambios).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Dialog.TButton", command=edit_win.destroy).pack(side="left", padx=8)

        username_entry.focus_set()

    def add_user_dialog(self):
        def guardar_usuario():
            nuevo_username = username_entry.get().strip()
            nueva_contraseña = password_entry.get().strip()
            nuevo_rol = role_var.get().strip()
            if not nuevo_username or not nueva_contraseña or not nuevo_rol:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                self.user_service.create(nuevo_username, nueva_contraseña, nuevo_rol)
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
                add_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {e}")

        add_win = tk.Toplevel(self)
        add_win.title("Agregar usuario")
        add_win.geometry("370x320")
        add_win.configure(bg="#232946")
        add_win.resizable(False, False)
        add_win.transient(self)
        add_win.grab_set()

        frame = tk.Frame(add_win, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)
        frame.pack_propagate(False)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        username_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        username_entry.pack(ipady=3)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        password_entry = ttk.Entry(frame, show="*", width=30, font=("Arial", 11))
        password_entry.pack(ipady=3)

        tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        role_var = tk.StringVar(value="estudiante")
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=["admin", "profesor", "estudiante"], state="readonly", width=28)
        role_combo.pack(ipady=3)
        role_combo.current(2)

        style = ttk.Style()
        style.configure("Dialog.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("Dialog.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar usuario", style="Dialog.TButton", command=guardar_usuario).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Dialog.TButton", command=add_win.destroy).pack(side="left", padx=8)

        username_entry.focus_set()
