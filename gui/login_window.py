import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, root, user_service, on_login):
        super().__init__(root)
        self.title("Iniciar Sesión - Smart-Rooms")
        self.geometry("400x320")
        self.resizable(False, False)
        self.user_service = user_service
        self.on_login = on_login

        # Fondo principal
        self.configure(bg="#232946")

        # Marco central
        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=240)

        # Logo y título
        logo = tk.Label(frame, text="🏢", font=("Arial", 32), bg="#f4f4f8", fg="#eebbc3")
        logo.pack(pady=(10, 0))
        title = tk.Label(frame, text="Smart-Rooms", font=("Arial", 16, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(0, 10))

        # Usuario
        user_label = tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        user_label.pack(pady=(5, 0))
        self.username_entry = ttk.Entry(frame, width=25)
        self.username_entry.pack()

        # Contraseña
        pass_label = tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f4f4f8", fg="#232946")
        pass_label.pack(pady=(10, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=25)
        self.password_entry.pack()

        # Botón de inicio de sesión
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Accent.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        login_btn = ttk.Button(frame, text="Iniciar Sesión", style="Accent.TButton", command=self.login)
        login_btn.pack(pady=18)

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