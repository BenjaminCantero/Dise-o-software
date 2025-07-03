import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from adapters.reserva_dialog_adapter import ReservaDialogAdapter
from builders.reserva_builder import ReservaBuilder
from mediator.app_mediator import EventListener
from commands.cancel_reserva_command import CreateReservaCommand  # Asegúrate de tener este comando

class ReservaApp(EventListener, tk.Tk):
    def __init__(self, reserva_service, sala_service, user_service, mediator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.mediator = mediator
        self.title("Reservas")
        self.geometry("850x650")
        self.configure(bg="#232946")

        # --- PATRÓN MEDIATOR: Registrar el componente ---
        if self.mediator:
            self.mediator.register("reserva_app", self)

        # Marco principal con sombra
        shadow = tk.Frame(self, bg="#1a1a2e")
        shadow.pack(fill="both", expand=True, padx=10, pady=10)
        frame = tk.Frame(shadow, bg="#f4f4f8")
        frame.pack(fill="both", expand=True)

        # Título
        title = tk.Label(frame, text="Gestión de Reservas", font=("Arial", 24, "bold"), bg="#f4f4f8", fg="#232946")
        title.pack(pady=(20, 10))

        # Botón de nueva reserva
        style = ttk.Style()
        style.configure("NuevaReserva.TButton", font=("Arial", 12, "bold"), background="#eebbc3", foreground="#232946", padding=8)
        style.map("NuevaReserva.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        nueva_reserva_btn = ttk.Button(frame, text="Nueva Reserva", style="NuevaReserva.TButton", command=self.nueva_reserva)
        nueva_reserva_btn.pack(pady=(0, 20), ipadx=8, ipady=2)

        # Tabla de reservas
        self.reservas_tree = None
        self.cargar_reservas()

    # --- PATRÓN MEDIATOR: Método para recibir eventos ---
    def on_event(self, sender, event, data):
        if event in ("reserva_creada", "reserva_eliminada", "reserva_editada"):
            self.cargar_reservas()

    def destroy(self):
        # --- PATRÓN MEDIATOR: Desregistrar el componente ---
        if self.mediator:
            self.mediator.unregister("reserva_app")
        super().destroy()

    def nueva_reserva(self):
        NuevaReservaDialog(self, self.reserva_service, self.sala_service, self.user_service, on_success=self.cargar_reservas)

    def cargar_reservas(self):
        if not hasattr(self, "reservas_tree") or self.reservas_tree is None:
            # Crea el Treeview si no existe
            columns = ("id", "usuario", "sala", "inicio", "fin")
            self.reservas_tree = ttk.Treeview(self, columns=columns, show="headings")
            for col in columns:
                self.reservas_tree.heading(col, text=col.capitalize())
                self.reservas_tree.column(col, anchor="center")
            self.reservas_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Limpia la tabla
        for row in self.reservas_tree.get_children():
            self.reservas_tree.delete(row)

        try:
            reservas = self.reserva_service.get_reservas()
            usuarios = {u["id"]: u["username"] for u in self.user_service.get_usuarios()}
            salas = {s["id"]: s["nombre"] for s in self.sala_service.get_salas()}
            for reserva in reservas:
                usuario = usuarios.get(reserva["usuario_id"], "Desconocido")
                sala = salas.get(reserva["sala_id"], "Desconocida")
                self.reservas_tree.insert(
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

class NuevaReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva_service, sala_service, user_service, on_success=None, current_user=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.geometry("370x470")  # Aumenta la altura
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.on_success = on_success
        self.current_user = current_user
        self.configure(bg="#232946")

        # Siempre en primer plano y bloquea la ventana principal
        self.transient(parent)
        self.grab_set()

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)  # Aumenta la altura del frame
        frame.pack_propagate(False)

        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(14, 0))
        self.sala_var = tk.StringVar()
        self.sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=[s["nombre"] for s in self.sala_service.get_all()], state="readonly", width=28)
        self.sala_combo.pack(ipady=3)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar()
        if self.current_user and self.current_user.get("role") == "admin":
            usuarios = [u["username"] for u in self.user_service.get_all()]
            self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=usuarios, state="readonly", width=28)
        else:
            self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=[self.current_user["username"]], state="readonly", width=28)
            self.usuario_var.set(self.current_user["username"])
            self.usuario_combo.config(state="disabled")
        self.usuario_combo.pack(ipady=3)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        from tkcalendar import DateEntry
        self.fecha_entry = DateEntry(frame, width=28, font=("Arial", 11), background="#eebbc3", foreground="#232946", date_pattern="yyyy-mm-dd")
        self.fecha_entry.pack(ipady=3)

        horas = [f"{h:02d}:{m:02d}" for h in range(8, 21) for m in (0, 30)]

        tk.Label(frame, text="Hora de inicio:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_inicio_var = tk.StringVar()
        self.hora_inicio_combo = ttk.Combobox(frame, textvariable=self.hora_inicio_var, values=horas, state="readonly", width=28)
        self.hora_inicio_combo.pack(ipady=3)

        tk.Label(frame, text="Hora de fin:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_fin_var = tk.StringVar()
        self.hora_fin_combo = ttk.Combobox(frame, textvariable=self.hora_fin_var, values=horas, state="readonly", width=28)
        self.hora_fin_combo.pack(ipady=3)

        style = ttk.Style()
        style.configure("Dialog.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("Dialog.TButton", background=[("active", "#eebbc3")], foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="Dialog.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="Dialog.TButton", command=self.destroy).pack(side="left", padx=8)

        self.fecha_entry.focus_set()

    @property
    def usuario_input(self):
        return self.usuario_combo

    @property
    def sala_input(self):
        return self.sala_combo

    @property
    def fecha_input(self):
        return self.fecha_entry

    @property
    def hora_inicio_input(self):
        return self.hora_inicio_combo

    @property
    def hora_fin_input(self):
        return self.hora_fin_combo

    def guardar(self):
        adapter = ReservaDialogAdapter(self)
        data = adapter.get_data()
        usuario_nombre = data.get("usuario")
        sala_nombre = data.get("sala")
        fecha = data.get("fecha")
        hora_inicio = data.get("hora_inicio")
        hora_fin = data.get("hora_fin")

        if not usuario_nombre or not sala_nombre or not fecha or not hora_inicio or not hora_fin:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            usuario = next(u for u in self.user_service.get_all() if u["username"] == usuario_nombre)
            sala = next(s for s in self.sala_service.get_all() if s["nombre"] == sala_nombre)
        except StopIteration:
            messagebox.showerror("Error", "Usuario o sala no válidos.")
            return

        try:
            fecha_inicio = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M")
            fecha_fin = datetime.strptime(f"{fecha} {hora_fin}", "%Y-%m-%d %H:%M")
            if fecha_fin <= fecha_inicio:
                messagebox.showerror("Error", "La hora de fin debe ser posterior a la de inicio.")
                return
        except Exception:
            messagebox.showerror("Error", "Formato de fecha u hora incorrecto.")
            return

        try:
            # Usar el builder para construir la reserva (ahora retorna dict)
            builder = ReservaBuilder()
            reserva_dict = builder \
                .set_usuario(usuario["id"]) \
                .set_sala(sala["id"]) \
                .set_fecha_inicio(fecha_inicio) \
                .set_fecha_fin(fecha_fin) \
                .build()
            # Serializar fechas a string ISO antes de enviar
            reserva_dict["fecha_inicio"] = reserva_dict["fecha_inicio"].isoformat()
            reserva_dict["fecha_fin"] = reserva_dict["fecha_fin"].isoformat()
            command = CreateReservaCommand(self.reserva_service, reserva_dict)
            command.execute()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la reserva:\n{e}")
            return

        messagebox.showinfo("Éxito", "Reserva creada correctamente.")
        if self.on_success:
            self.on_success()
        self.destroy()

def es_fecha_valida(fecha_str):
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def es_hora_valida(hora_str):
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    # Aquí deberías pasar instancias reales de los servicios
    app = ReservaApp(
        reserva_service=None,
        sala_service=None,
        user_service=None,
        mediator=None
    )
    app.mainloop()