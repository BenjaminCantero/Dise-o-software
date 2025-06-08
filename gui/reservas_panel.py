from tkcalendar import DateEntry  # Agrega esta importación
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from commands.cancel_reserva_command import CreateReservaCommand, CancelReservaCommand, EditReservaCommand  # Importa los comandos

class ReservasPanel(ttk.Frame):
    def __init__(self, parent, mediator, sala_service, user_service, reserva_service, user, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.sala_service = sala_service
        self.user_service = user_service
        self.reserva_service = reserva_service
        self.user = user
        self.on_volver = on_volver
        self.create_widgets()
        # --- PATRÓN MEDIATOR: Registrar el panel ---
        if self.mediator:
            self.mediator.register("reservas_panel", self)
        # --- PATRÓN OBSERVER: Registrar como observador ---
        if self.reserva_service:
            self.reserva_service.add_observer(self)

    def update(self, event, data):
        if event == "reserva_editada":
            messagebox.showinfo("Éxito", "La reserva ha sido modificada con éxito.")
            self.cargar_reservas()
        elif event in ("reserva_creada", "reserva_eliminada"):
            self.cargar_reservas()

    # --- PATRÓN MEDIATOR: Método para recibir eventos ---
    def on_event(self, sender, event, data):
        if event in ("reserva_creada", "reserva_eliminada", "reserva_editada"):
            self.cargar_reservas()

    def destroy(self):
        # --- PATRÓN MEDIATOR: Desregistrar el panel ---
        if self.mediator:
            self.mediator.unregister("reservas_panel")
        # --- PATRÓN OBSERVER: Quitar como observador ---
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

        # Marco superior con título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Filtro de búsqueda
        filter_frame = ttk.Frame(self, style="Panel.TFrame")
        filter_frame.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(filter_frame, text="Buscar por usuario:", background="#f4f4f8", foreground="#232946", font=("Arial", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Buscar", style="Panel.TButton", command=self.filtrar_reservas).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Limpiar", style="Panel.TButton", command=self.cargar_reservas).pack(side="left", padx=5)

        # Tabla de reservas con scrollbar
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("id", "sala", "usuario", "fecha", "hora")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col, ancho in zip(columns, [50, 120, 120, 100, 80]):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=ancho, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Nueva Reserva", style="Panel.TButton", command=self.nueva_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Reserva", style="Panel.TButton", command=self.eliminar_reserva, width=18).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Reserva", style="Panel.TButton", command=self.editar_reserva, width=18).pack(side="left", padx=8)

        ttk.Button(self, text="Volver al inicio", style="Panel.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.reserva_service:
            reservas = self.reserva_service.listar_reservas()
            # Filtrado por rol
            if hasattr(self, "user") and hasattr(self.user, "role"):
                if self.user.role in ("estudiante", "profesor"):
                    # Solo sus reservas
                    reservas = [r for r in reservas if r["usuario"] == self.user.username]
                # Si es admin, ve todas
            for reserva in reservas:
                self.tree.insert("", "end", values=(
                    reserva["id"], reserva["sala"], reserva["usuario"], reserva["fecha"], reserva["hora"]
                ))

    def filtrar_reservas(self):
        filtro = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if self.reserva_service:
            reservas = self.reserva_service.listar_reservas()
            for reserva in reservas:
                if filtro in str(reserva["usuario"]).lower():
                    self.tree.insert("", "end", values=(
                        reserva["id"], reserva["sala"], reserva["usuario"], reserva["fecha"], reserva["hora"]
                    ))

    def nueva_reserva(self):
        salas = [s["nombre"] for s in self.sala_service.listar_salas()]
        usuarios = [u.username for u in self.user_service.listar_usuarios()]

        dialog = tk.Toplevel(self)
        dialog.title("Nueva Reserva")
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg="#f4f4f8")

        frm = ttk.Frame(dialog, style="Panel.TFrame")
        frm.pack(padx=25, pady=20, fill="both", expand=True)

        ttk.Label(frm, text="Crear Nueva Reserva", style="PanelTitle.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 18))

        # Sala
        ttk.Label(frm, text="Sala:", style="PanelTitle.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        sala_var = tk.StringVar()
        sala_cb = ttk.Combobox(frm, textvariable=sala_var, values=salas, state="readonly", font=("Arial", 12))
        sala_cb.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        # Usuario (solo admin)
        if hasattr(self.user, "role") and self.user.role == "admin":
            ttk.Label(frm, text="Usuario:", style="PanelTitle.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
            usuario_var = tk.StringVar()
            usuario_cb = ttk.Combobox(frm, textvariable=usuario_var, values=usuarios, state="readonly", font=("Arial", 12))
            usuario_cb.grid(row=2, column=1, padx=8, pady=6, sticky="w")
        else:
            usuario_var = tk.StringVar(value=self.user.username)

        # Fecha
        ttk.Label(frm, text="Fecha:", style="PanelTitle.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
        fecha_var = tk.StringVar()
        fecha_entry = DateEntry(frm, textvariable=fecha_var, date_pattern="yyyy-mm-dd", font=("Arial", 12))
        fecha_entry.grid(row=3, column=1, padx=8, pady=6, sticky="w")

        # Hora
        ttk.Label(frm, text="Hora (24h):", style="PanelTitle.TLabel").grid(row=4, column=0, padx=8, pady=6, sticky="e")
        hora_var = tk.StringVar(value="12")
        spin_hora = ttk.Spinbox(frm, from_=0, to=23, wrap=True, textvariable=hora_var, width=5, font=("Arial", 12), format="%02.0f")
        spin_hora.grid(row=4, column=1, padx=8, pady=6, sticky="w")

        # Minuto
        ttk.Label(frm, text="Minuto:", style="PanelTitle.TLabel").grid(row=5, column=0, padx=8, pady=6, sticky="e")
        minuto_var = tk.StringVar(value="00")
        spin_minuto = ttk.Spinbox(frm, from_=0, to=59, wrap=True, textvariable=minuto_var, width=5, font=("Arial", 12), format="%02.0f")
        spin_minuto.grid(row=5, column=1, padx=8, pady=6, sticky="w")

        # Botón guardar
        def guardar():
            sala = sala_var.get()
            usuario = usuario_var.get()
            fecha = fecha_var.get()
            hora = hora_var.get()
            minuto = minuto_var.get()
            if not sala or not usuario or not fecha or not hora or not minuto:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                return
            if not (hora.isdigit() and minuto.isdigit()):
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos en hora y minuto.", parent=dialog)
                return
            try:
                fecha_inicio = datetime.strptime(f"{fecha} {hora}:{minuto}", "%Y-%m-%d %H:%M")
                fecha_fin = fecha_inicio.replace(hour=(fecha_inicio.hour + 1) % 24)
                reserva_data = {
                    "sala_nombre": sala,
                    "usuario_username": usuario,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
                command = CreateReservaCommand(self.reserva_service, reserva_data)
                command.execute()
                messagebox.showinfo("Éxito", "Reserva creada correctamente.", parent=dialog)
                dialog.destroy()
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_creada")
            except Exception:
                messagebox.showerror("Error", "Por favor, ingrese valores correctos.", parent=dialog)

        ttk.Button(frm, text="Guardar", style="Panel.TButton", command=guardar).grid(row=6, column=0, columnspan=2, pady=18)

        # Centrar el formulario
        dialog.update_idletasks()
        w = dialog.winfo_width()
        h = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"+{x}+{y}")

    def eliminar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar.")
            return
        item = self.tree.item(seleccion[0])
        reserva_id = item["values"][0]
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar la reserva seleccionada?")
        if confirm:
            try:
                command = CancelReservaCommand(self.reserva_service, reserva_id)
                command.execute()
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente.")
                self.cargar_reservas()
                # --- PATRÓN MEDIATOR: Notificar evento ---
                if self.mediator:
                    self.mediator.notify(self, "reserva_eliminada", data=reserva_id)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def editar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")
            return
        if self.reserva_service:
            reserva_id = self.tree.item(seleccion[0])["values"][0]
            reserva = next((r for r in self.reserva_service.listar_reservas() if r["id"] == reserva_id), None)
            if reserva:
                salas = [s["nombre"] for s in self.sala_service.listar_salas()]
                usuarios = [u.username for u in self.user_service.listar_usuarios()]
                def on_save(sala, usuario, fecha, hora):
                    try:
                        fecha_inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                        fecha_fin = fecha_inicio.replace(hour=(fecha_inicio.hour + 1) % 24)
                        new_data = {
                            "sala_nombre": sala,
                            "usuario_username": usuario,
                            "fecha_inicio": fecha_inicio,
                            "fecha_fin": fecha_fin
                        }
                        command = EditReservaCommand(self.reserva_service, reserva["id"], new_data)
                        command.execute()
                        self.cargar_reservas()
                    except Exception:
                        messagebox.showerror("Error", "Por favor, ingrese valores correctos.", parent=dialog)
                dialog = tk.Toplevel(self)
                dialog.title("Editar Reserva")
                dialog.grab_set()
                dialog.resizable(False, False)

                tk.Label(dialog, text="Sala:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                sala_var = tk.StringVar(value=reserva["sala"])
                sala_cb = ttk.Combobox(dialog, textvariable=sala_var, values=salas, state="readonly")
                sala_cb.grid(row=0, column=1, padx=10, pady=5)

                # Solo admin puede editar el usuario, los demás no pueden cambiarlo
                if hasattr(self.user, "role") and self.user.role == "admin":
                    tk.Label(dialog, text="Usuario:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
                    usuario_var = tk.StringVar(value=reserva["usuario"])
                    usuario_cb = ttk.Combobox(dialog, textvariable=usuario_var, values=usuarios, state="readonly")
                    usuario_cb.grid(row=1, column=1, padx=10, pady=5)
                else:
                    usuario_var = tk.StringVar(value=reserva["usuario"])

                tk.Label(dialog, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
                fecha_var = tk.StringVar(value=reserva["fecha"])
                tk.Entry(dialog, textvariable=fecha_var).grid(row=2, column=1, padx=10, pady=5)

                tk.Label(dialog, text="Hora (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
                hora_var = tk.StringVar(value=reserva["hora"])
                tk.Entry(dialog, textvariable=hora_var).grid(row=3, column=1, padx=10, pady=5)

                def guardar_cambios():
                    sala = sala_var.get()
                    usuario = usuario_var.get()
                    fecha = fecha_var.get()
                    hora = hora_var.get()
                    if not sala or not usuario or not fecha or not hora:
                        messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                        return
                    try:
                        on_save(sala, usuario, fecha, hora)
                        dialog.destroy()
                    except Exception:
                        messagebox.showerror("Error", "Por favor, ingrese valores correctos.", parent=dialog)

                ttk.Button(dialog, text="Guardar cambios", command=guardar_cambios).grid(row=4, column=0, columnspan=2, pady=10)
                dialog.wait_window()
