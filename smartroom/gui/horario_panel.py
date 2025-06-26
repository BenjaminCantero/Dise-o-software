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
        style.configure("PanelTitle.TLabel", font=("Arial", 20, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 26), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Custom.Treeview", font=("Arial", 13), rowheight=30, background="#f4f4f8", fieldbackground="#f4f4f8")
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Arial", 14, "bold"), background="#eebbc3", foreground="#232946")

        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(18, 0), padx=18)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 12))
        label = ttk.Label(top_frame, text="Horario de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Subtítulo con nombre y rol
        if self.user:
            rol = self.user["role"].capitalize()
            nombre = self.user["username"]
            subtitulo = ttk.Label(
                top_frame,
                text=f"Mostrando reservas para: {nombre} ({rol})",
                font=("Arial", 12),
                background="#f4f4f8",
                foreground="#232946"
            )
            subtitulo.pack(side="left", padx=(20, 0))

        # Tabla de horarios
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=40, pady=24)
        columns = ("Sala", "Fecha", "Hora inicio", "Hora fin")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14,
            style="Custom.Treeview"
        )
        for col, ancho in zip(columns, [160, 120, 110, 110]):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=ancho, minwidth=80, stretch=True)

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
        reservas = []
        if self.reserva_service:
            # Obtén todas las reservas desde el servicio
            reservas = self.reserva_service.get_all()
            # Filtra según el rol del usuario
            if self.user and "role" in self.user:
                if self.user["role"] in ("estudiante", "profesor"):
                    reservas = [r for r in reservas if r.get("usuario_username") == self.user["username"]]
        for i, reserva in enumerate(reservas):
            sala = reserva.get("sala_nombre", "N/A")
            fecha_inicio = reserva.get("fecha_inicio", "N/A")
            fecha_fin = reserva.get("fecha_fin", "N/A")
            # Formatea fecha y hora
            try:
                fecha = str(fecha_inicio)[:10]
                hora_inicio = str(fecha_inicio)[11:16]
                hora_fin = str(fecha_fin)[11:16]
            except Exception:
                fecha = str(fecha_inicio)
                hora_inicio = ""
                hora_fin = ""
            tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
            self.tree.insert(
                "", "end",
                values=(sala, fecha, hora_inicio, hora_fin),
                tags=tags
            )
        # Colores alternos para filas
        self.tree.tag_configure("evenrow", background="#f4f4f8")
        self.tree.tag_configure("oddrow", background="#e6e6ef")