from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

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
            self.reserva_service.cancelar_reserva(self.user.id, reserva[1], reserva[2])
            messagebox.showinfo("Éxito", "Reserva cancelada.")
            self.cargar_reservas()

    def crear_reserva(self):
        ventana = tk.Toplevel(self)
        ventana.title("Crear reserva")
        ventana.grab_set()

        # --- Consulta las salas disponibles desde la base de datos ---
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM salas")  # Trae id y nombre
        salas = cursor.fetchall()
        conn.close()

        sala_nombres = [row[1] for row in salas]

        tk.Label(ventana, text="Sala:").grid(row=0, column=0, padx=10, pady=5)
        sala_cb = ttk.Combobox(ventana, values=sala_nombres, state="readonly")
        if sala_nombres:
            sala_cb.set(sala_nombres[0])
        sala_cb.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Fecha:").grid(row=1, column=0, padx=10, pady=5)
        fecha_entry = DateEntry(ventana, date_pattern="yyyy-mm-dd")
        fecha_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Hora:").grid(row=2, column=0, padx=10, pady=5)
        horas = [f"{h:02d}" for h in range(8, 22)]
        minutos = ["00", "15", "30", "45"]
        hora_cb = ttk.Combobox(ventana, values=horas, width=3, state="readonly")
        hora_cb.set(horas[0])
        hora_cb.grid(row=2, column=1, sticky="w", padx=(10,0), pady=5)
        min_cb = ttk.Combobox(ventana, values=minutos, width=3, state="readonly")
        min_cb.set(minutos[0])
        min_cb.grid(row=2, column=1, sticky="e", padx=(0,10), pady=5)

        def confirmar():
            sala_nombre = sala_cb.get()
            fecha = fecha_entry.get()
            hora = f"{hora_cb.get()}:{min_cb.get()}"
            if not sala_nombre:
                messagebox.showwarning("Faltan datos", "Seleccione la sala.")
                return
            # Busca el id de la sala seleccionada
            sala_id = None
            for row in salas:
                if row[1] == sala_nombre:
                    sala_id = row[0]
                    break
            if sala_id is None:
                messagebox.showerror("Error", "No se encontró el ID de la sala seleccionada.")
                return
            try:
                self.reserva_service.crear_reserva(self.user.id, sala_id, fecha, hora)
                messagebox.showinfo("Éxito", "Reserva creada correctamente.")
                self.cargar_reservas()
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la reserva:\n{e}")

        ttk.Button(ventana, text="Confirmar", command=confirmar).grid(row=3, column=0, columnspan=2, pady=10)