import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from database_setup import DatabaseSetup  # Importar la clase de configuración de la base de datos


class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x400")
        self.root.configure(bg="#343a40")

        # Inicializar la base de datos
        self.db = DatabaseSetup()
        self.db.inicializar_base_datos()

        # Marco principal
        frame = tk.Frame(self.root, bg="#495057", padx=20, pady=20, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(frame, text="Inicio de Sesión", font=("Segoe UI", 18, "bold"), bg="#495057", fg="white").pack(pady=10)

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Segoe UI", 12), bg="#495057", fg="white").pack(anchor="w", pady=(10, 5))
        self.entry_user = tk.Entry(frame, font=("Segoe UI", 12), relief="flat", bg="#e9ecef", fg="#495057")
        self.entry_user.pack(fill="x", pady=5)

        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 12), bg="#495057", fg="white").pack(anchor="w", pady=(10, 5))
        self.entry_pass = tk.Entry(frame, font=("Segoe UI", 12), show="*", relief="flat", bg="#e9ecef", fg="#495057")
        self.entry_pass.pack(fill="x", pady=5)

        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), bg="#007bff", fg="white",
                  activebackground="#0056b3", activeforeground="white", relief="flat",
                  command=self.validar_login).pack(pady=20, fill="x")

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
            app = SistemaGestionSalas(main_root, role, self.db)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def __del__(self):
        self.db.cerrar_conexion()


class SistemaGestionSalas:
    def __init__(self, root, role, db):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        self.role = role
        self.db = db  # Reutilizar la conexión a la base de datos

        # Paleta de colores mejorada
        self.color_fondo = "#f8f9fa"
        self.color_sidebar = "#343a40"
        self.color_principal = "#007bff"
        self.color_secundario = "#0056b3"
        self.color_exito = "#28a745"
        self.color_advertencia = "#dc3545"
        self.color_texto = "#212529"
        self.color_borde = "#dee2e6"

        # Fuentes mejoradas
        self.titulo_font = ("Segoe UI", 18, "bold")
        self.subtitulo_font = ("Segoe UI", 14)
        self.normal_font = ("Segoe UI", 11)
        self.boton_font = ("Segoe UI", 10, "bold")

        # Configurar el estilo general
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configurar estilos personalizados
        self.style.configure("TFrame", background=self.color_fondo)
        self.style.configure("TLabel", background=self.color_fondo,
                             foreground=self.color_texto, font=self.normal_font)
        self.style.configure("TButton", font=self.boton_font,
                             borderwidth=1, relief="solid")
        self.style.map("TButton",
                       foreground=[("active", "white")],
                       background=[("active", self.color_secundario)])

        # Contenedor principal
        self.main_frame = tk.Frame(root, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)

        # ===== SIDEBAR MEJORADO =====
        self.sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo o título
        tk.Label(self.sidebar,
                 text="Gestión de Salas",
                 font=("Segoe UI", 16, "bold"),
                 bg=self.color_sidebar,
                 fg="white",
                 pady=20).pack(fill="x")

        # Separador
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Opciones del menú
        self.menu_opciones = []
        self.crear_menu()

        # Separador final
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Versión del sistema
        tk.Label(self.sidebar,
                 text="v2.0",
                 font=("Segoe UI", 8),
                 bg=self.color_sidebar,
                 fg="#adb5bd").pack(side="bottom", pady=10)

        # ===== CONTENIDO PRINCIPAL =====
        self.content_frame = tk.Frame(self.main_frame, bg=self.color_fondo, padx=30, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Cargar datos iniciales
        self.salas = self.db.obtener_salas()
        self.reservas = self.db.obtener_reservas()

        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()

    def crear_menu(self):
        # Limpiar el menú existente
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        menu_base = [
            ("Inicio", "home", self.mostrar_inicio),
            ("Calendario", "calendar", self.mostrar_calendario),
            ("Salas", "door-open", self.mostrar_salas)
        ]

        menu_admin = [
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas),
            ("Reportes", "file-text", self.mostrar_reportes),
            ("Configuración", "settings", self.mostrar_config)
        ]

        menu_profesor = []  # El profesor solo ve el menú base

        menu_estudiante = [
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas)
        ]

        menu_final = menu_base.copy()

        if self.role == "admin":
            menu_final.extend(menu_admin)
        elif self.role == "profesor":
            menu_final.extend(menu_profesor)
        elif self.role == "estudiante":
            # Insertar "Reservar Sala" después de "Inicio"
            menu_final.insert(1, ("Reservar Sala", "calendar-plus", self.mostrar_reservas))

        for texto, icono, comando in menu_final:
            btn = tk.Button(self.sidebar,
                            text=f"  {texto}",
                            font=self.normal_font,
                            bg=self.color_sidebar,
                            fg="white",
                            activebackground=self.color_secundario,
                            activeforeground="white",
                            anchor="w",
                            padx=15,
                            pady=12,
                            relief="flat",
                            command=comando)
            btn.pack(fill="x", padx=5)

    def mostrar_inicio(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame,
                 text="Panel Principal",
                 font=self.titulo_font,
                 bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_reservas(self):
        pass  # Implementar lógica para mostrar reservas

    def mostrar_calendario(self):
        pass  # Implementar lógica para mostrar calendario

    def mostrar_salas(self):
        pass  # Implementar lógica para mostrar salas

    def mostrar_reportes(self):
        pass  # Implementar lógica para mostrar reportes

    def mostrar_config(self):
        pass  # Implementar lógica para mostrar configuración


if __name__ == "__main__":
    root = tk.Tk()
    login = LoginSistema(root)
    root.mainloop()
