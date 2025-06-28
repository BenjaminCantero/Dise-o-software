import tkinter as tk
from tkinter import ttk

class DashboardPanel(ttk.Frame):
    def __init__(self, parent, sala_service=None, reserva_service=None, user_service=None):
        super().__init__(parent)
        self.sala_service = sala_service
        self.reserva_service = reserva_service
        self.user_service = user_service
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def refrescar_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Segoe UI", 22, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("Card.TFrame", background="#eebbc3", relief="ridge", borderwidth=2)
        style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("CardValue.TLabel", font=("Segoe UI", 18, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Custom.Treeview", font=("Segoe UI", 13), rowheight=32, background="#f4f4f8", fieldbackground="#f4f4f8", borderwidth=0)
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 14, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("Modern.TButton", font=("Segoe UI", 12, "bold"), background="#eebbc3", foreground="#232946", borderwidth=0, padding=8)
        style.map("Modern.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        title = ttk.Label(self, text="Dashboard de Smart-Rooms", style="PanelTitle.TLabel")
        title.pack(pady=20)

        cards_frame = ttk.Frame(self, style="Panel.TFrame")
        cards_frame.pack(pady=10, padx=20, fill="x")

        salas = self.sala_service.get_all() if self.sala_service else []
        total_salas = len(salas)
        ocupadas = len([s for s in salas if s.get("estado") == "ocupada"])
        libres = len([s for s in salas if s.get("estado") == "disponible"])
        reservas = self.reserva_service.get_all() if self.reserva_service else []
        total_reservas = len(reservas)

        card1 = ttk.Frame(cards_frame, style="Card.TFrame")
        card1.grid(row=0, column=0, padx=12, pady=5, sticky="nsew")
        ttk.Label(card1, text="Total de salas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card1, text=total_salas, style="CardValue.TLabel").pack(pady=(0, 10))

        card2 = ttk.Frame(cards_frame, style="Card.TFrame")
        card2.grid(row=0, column=1, padx=12, pady=5, sticky="nsew")
        ttk.Label(card2, text="Salas ocupadas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card2, text=ocupadas, style="CardValue.TLabel").pack(pady=(0, 10))

        card3 = ttk.Frame(cards_frame, style="Card.TFrame")
        card3.grid(row=0, column=2, padx=12, pady=5, sticky="nsew")
        ttk.Label(card3, text="Salas disponibles", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card3, text=libres, style="CardValue.TLabel").pack(pady=(0, 10))

        card4 = ttk.Frame(cards_frame, style="Card.TFrame")
        card4.grid(row=0, column=3, padx=12, pady=5, sticky="nsew")
        ttk.Label(card4, text="Reservas activas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card4, text=total_reservas, style="CardValue.TLabel").pack(pady=(0, 10))

        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        tabla_label = ttk.Label(self, text="Reservas actuales", font=("Segoe UI", 14, "bold"), background="#f4f4f8", foreground="#232946")
        tabla_label.pack(pady=(30, 5))

        tabla_frame = ttk.Frame(self, style="Panel.TFrame")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("sala", "usuario", "fecha", "hora")
        tree = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8, style="Custom.Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=120)
        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        if self.reserva_service and self.sala_service and self.user_service:
            reservas = self.reserva_service.get_all()
            usuarios = {u["id"]: u["username"] for u in self.user_service.get_all()}
            salas = {s["id"]: s["nombre"] for s in self.sala_service.get_all()}
            for reserva in reservas:
                usuario = usuarios.get(reserva.get("usuario_id"), "None")
                sala = salas.get(reserva.get("sala_id"), "None")
                fecha_inicio = reserva.get("fecha_inicio", "None")
                fecha = fecha_inicio[:10] if fecha_inicio else "None"
                hora = fecha_inicio[11:16] if fecha_inicio else "None"
                tree.insert("", "end", values=(sala, usuario, fecha, hora))