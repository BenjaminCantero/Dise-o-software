import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class MisReservasPanel(ttk.Frame):
    def __init__(self, parent, reserva_service, user):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.user = user
        self.create_widgets()
        self.cargar_reservas()

    def create_widgets(self):
        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(pady=10)
        ttk.Label(filtro_frame, text="Filtrar por fecha:").pack(side="left")
        self.fecha_entry = ttk.Entry(filtro_frame, width=12)
        self.fecha_entry.pack(side="left", padx=5)
        ttk.Button(filtro_frame, text="Buscar", command=self.cargar_reservas).pack(side="left")

        self.tree = ttk.Treeview(self, columns=("Sala", "Fecha", "Hora", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, pady=10)

        # Frame para los botones centrados
        botones_frame = ttk.Frame(self)
        botones_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("Custom.TButton",
            borderwidth=1,
            relief="solid",
            foreground="#1a1a2e",
            background="#fff",
            font=("Arial", 10, "bold")
        )
        style.map("Custom.TButton",
            background=[("active", "#f8e1ea")],
            bordercolor=[("!active", "#e3bfc7"), ("active", "#e3bfc7")]
        )

        cancelar_btn = ttk.Button(
            botones_frame,
            text="Cancelar reserva seleccionada",
            command=self.cancelar_reserva,
            width=25,
            style="Custom.TButton"
        )
        cancelar_btn.pack(side="left", padx=10)

        crear_btn = ttk.Button(
            botones_frame,
            text="Crear reserva",
            command=self.crear_reserva,
            width=15,
            style="Custom.TButton"
        )
        crear_btn.pack(side="left", padx=10)

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        fecha_filtro = self.fecha_entry.get().strip()
        reservas = self.reserva_service.obtener_reservas_por_usuario(self.user.username)
        for reserva in reservas:
            if fecha_filtro and reserva["fecha"] != fecha_filtro:
                continue
            self.tree.insert("", "end", values=(reserva["sala"], reserva["fecha"], reserva["hora"], reserva["estado"]))

    def cancelar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva para cancelar.")
            return
        reserva = self.tree.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas cancelar esta reserva?")
        if respuesta:
            self.reserva_service.cancelar_reserva(self.user["id"], reserva[1], reserva[2])  # Ajusta según tu modelo
            messagebox.showinfo("Éxito", "Reserva cancelada.")
            self.cargar_reservas()

    def crear_reserva(self):
        sala = simpledialog.askstring("Crear reserva", "Ingrese la sala:")
        if not sala:
            return
        fecha = simpledialog.askstring("Crear reserva", "Ingrese la fecha (YYYY-MM-DD):")
        if not fecha:
            return
        hora = simpledialog.askstring("Crear reserva", "Ingrese la hora (HH:MM):")
        if not hora:
            return

        try:
            self.reserva_service.crear_reserva(self.user["id"], sala, fecha, hora)
            messagebox.showinfo("Éxito", "Reserva creada correctamente.")
            self.cargar_reservas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la reserva:\n{e}")