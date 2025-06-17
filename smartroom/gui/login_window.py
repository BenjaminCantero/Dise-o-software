import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, root, user_service, on_login):
        super().__init__(root)
        self.title("Iniciar Sesión - Smart-Rooms")
        self.geometry("480x520")
        self.resizable(False, False)
        self.user_service = user_service
        self.on_login = on_login

        # Fondo principal
        self.configure(bg="#232946")

        # Marco central con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=390, height=400)
        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=390)

        # Logo y título
        logo = tk.Label(frame, text="🏢", font=("Arial", 44), bg="#f4f4f8", fg="#eebbc3")
        logo.pack(pady=(28, 0))
        title = tk.Label(frame, text="Smart-Rooms", font=("Arial", 22, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(0, 22))

        # Usuario
        user_label = tk.Label(frame, text="Usuario:", font=("Arial", 13), bg="#f4f4f8", fg="#232946")
        user_label.pack(pady=(5, 0))
        self.username_entry = ttk.Entry(frame, width=28, font=("Arial", 13))
        self.username_entry.pack(ipady=5, pady=(0, 12))

        # Contraseña
        pass_label = tk.Label(frame, text="Contraseña:", font=("Arial", 13), bg="#f4f4f8", fg="#232946")
        pass_label.pack(pady=(5, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=28, font=("Arial", 13))
        self.password_entry.pack(ipady=5, pady=(0, 22))

        # Estilo para el botón principal
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 14, "bold"), background="#eebbc3", foreground="#232946", padding=10)
        style.map("Accent.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        # Botón de inicio de sesión
        login_btn = ttk.Button(frame, text="Iniciar sesión", style="Accent.TButton", command=self.login)
        login_btn.pack(pady=(10, 12), ipadx=12, ipady=4)

        # Botón adicional debajo del formulario
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
        messagebox.showinfo("Crear cuenta", "Funcionalidad para registrar un nuevo usuario.")
        # Aquí puedes implementar o llamar a una ventana de registro
