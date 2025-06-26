import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from adapters.reserva_dialog_adapter import ReservaDialogAdapter
from commands.cancel_reserva_command import EditReservaCommand    
from builders.reserva_builder import ReservaBuilder

class EditarReservaDialog(tk.Toplevel):
    def __init__(self, parent, reserva, reserva_service, sala_service, user_service, on_save=None):
        super().__init__(parent)
        self.title("Editar Reserva")
        self.geometry("370x350")
        self.reserva = reserva
        self.reserva_service = reserva_service
        self.sala_service = sala_service
        self.user_service = user_service
        self.on_save = on_save

        # Obtener usuarios y salas desde la API
        try:
            self.usuarios = [u["username"] for u in self.user_service.get_all()]
            self.salas = [s["nombre"] for s in self.sala_service.get_all()]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar usuarios o salas: {str(e)}")
            self.destroy()
            return

        self.configure(bg="#232946")

        frame = tk.Frame(self, bg="#f4f4f8", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=300)

        tk.Label(frame, text="Sala:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(18, 0))
        self.sala_var = tk.StringVar(value=reserva["sala"])
        self.sala_combo = ttk.Combobox(frame, textvariable=self.sala_var, values=self.salas, state="readonly", width=28)
        self.sala_combo.pack(ipady=3)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.usuario_var = tk.StringVar(value=reserva["usuario"])
        self.usuario_combo = ttk.Combobox(frame, textvariable=self.usuario_var, values=self.usuarios, state="readonly", width=28)
        self.usuario_combo.pack(ipady=3)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.fecha_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.fecha_entry.pack(ipady=3)
        self.fecha_entry.insert(0, reserva["fecha"])

        tk.Label(frame, text="Hora:", font=("Arial", 12), bg="#f4f4f8", fg="#232946").pack(pady=(10, 0))
        self.hora_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.hora_entry.pack(ipady=3)
        self.hora_entry.insert(0, reserva["hora"])

        btn_frame = tk.Frame(frame, bg="#f4f4f8")
        btn_frame.pack(pady=18)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda event: self.guardar())
        self.fecha_entry.focus_set()

    def guardar(self):
        adapter = ReservaDialogAdapter(self)
        data = adapter.get_data()

        # Validaciones
        self.sala_combo.configure(background="white")
        self.usuario_combo.configure(background="white")
        self.fecha_entry.configure(background="white")
        self.hora_entry.configure(background="white")

        error = False
        if not data["sala"]:
            self.sala_combo.configure(background="#ffcccc")
            error = True
        if not data["usuario"]:
            self.usuario_combo.configure(background="#ffcccc")
            error = True

        if not data["fecha"] or not es_fecha_valida(data["fecha"]):
            self.fecha_entry.configure(background="#ffcccc")
            messagebox.showerror("Error", "La fecha debe tener el formato YYYY-MM-DD")
            return

        if not data["hora"] or not es_hora_valida(data["hora"]):
            self.hora_entry.configure(background="#ffcccc")
            messagebox.showerror("Error", "La hora debe tener el formato HH:MM (24h)")
            return

        if error:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            fecha_inicio = datetime.strptime(f"{data['fecha']} {data['hora']}", "%Y-%m-%d %H:%M")
            fecha_fin = fecha_inicio.replace(hour=(fecha_inicio.hour + 1) % 24)
            # Busca los IDs correspondientes
            usuarios = self.user_service.get_all()
            salas = self.sala_service.get_all()
            usuario_id = next((u["id"] for u in usuarios if u["username"] == data["usuario"]), None)
            sala_id = next((s["id"] for s in salas if s["nombre"] == data["sala"]), None)
            if usuario_id is None or sala_id is None:
                messagebox.showerror("Error", "No se encontró el usuario o la sala seleccionada.")
                return
            # Llama al método update del servicio
            self.reserva_service.update(
                self.reserva["id"],
                usuario_id=usuario_id,
                sala_id=sala_id,
                fecha_inicio=fecha_inicio.isoformat(),
                fecha_fin=fecha_fin.isoformat()
            )
        except Exception as e:
            messagebox.showerror("Conflicto", str(e))
            return

        messagebox.showinfo("Éxito", "Reserva editada correctamente")
        if self.on_save:
            self.on_save(data["sala"], data["usuario"], data["fecha"], data["hora"])
        self.destroy()

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