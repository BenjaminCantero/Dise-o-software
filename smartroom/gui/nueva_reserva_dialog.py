import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from adapters.reserva_dialog_adapter import ReservaDialogAdapter
from builders.reserva_builder import ReservaBuilder
from commands.cancel_reserva_command import CreateReservaCommand  # Importa el comando

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
        # Obtén las listas de nombres de salas y usuarios
        salas = [s["nombre"] for s in self.mediator.sala_service.listar_salas()]
        usuarios = [u["nombre"] for u in self.mediator.user_service.listar_usuarios()]
        NuevaReservaDialog(self, self.reserva_service, salas, usuarios, on_save=self.cargar_reservas, mediator=self.mediator)

    def cargar_reservas(self):
        # Implementa la carga de reservas en la tabla
        pass

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
    def __init__(self, parent, reserva_service, salas, usuarios, on_save=None, mediator=None):
        super().__init__(parent)
        self.title("Nueva Reserva")
        self.geometry("400x350")
        self.reserva_service = reserva_service
        self.on_save = on_save
        self.mediator = mediator  # --- PATRÓN MEDIATOR: Guardar referencia ---
        self.configure(bg="#232946")

        # --- PATRÓN MEDIATOR: Registrar el diálogo ---
        if self.mediator:
            self.mediator.register("nueva_reserva_dialog", self)

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=300)

        # Sala
        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.sala_var = tk.StringVar()
        self.sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=salas, state="readonly", width=28)
        self.sala_combo.pack(ipady=3)

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar()
        self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=usuarios, state="readonly", width=28)
        self.usuario_combo.pack(ipady=3)

        # Fecha
        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.fecha_entry.pack(ipady=3)

        # Hora
        tk.Label(frame, text="Hora (HH:MM):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.hora_entry.pack(ipady=3)

        # Botones
        style = ttk.Style()
        style.configure("ReservaForm.TButton", font=("Arial", 11, "bold"), background="#eebbc3", foreground="#232946", padding=6)
        style.map("ReservaForm.TButton",
                  background=[("active", "#eebbc3")],
                  foreground=[("active", "#232946")])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", style="ReservaForm.TButton", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", style="ReservaForm.TButton", command=self.destroy).pack(side="left", padx=8)

        self.fecha_entry.focus_set()

    # --- PATRÓN MEDIATOR: Método para recibir eventos ---
    def on_event(self, sender, event, data):
        if event in ("reserva_creada", "reserva_eliminada", "reserva_editada"):
            # Aquí podrías actualizar campos o cerrar el diálogo si lo deseas
            pass

    def destroy(self):
        # --- PATRÓN MEDIATOR: Desregistrar el diálogo ---
        if self.mediator:
            self.mediator.unregister("nueva_reserva_dialog")
        super().destroy()

    def guardar(self):
        adapter = ReservaDialogAdapter(self)
        data = adapter.get_data()

        # Validaciones básicas
        if not data["sala"] or not data["usuario"] or not data["fecha"] or not data["hora"]:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            reserva_data = {
                "sala_nombre": data["sala"],
                "usuario_username": data["usuario"],
                "fecha_inicio": datetime.strptime(f"{data['fecha']} {data['hora']}", "%Y-%m-%d %H:%M"),
                "fecha_fin": datetime.strptime(f"{data['fecha']} {data['hora']}", "%Y-%m-%d %H:%M").replace(hour=(datetime.strptime(data['hora'], "%H:%M").hour + 1) % 24)
            }
            command = CreateReservaCommand(self.reserva_service, reserva_data)
            command.execute()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Reserva creada correctamente.")
        if self.on_save:
            self.on_save()
        # --- PATRÓN MEDIATOR: Notificar evento ---
        if self.mediator:
            self.mediator.notify(self, "reserva_creada", data)
        self.destroy()

        self.sala_var.set("")
        self.usuario_var.set("")
        self.fecha_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)

    @property
    def sala_input(self):
        return self.sala_combo

    @property
    def usuario_input(self):
        return self.usuario_combo

    @property
    def fecha_input(self):
        return self.fecha_entry

    @property
    def hora_input(self):
        return self.hora_entry

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