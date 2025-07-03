import tkinter as tk
from tkinter import ttk, messagebox
from mediator.app_mediator import EventListener
from factories.dialog_factory import DialogFactory
from adapters.usuario_dialog_adapter import UsuarioDialogAdapter
from builders.usuario_builder import UsuarioBuilder
from commands.user_commands import CreateUsuarioCommand, EditUsuarioCommand, DeleteUsuarioCommand

class AdminPanel(EventListener, ttk.Frame):
    def __init__(self, parent, mediator, user_service=None, on_volver=None, dialog_factory=None):
        super().__init__(parent)
        self.mediator = mediator
        self.user_service = user_service
        self.on_volver = on_volver
        self.dialog_factory = dialog_factory  # Inyecta la factory
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        # --- PATRÓN MEDIATOR: Registrar el panel ---
        if self.mediator:
            self.mediator.register("admin_panel", self)

    # --- PATRÓN MEDIATOR: Método para recibir eventos ---
    def on_event(self, sender, event, data):
        if event in ("usuario_creado", "usuario_eliminado", "usuario_editado"):
            self.cargar_usuarios()

    def destroy(self):
        # --- PATRÓN MEDIATOR: Desregistrar el panel ---
        if self.mediator:
            self.mediator.unregister("admin_panel")
        super().destroy()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Segoe UI", 22, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Segoe UI Emoji", 32), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Card.TFrame", background="#eebbc3", relief="ridge", borderwidth=2)
        style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("CardValue.TLabel", font=("Segoe UI", 18, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Custom.Treeview", font=("Segoe UI", 13), rowheight=32, background="#f4f4f8", fieldbackground="#f4f4f8", borderwidth=0)
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 14, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Modern.TButton", font=("Segoe UI", 12, "bold"), background="#eebbc3", foreground="#232946", borderwidth=0, padding=8)
        style.map("Modern.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(18, 0), padx=18)
        icon = ttk.Label(top_frame, text="👤", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 12))
        label = ttk.Label(top_frame, text="Gestión de Usuarios", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Cards resumen
        cards_frame = ttk.Frame(self, style="Panel.TFrame")
        cards_frame.pack(pady=10, padx=20, fill="x")

        usuarios = self.user_service.get_all() if self.user_service else []
        total_usuarios = len(usuarios)
        admins = len([u for u in usuarios if u["role"] == "admin"])
        profesores = len([u for u in usuarios if u["role"] == "profesor"])
        estudiantes = len([u for u in usuarios if u["role"] == "estudiante"])

        card_data = [
            ("Total usuarios", total_usuarios),
            ("Admins", admins),
            ("Profesores", profesores),
            ("Estudiantes", estudiantes)
        ]
        for i, (title, value) in enumerate(card_data):
            card = ttk.Frame(cards_frame, style="Card.TFrame")
            card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(pady=(10, 2))
            ttk.Label(card, text=value, style="CardValue.TLabel").pack(pady=(0, 10))
            cards_frame.columnconfigure(i, weight=1)

        # Contenedor principal para tabla y botones
        main_container = ttk.Frame(self, style="Panel.TFrame")
        main_container.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=0)
        main_container.columnconfigure(0, weight=1)

        # Tabla de usuarios
        tabla_label = ttk.Label(main_container, text="Cuentas registradas", font=("Segoe UI", 14, "bold"), background="#f4f4f8", foreground="#232946")
        tabla_label.grid(row=0, column=0, sticky="w", pady=(10, 5))

        table_frame = ttk.Frame(main_container, style="Panel.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")
        main_container.rowconfigure(1, weight=1)
        columns = ("username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Custom.Treeview")
        self.tree.heading("username", text="Usuario")
        self.tree.heading("role", text="Rol")
        self.tree.column("username", width=180, anchor="center")
        self.tree.column("role", width=120, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción (siempre visibles abajo)
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(fill="x", pady=(0, 18), padx=20)
        ttk.Button(btn_frame, text="Crear Usuario", style="Modern.TButton", width=18, command=self.create_usuario).pack(side="left", padx=8, pady=8)
        ttk.Button(btn_frame, text="Eliminar Usuario", style="Modern.TButton", width=18, command=self.delete_usuario).pack(side="left", padx=8, pady=8)
        ttk.Button(btn_frame, text="Editar Usuario", style="Modern.TButton", width=18, command=self.editar_usuario).pack(side="left", padx=8, pady=8)

        ttk.Button(self, text="Volver al inicio", style="Modern.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        if self.user_service:
            for row in self.tree.get_children():
                self.tree.delete(row)
            usuarios = self.user_service.get_all()
            for usuario in usuarios:
                self.tree.insert("", "end", values=(usuario["username"], usuario["role"]))

    def create_usuario(self):
        def on_save(username, password, role):
            try:
                usuario_data = (
                    UsuarioBuilder()
                    .set_username(username)
                    .set_password(password)
                    .set_role(role)
                    .build()
                )
                command = CreateUsuarioCommand(self.user_service, usuario_data)
                command.execute()
                self.cargar_usuarios()
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
                if self.mediator:
                    self.mediator.notify(self, "usuario_creado", usuario_data["username"])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario: {e}")
        if self.dialog_factory:
            self.dialog_factory.create_dialog("editar_usuario", self, None, on_save=on_save)
        else:
            # fallback
            from gui.editar_usuario_dialog import EditarUsuarioDialog
            EditarUsuarioDialog(self, None, on_save=on_save)

    def delete_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
            return
        if self.user_service:
            respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este usuario?")
            if respuesta:
                username = self.tree.item(selected[0])["values"][0]
                usuarios = self.user_service.get_all()
                usuario = next((u for u in usuarios if u["username"] == username), None)
                if usuario:
                    # --- Command: ejecuta la acción de eliminar usuario ---
                    command = DeleteUsuarioCommand(self.user_service, usuario["id"])
                    command.execute()
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                    self.cargar_usuarios()
                    if self.mediator:
                        self.mediator.notify(self, "usuario_eliminado", username)
                else:
                    messagebox.showerror("Error", "No se encontró el usuario.")

    def editar_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para editar.")
            return
        username = self.tree.item(selected[0])["values"][0]
        usuarios = self.user_service.get_all()
        usuario = next((u for u in usuarios if u["username"] == username), None)
        if not usuario:
            messagebox.showerror("Error", "No se encontró el usuario.")
            return
        usuario_id = usuario["id"]

        def on_save(username, password, role):
            try:
                if not username or not role:
                    raise Exception("El nombre de usuario y el rol son obligatorios.")
                usuario_data = (
                    UsuarioBuilder()
                    .set_username(username.strip())
                    .set_role(role.strip())
                    .build()
                )
                command = EditUsuarioCommand(self.user_service, usuario_id, usuario_data)
                command.execute()
                self.cargar_usuarios()
                messagebox.showinfo("Éxito", "Usuario editado correctamente.")
                if self.mediator:
                    self.mediator.notify(self, "usuario_editado", username)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar el usuario: {e}")
        if self.dialog_factory:
            self.dialog_factory.create_dialog("editar_usuario", self, usuario, on_save=on_save)
        else:
            from gui.editar_usuario_dialog import EditarUsuarioDialog
            EditarUsuarioDialog(self, usuario, on_save=on_save)