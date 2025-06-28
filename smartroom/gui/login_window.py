import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, root, user_service, on_login):
        super().__init__(root)
        self.title("Iniciar Sesión - Smart-Rooms")
        self.geometry("480x550")  # Aumentado para que se vea el botón
        self.resizable(False, False)
        self.user_service = user_service
        self.on_login = on_login

        # Fondo principal
        self.configure(bg="#232946")

        # Marco central con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=390, height=420)
        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=410)

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
        login_btn.pack(pady=(4, 8), ipadx=12, ipady=4)

        # Botón "Crear cuenta"
        create_account_btn = ttk.Button(frame, text="Crear cuenta", command=self.create_account)
        create_account_btn.pack(ipady=3)

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

    def create_account(self):
        # Ventana para registrar usuario
        def registrar():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get().strip()
            if not username or not password or not role:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                self.user_service.create(username, password, role)
                messagebox.showinfo("Éxito", "Usuario creado correctamente. Ahora puedes iniciar sesión.")
                reg_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {e}")

        reg_win = tk.Toplevel(self)
        reg_win.title("Registrar nuevo usuario")
        reg_win.geometry("320x260")
        reg_win.resizable(False, False)

        tk.Label(reg_win, text="Usuario:").pack(pady=(18, 0))
        username_entry = ttk.Entry(reg_win, width=24)
        username_entry.pack()

        tk.Label(reg_win, text="Contraseña:").pack(pady=(10, 0))
        password_entry = ttk.Entry(reg_win, show="*", width=24)
        password_entry.pack()

        tk.Label(reg_win, text="Rol:").pack(pady=(10, 0))
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(reg_win, textvariable=role_var, values=["admin", "profesor", "estudiante"], state="readonly")
        role_combo.pack()
        role_combo.current(0)

        ttk.Button(reg_win, text="Registrar", command=registrar).pack(pady=18)

        username_entry.focus_set()
