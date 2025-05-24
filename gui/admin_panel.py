import tkinter as tk
from tkinter import ttk

class AdminPanel(ttk.Frame):
    def __init__(self, parent, user_service=None, mediator=None):
        super().__init__(parent)
        self.user_service = user_service
        self.mediator = mediator
        # Registrar como observer del servicio de usuarios
        if self.user_service:
            self.user_service.add_observer(self)
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    # Patrón Observer
    def update(self, event, data):
        if event in ("usuario_creado", "usuario_eliminado", "usuario_editado"):
            self.cargar_usuarios()

    def destroy(self):
        if self.user_service:
            self.user_service.remove_observer(self)
        super().destroy()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 20, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 28), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Card.TFrame", background="#eebbc3", relief="ridge", borderwidth=2)
        style.configure("CardTitle.TLabel", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("CardValue.TLabel", font=("Arial", 16, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="👤", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Usuarios", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Cards resumen
        cards_frame = ttk.Frame(self, style="Panel.TFrame")
        cards_frame.pack(pady=10, padx=20, fill="x")

        total_usuarios = len(self.user_service.listar_usuarios()) if self.user_service else 0
        admins = len([u for u in self.user_service.listar_usuarios() if u.role == "admin"]) if self.user_service else 0
        profesores = len([u for u in self.user_service.listar_usuarios() if u.role == "profesor"]) if self.user_service else 0
        estudiantes = len([u for u in self.user_service.listar_usuarios() if u.role == "estudiante"]) if self.user_service else 0

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

        # Tabla de usuarios
        tabla_label = ttk.Label(self, text="Cuentas registradas", font=("Arial", 14, "bold"), background="#f4f4f8", foreground="#232946")
        tabla_label.pack(pady=(30, 5))

        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("username", text="Usuario")
        self.tree.heading("role", text="Rol")
        self.tree.column("username", width=180, anchor="center")
        self.tree.column("role", width=120, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Crear Usuario", style="Panel.TButton", width=18, command=self.crear_usuario).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Usuario", style="Panel.TButton", width=18, command=self.eliminar_usuario).pack(side="left", padx=8)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.user_service:
            usuarios = self.user_service.listar_usuarios()
            for usuario in usuarios:
                self.tree.insert("", "end", values=(usuario.username, usuario.role))

    def crear_usuario(self):
        # Aquí puedes abrir un diálogo para crear usuario (puedes implementarlo después)
        tk.messagebox.showinfo("Crear usuario", "Funcionalidad pendiente de implementar.")

    def eliminar_usuario(self):
        selected = self.tree.selection()
        if selected and self.user_service:
            username = self.tree.item(selected[0])["values"][0]
            # Aquí deberías llamar a un método para eliminar el usuario
            tk.messagebox.showinfo("Eliminar usuario", f"Funcionalidad para eliminar '{username}' pendiente de implementar.")