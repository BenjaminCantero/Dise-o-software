import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from adapters.reserva_dialog_adapter import ReservaDialogAdapter
from commands.cancel_reserva_command import EditReservaCommand
from builders.reserva_builder import ReservaBuilder

class EditarReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva, reserva_service, sala_service, user_service, on_save=None, current_user=None):
        super().__init__(parent)
        self.title("Editar Reserva")
        self.geometry("370x410")
        self.reserva = reserva
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.on_save = on_save
        self.current_user = current_user
        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)
        frame.pack_propagate(False)

        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(14, 0))
        self.sala_var = tk.StringVar(value=reserva["sala"])
        self.sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=[s["nombre"] for s in self.sala_service.get_all()], state="readonly", width=28)
        self.sala_combo.pack(ipady=3)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar(value=reserva["usuario"])
        if self.current_user and self.current_user.get("role") == "admin":
            usuarios = [u["username"] for u in self.user_service.get_all()]
            self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=usuarios, state="readonly", width=28)
        else:
            self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=[self.current_user["username"]], state="readonly", width=28)
            self.usuario_var.set(self.current_user["username"])
            self.usuario_combo.config(state="disabled")
        self.usuario_combo.pack(ipady=3)

        from tkcalendar import DateEntry
        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.fecha_entry = DateEntry(frame, width=28, font=("Arial", 11), background="#eebbc3", foreground="#232946", date_pattern="yyyy-mm-dd")
        self.fecha_entry.set_date(reserva["fecha"])
        self.fecha_entry.pack(ipady=3)

        horas = [f"{h:02d}:{m:02d}" for h in range(8, 21) for m in (0, 30)]
        tk.Label(frame, text="Hora de inicio:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_inicio_var = tk.StringVar(value=reserva.get("hora_inicio", reserva.get("hora", "")))
        self.hora_inicio_combo = ttk.Combobox(frame, textvariable=self.hora_inicio_var, values=horas, state="readonly", width=28)
        self.hora_inicio_combo.pack(ipady=3)

        tk.Label(frame, text="Hora de fin:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_fin_var = tk.StringVar(value=reserva.get("hora_fin", ""))
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
            command = EditReservaCommand(
                self.reserva_service,
                self.reserva["id"],
                {
                    "usuario_id": usuario["id"],
                    "sala_id": sala["id"],
                    "fecha_inicio": fecha_inicio.isoformat(),
                    "fecha_fin": fecha_fin.isoformat()
                }
            )
            command.execute()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la reserva:\n{e}")
            return

        messagebox.showinfo("Éxito", "Reserva editada correctamente.")
        if self.on_save:
            self.on_save()
        self.destroy()