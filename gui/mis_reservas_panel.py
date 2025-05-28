import tkinter as tk
from tkinter import ttk, messagebox

class MisReservasPanel(ttk.Frame):
    def __init__(self, parent, reserva_service, user):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.user = user
        # Registrar como observer
        if self.reserva_service:
            self.reserva_service.add_observer(self)
        self.configure(style="Panel.TFrame")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.cargar_reservas()

    def update(self, event, data):
        if event in ("reserva_creada", "reserva_eliminada", "reserva_editada"):
            self.cargar_reservas()

    def destroy(self):
        if self.reserva_service:
            self.reserva_service.remove_observer(self)
        super().destroy()

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

        # Tabla de reservas mejorada
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)
        columns = ("Sala", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
            style="Custom.Treeview"
        )
        # Mejorar cabeceras y proporciones
        self.tree.heading("Sala", text="Sala")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Sala", anchor="center", width=180, minwidth=120, stretch=True)
        self.tree.column("Fecha", anchor="center", width=120, minwidth=90, stretch=True)
        self.tree.column("Hora", anchor="center", width=120, minwidth=90, stretch=True)
        self.tree.column("Estado", anchor="center", width=120, minwidth=90, stretch=True)

        # Scrollbar vertical y horizontal
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Alternar color de filas para mejor visualización
        style.configure("Custom.Treeview", font=("Arial", 12), rowheight=28, background="#f4f4f8", fieldbackground="#f4f4f8")
        style.map("Custom.Treeview", background=[("selected", "#eebbc3")])
        style.configure("Custom.Treeview.Heading", font=("Arial", 13, "bold"), background="#eebbc3", foreground="#232946")

        # Botón de cancelar reserva
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cancelar reserva seleccionada", style="Panel.TButton", command=self.cancelar_reserva, width=28).pack()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        reservas = self.reserva_service.obtener_reservas_por_usuario(self.user.username)
        for i, reserva in enumerate(reservas):
            tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
            self.tree.insert("", "end", values=(reserva["sala"], reserva["fecha"], reserva["hora"], reserva["estado"]), tags=tags)
        # Colores alternos para filas
        self.tree.tag_configure("evenrow", background="#f4f4f8")
        self.tree.tag_configure("oddrow", background="#e6e6ef")

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