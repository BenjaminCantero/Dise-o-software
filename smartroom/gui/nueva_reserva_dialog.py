import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from adapters.reserva_dialog_adapter import ReservaDialogAdapter
from builders.reserva_builder import ReservaBuilder
from commands.cancel_reserva_command import CreateReservaCommand  # Importa el comando
from smartroom.services import reserva_service, sala_service, user_service

class ReservaApp(tk.Tk):
    def __init__(self, reserva_service, mediator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reserva_service = reserva_service
        self.mediator = mediator
        self.title("Reservas")
        self.geometry("800x600")
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
        NuevaReservaDialog(self, on_success=self.cargar_reservas)

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

    def crear_reserva(self):
        usuario = self.obtener_usuario_seleccionado()  # objeto o id
        sala = self.obtener_sala_seleccionada()        # objeto o id
        fecha_inicio = self.obtener_fecha_inicio()
        fecha_fin = self.obtener_fecha_fin()

        builder = ReservaBuilder()
        reserva = (
            builder
            .set_usuario(usuario)
            .set_sala(sala)
            .set_fecha_inicio(fecha_inicio)
            .set_fecha_fin(fecha_fin)
            .build()
        )

        # Ahora puedes pasar la reserva al servicio o repositorio
        self.reserva_service.agregar_reserva(reserva)

class NuevaReservaDialog(tk.Toplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.on_success = on_success

        # Obtener usuarios y salas desde la API
        try:
            self.usuarios = user_service.get_usuarios()
            self.salas = sala_service.get_salas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar usuarios o salas:\n{e}")
            self.destroy()
            return

        self.usuario_var = tk.StringVar()
        self.sala_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.hora_inicio_var = tk.StringVar()
        self.hora_fin_var = tk.StringVar()

        ttk.Label(self, text="Usuario:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.usuario_combo = ttk.Combobox(self, textvariable=self.usuario_var, values=[u["username"] for u in self.usuarios])
        self.usuario_combo.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Sala:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.sala_combo = ttk.Combobox(self, textvariable=self.sala_var, values=[s["nombre"] for s in self.salas])
        self.sala_combo.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.fecha_entry = ttk.Entry(self, textvariable=self.fecha_var)
        self.fecha_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Hora inicio (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.hora_inicio_entry = ttk.Entry(self, textvariable=self.hora_inicio_var)
        self.hora_inicio_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self, text="Hora fin (HH:MM):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.hora_fin_entry = ttk.Entry(self, textvariable=self.hora_fin_var)
        self.hora_fin_entry.grid(row=4, column=1, padx=10, pady=5)

        guardar_btn = ttk.Button(self, text="Guardar", command=self.guardar)
        guardar_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def guardar(self):
        usuario_nombre = self.usuario_var.get()
        sala_nombre = self.sala_var.get()
        fecha = self.fecha_var.get()
        hora_inicio = self.hora_inicio_var.get()
        hora_fin = self.hora_fin_var.get()

        if not usuario_nombre or not sala_nombre or not fecha or not hora_inicio or not hora_fin:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            usuario = next(u for u in self.usuarios if u["username"] == usuario_nombre)
            sala = next(s for s in self.salas if s["nombre"] == sala_nombre)
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
            reserva_service.crear_reserva(
                usuario_id=usuario["id"],
                sala_id=sala["id"],
                fecha_inicio=fecha_inicio.isoformat(),
                fecha_fin=fecha_fin.isoformat()
            )
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
    app = ReservaApp(reserva_service=None, mediator=None)
    app.mainloop()