import tkinter as tk
from tkinter import ttk, messagebox
from database_setup import DatabaseSetup
from sistema_gestion import SistemaGestionSalas  # Importar la clase del sistema de gestión

class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("500x500")
        self.root.configure(bg="#2c3e50")

        # Inicializar la base de datos
        self.db = DatabaseSetup()
        self.db.inicializar_base_datos()

        # Marco principal
        frame = tk.Frame(self.root, bg="#ecf0f1", padx=30, pady=30, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(frame, text="Inicio de Sesión", font=("Segoe UI", 20, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Segoe UI", 12), bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(10, 5))
        self.entry_user = tk.Entry(frame, font=("Segoe UI", 12), relief="flat", bg="#dfe6e9", fg="#2c3e50", insertbackground="#2c3e50")
        self.entry_user.pack(fill="x", pady=5, ipady=5)

        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 12), bg="#ecf0f1", fg="#34495e").pack(anchor="w", pady=(10, 5))
        self.entry_pass = tk.Entry(frame, font=("Segoe UI", 12), show="*", relief="flat", bg="#dfe6e9", fg="#2c3e50", insertbackground="#2c3e50")
        self.entry_pass.pack(fill="x", pady=5, ipady=5)

        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white",
                  activebackground="#2980b9", activeforeground="white", relief="flat",
                  command=self.validar_login).pack(pady=20, fill="x", ipady=5)

        # Pie de página
        tk.Label(self.root, text="© 2025 Gestión de Salas", font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7").pack(side="bottom", pady=10)

    def validar_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # Validar credenciales
        result = self.db.obtener_usuario(username, password)

        if result:
            role = result[0]
            messagebox.showinfo("Éxito", f"Bienvenido, {username} ({role})")
            self.root.destroy()  # Cerrar ventana de login

            # Abrir la aplicación principal
            main_root = tk.Tk()
            app = SistemaGestionSalas(main_root, role, self.db, username)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def __del__(self):
        self.db.cerrar_conexion()