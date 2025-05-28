import tkinter as tk
from tkinter import ttk

class HorarioPanel(ttk.Frame):
    def __init__(self, parent, reserva_service=None, user=None):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.user = user
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 18, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 22), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])
        style.configure("Custom.Treeview", font=("Arial", 12), rowheight=28, background="#f4f4f8", fieldbackground="#f4f4f8")
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Arial", 13, "bold"), background="#eebbc3", foreground="#232946")

        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Mi Horario de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Tabla de horarios mejorada
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)
        columns = ("Sala", "Horario", "User")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
            style="Custom.Treeview"
        )
        self.tree.heading("Sala", text="Sala")
        self.tree.heading("Horario", text="Horario")
        self.tree.heading("User", text="User")
        self.tree.column("Sala", anchor="center", width=180, minwidth=120, stretch=True)
        self.tree.column("Horario", anchor="center", width=220, minwidth=150, stretch=True)
        self.tree.column("User", anchor="center", width=180, minwidth=120, stretch=True)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.cargar_horario()

    def cargar_horario(self):
        # Limpia la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Obtiene las reservas desde el servicio
        if self.reserva_service and self.user:
            reservas = self.reserva_service.obtener_reservas_por_usuario(self.user.username)
            for i, reserva in enumerate(reservas):
                sala = reserva.get("sala", "N/A")
                fecha = reserva.get("fecha", "N/A")
                hora = reserva.get("hora", "N/A")
                profesor = reserva.get("usuario", "N/A")
                horario = f"{fecha} {hora}"
                tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
                self.tree.insert("", "end", values=(sala, horario, profesor), tags=tags)
            # Colores alternos para filas
            self.tree.tag_configure("evenrow", background="#f4f4f8")
            self.tree.tag_configure("oddrow", background="#e6e6ef")