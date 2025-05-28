import tkinter as tk
from tkinter import ttk, messagebox

class MisReservasPanel(ttk.Frame):
    def __init__(self, parent, reserva_service, user):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.user = user
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.cargar_reservas()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 18, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 22), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="🗓️", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Mis Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Filtro de búsqueda por fecha
        filtro_frame = ttk.Frame(self, style="Panel.TFrame")
        filtro_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(filtro_frame, text="Filtrar por fecha:", background="#f4f4f8", foreground="#232946", font=("Arial", 11)).pack(side="left")
        self.fecha_entry = ttk.Entry(filtro_frame, width=12)
        self.fecha_entry.pack(side="left", padx=5)
        ttk.Button(filtro_frame, text="Buscar", style="Panel.TButton", command=self.cargar_reservas).pack(side="left", padx=5)
        ttk.Button(filtro_frame, text="Limpiar", style="Panel.TButton", command=self.limpiar_filtro).pack(side="left", padx=5)

        # Tabla de reservas
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("Sala", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botón de cancelar reserva
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cancelar reserva seleccionada", style="Panel.TButton", command=self.cancelar_reserva, width=28).pack()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        fecha_filtro = self.fecha_entry.get().strip()
        reservas = self.reserva_service.obtener_reservas_por_usuario(self.user.username)
        for reserva in reservas:
            if fecha_filtro and reserva["fecha"] != fecha_filtro:
                continue
            self.tree.insert("", "end", values=(reserva["sala"], reserva["fecha"], reserva["hora"], reserva["estado"]))

    def limpiar_filtro(self):
        self.fecha_entry.delete(0, tk.END)
        self.cargar_reservas()

    def cancelar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva para cancelar.")
            return
        reserva = self.tree.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas cancelar esta reserva?")
        if respuesta:
            # Ajusta el método según tu modelo de reserva (puede que necesites el ID de la reserva)
            self.reserva_service.cancelar_reserva(self.user.username, reserva[1], reserva[2])
            messagebox.showinfo("Éxito", "Reserva cancelada.")
            self.cargar_reservas()