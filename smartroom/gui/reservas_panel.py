from tkcalendar import DateEntry
from tkinter import ttk, messagebox, Toplevel, StringVar, Label, Entry, Button
from datetime import datetime

class ReservasPanel(ttk.Frame):
    def __init__(self, parent, mediator=None, reserva_service=None, sala_service=None, user_service=None, user=None, on_volver=None):
        super().__init__(parent)
        self.mediator = mediator
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.user = user
        self.on_volver = on_volver
        self._setup_styles()
        self.create_widgets()
        if self.mediator:
            self.mediator.register("reservas_panel", self)

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Panel.TFrame", background="#f4f4f8")
        style.configure("PanelTitle.TLabel", font=("Arial", 20, "bold"), background="#f4f4f8", foreground="#232946")
        style.configure("PanelIcon.TLabel", font=("Arial", 28), background="#f4f4f8", foreground="#eebbc3")
        style.configure("Panel.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946")
        style.map("Panel.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

    def create_widgets(self):
        # Título e icono
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(10, 0), padx=10)
        icon = ttk.Label(top_frame, text="📅", style="PanelIcon.TLabel")
        icon.pack(side="left", padx=(0, 10))
        label = ttk.Label(top_frame, text="Gestión de Reservas", style="PanelTitle.TLabel")
        label.pack(side="left")

        # Tabla de reservas
        table_frame = ttk.Frame(self, style="Panel.TFrame")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        columns = ("id", "usuario", "sala", "inicio", "fin")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("sala", text="Sala")
        self.tree.heading("inicio", text="Fecha Inicio")
        self.tree.heading("fin", text="Fecha Fin")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("usuario", width=120, anchor="center")
        self.tree.column("sala", width=120, anchor="center")
        self.tree.column("inicio", width=150, anchor="center")
        self.tree.column("fin", width=150, anchor="center")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = ttk.Frame(self, style="Panel.TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Nueva Reserva", style="Panel.TButton", width=18, command=self.nueva_reserva).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Eliminar Reserva", style="Panel.TButton", width=18, command=self.eliminar_reserva).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Editar Reserva", style="Panel.TButton", width=18, command=self.editar_reserva).pack(side="left", padx=8)

        ttk.Button(self, text="Volver al inicio", style="Panel.TButton", command=self.on_volver).pack(pady=10)

        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            reservas = self.reserva_service.get_reservas()
            usuarios = {u["id"]: u["username"] for u in self.user_service.get_usuarios()}
            salas = {s["id"]: s["nombre"] for s in self.sala_service.get_salas()}
            for reserva in reservas:
                usuario = usuarios.get(reserva["usuario_id"], "Desconocido")
                sala = salas.get(reserva["sala_id"], "Desconocida")
                self.tree.insert(
                    "", "end",
                    values=(
                        reserva["id"],
                        usuario,
                        sala,
                        reserva["fecha_inicio"].replace("T", " ")[:16],
                        reserva["fecha_fin"].replace("T", " ")[:16]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las reservas:\n{e}")

    def nueva_reserva(self):
        self._abrir_dialogo_reserva("Nueva Reserva")

    def editar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        reservas = self.reserva_service.get_reservas()
        reserva = next((r for r in reservas if r["id"] == reserva_id), None)
        if reserva:
            self._abrir_dialogo_reserva("Editar Reserva", reserva)

    def eliminar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar.")
            return
        reserva_id = self.tree.item(selected[0])["values"][0]
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta reserva?")
        if respuesta:
            try:
                self.reserva_service.delete_reserva(reserva_id)
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_eliminada", reserva_id)
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la reserva:\n{e}")

    def _abrir_dialogo_reserva(self, titulo, reserva=None):
        dialog = Toplevel(self)
        dialog.title(titulo)
        dialog.geometry("420x480")
        dialog.configure(bg="#232946")
        dialog.transient(self)
        dialog.grab_set()

        frame = ttk.Frame(dialog, style="Panel.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=370, height=400)

        label_opts = {"font": ("Arial", 12), "bg": "#f4f4f8", "fg": "#232946"}
        entry_opts = {"font": ("Arial", 11)}

        # Usuario
        Label(frame, text="Usuario:", **label_opts).grid(row=0, column=0, sticky="e", padx=(18, 6), pady=(18, 6))
        usuarios = self.user_service.get_usuarios()
        usuario_var = StringVar()
        usuario_combo = ttk.Combobox(frame, values=[f'{u["id"]}: {u["username"]}' for u in usuarios], state="readonly", textvariable=usuario_var, width=24)
        usuario_combo.grid(row=0, column=1, padx=(6, 18), pady=(18, 6))
        if reserva:
            usuario_combo.set(f'{reserva["usuario_id"]}: {next((u["username"] for u in usuarios if u["id"] == reserva["usuario_id"]), "")}')
        else:
            usuario_combo.current(0)

        # Sala
        Label(frame, text="Sala:", **label_opts).grid(row=1, column=0, sticky="e", padx=(18, 6), pady=6)
        salas = self.sala_service.get_salas()
        sala_var = StringVar()
        sala_combo = ttk.Combobox(frame, values=[f'{s["id"]}: {s["nombre"]}' for s in salas], state="readonly", textvariable=sala_var, width=24)
        sala_combo.grid(row=1, column=1, padx=(6, 18), pady=6)
        if reserva:
            sala_combo.set(f'{reserva["sala_id"]}: {next((s["nombre"] for s in salas if s["id"] == reserva["sala_id"]), "")}')
        else:
            sala_combo.current(0)

        # Fecha y hora inicio
        Label(frame, text="Fecha Inicio:", **label_opts).grid(row=2, column=0, sticky="e", padx=(18, 6), pady=6)
        fecha_inicio = DateEntry(frame, width=22)
        fecha_inicio.grid(row=2, column=1, padx=(6, 18), pady=6)
        Label(frame, text="Hora Inicio (HH:MM):", **label_opts).grid(row=3, column=0, sticky="e", padx=(18, 6), pady=6)
        hora_inicio = Entry(frame, **entry_opts, width=26)
        hora_inicio.grid(row=3, column=1, padx=(6, 18), pady=6)

        # Fecha y hora fin
        Label(frame, text="Fecha Fin:", **label_opts).grid(row=4, column=0, sticky="e", padx=(18, 6), pady=6)
        fecha_fin = DateEntry(frame, width=22)
        fecha_fin.grid(row=4, column=1, padx=(6, 18), pady=6)
        Label(frame, text="Hora Fin (HH:MM):", **label_opts).grid(row=5, column=0, sticky="e", padx=(18, 6), pady=6)
        hora_fin = Entry(frame, **entry_opts, width=26)
        hora_fin.grid(row=5, column=1, padx=(6, 18), pady=6)

        # Rellenar datos si es edición
        if reserva:
            try:
                fi = reserva["fecha_inicio"]
                ff = reserva["fecha_fin"]
                if "T" in fi:
                    fecha_i, hora_i = fi.split("T")
                    hora_i = hora_i[:5]
                else:
                    fecha_i, hora_i = fi[:10], fi[11:16]
                if "T" in ff:
                    fecha_f, hora_f = ff.split("T")
                    hora_f = hora_f[:5]
                else:
                    fecha_f, hora_f = ff[:10], ff[11:16]
                fecha_inicio.set_date(fecha_i)
                hora_inicio.delete(0, "end")
                hora_inicio.insert(0, hora_i)
                fecha_fin.set_date(fecha_f)
                hora_fin.delete(0, "end")
                hora_fin.insert(0, hora_f)
            except Exception:
                pass

        # Botones
        btn_frame = ttk.Frame(frame, style="Panel.TFrame")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(24, 0))
        ttk.Button(btn_frame, text="Guardar", style="Panel.TButton", command=lambda: guardar()).pack(side="left", padx=12)
        ttk.Button(btn_frame, text="Cancelar", style="Panel.TButton", command=dialog.destroy).pack(side="left", padx=12)

        def guardar():
            usuario_val = usuario_combo.get()
            sala_val = sala_combo.get()
            hora_ini_val = hora_inicio.get().strip()
            hora_fin_val = hora_fin.get().strip()
            if not usuario_val or not sala_val or not hora_ini_val or not hora_fin_val:
                messagebox.showwarning("Campos incompletos", "Completa todos los campos antes de guardar.")
                return

            try:
                usuario_id = int(usuario_val.split(":")[0])
                sala_id = int(sala_val.split(":")[0])
                fecha_ini = f"{fecha_inicio.get()}T{hora_ini_val}:00"
                fecha_fin_str = f"{fecha_fin.get()}T{hora_fin_val}:00"
                if reserva:
                    self.reserva_service.update_reserva(reserva["id"], usuario_id, sala_id, fecha_ini, fecha_fin_str)
                else:
                    self.reserva_service.create_reserva(usuario_id, sala_id, fecha_ini, fecha_fin_str)
                self.cargar_reservas()
                if self.mediator:
                    self.mediator.notify(self, "reserva_editada" if reserva else "reserva_creada")
                dialog.destroy()
                messagebox.showinfo("Éxito", "Reserva guardada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la reserva:\n{e}")

        dialog.bind("<Return>", lambda event: guardar())
        usuario_combo.focus_set()

    def on_event(self, sender, event, data):
        self.cargar_reservas()