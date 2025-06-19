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
        # Elimina widgets y vuelve a crear el dashboard actualizado
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 20, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("Card.TFrame", background="#eebbc3", relief="ridge", borderwidth=2)
        style.configure("CardTitle.TLabel", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946")
        style.configure("CardValue.TLabel", font=("Arial", 18, "bold"), background="#eebbc3", foreground="#232946")

        # Título
        title = ttk.Label(self, text="Dashboard de Smart-Rooms", style="PanelTitle.TLabel")
        title.pack(pady=20)

        # Cuadros resumen (cards)
        cards_frame = ttk.Frame(self, style="Panel.TFrame")
        cards_frame.pack(pady=10, padx=20, fill="x")

        total_salas = len(self.sala_service.listar_salas()) if self.sala_service else 0
        ocupadas = len([s for s in self.sala_service.listar_salas() if s["estado"] == "ocupada"]) if self.sala_service else 0
        libres = len([s for s in self.sala_service.listar_salas() if s["estado"] == "disponible"]) if self.sala_service else 0
        total_reservas = len(self.reserva_service.listar_reservas()) if self.reserva_service else 0

        # Card: Total de salas
        card1 = ttk.Frame(cards_frame, style="Card.TFrame")
        card1.grid(row=0, column=0, padx=12, pady=5, sticky="nsew")
        ttk.Label(card1, text="Total de salas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card1, text=total_salas, style="CardValue.TLabel").pack(pady=(0, 10))

        # Card: Salas ocupadas
        card2 = ttk.Frame(cards_frame, style="Card.TFrame")
        card2.grid(row=0, column=1, padx=12, pady=5, sticky="nsew")
        ttk.Label(card2, text="Salas ocupadas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card2, text=ocupadas, style="CardValue.TLabel").pack(pady=(0, 10))

        # Card: Salas disponibles
        card3 = ttk.Frame(cards_frame, style="Card.TFrame")
        card3.grid(row=0, column=2, padx=12, pady=5, sticky="nsew")
        ttk.Label(card3, text="Salas disponibles", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card3, text=libres, style="CardValue.TLabel").pack(pady=(0, 10))

        # Card: Reservas activas
        card4 = ttk.Frame(cards_frame, style="Card.TFrame")
        card4.grid(row=0, column=3, padx=12, pady=5, sticky="nsew")
        ttk.Label(card4, text="Reservas activas", style="CardTitle.TLabel").pack(pady=(10, 2))
        ttk.Label(card4, text=total_reservas, style="CardValue.TLabel").pack(pady=(0, 10))

        # Ajuste de columnas para que las cards se expandan
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        # Tabla de reservas actuales
        tabla_label = ttk.Label(self, text="Reservas actuales", font=("Arial", 14, "bold"), background="#f4f4f8", foreground="#232946")
        tabla_label.pack(pady=(30, 5))

        tabla_frame = ttk.Frame(self, style="Panel.TFrame")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("sala", "usuario", "fecha", "hora")
        tree = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=120)
        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Cargar reservas actuales
        if self.reserva_service:
            reservas = self.reserva_service.listar_reservas()
            for reserva in reservas:
                sala = reserva.get("sala") if isinstance(reserva, dict) else getattr(reserva, "sala", "")
                usuario = reserva.get("usuario") if isinstance(reserva, dict) else getattr(reserva, "usuario", "")
                fecha = reserva.get("fecha") if isinstance(reserva, dict) else getattr(reserva, "fecha", "")
                hora = reserva.get("hora") if isinstance(reserva, dict) else getattr(reserva, "hora", "")
                tree.insert("", "end", values=(sala, usuario, fecha, hora))