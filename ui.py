import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers import get_rooms, add_room

class RoomManagementApp(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_header()
        self.create_room_list()
        self.create_form_section()
        self.create_statistics_section()
        self.create_user_management_section()
        self.load_rooms()

    def create_header(self):
        ttk.Label(self, text="Gestión de Salas", font=("Arial", 18, "bold")).pack(pady=10)

    def create_room_list(self):
        frame = ttk.LabelFrame(self, text="Lista de Salas")
        frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Nombre", "Capacidad", "Tipo")
        self.room_list = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.room_list.heading(col, text=col)
            self.room_list.column(col, width=100, anchor=CENTER)
        
        self.room_list.pack(fill="both", expand=True, padx=5, pady=5)

    def create_form_section(self):
        frame = ttk.LabelFrame(self, text="Añadir Nueva Sala")
        frame.pack(fill="x", pady=10)

        form_fields = ["Nombre", "Capacidad", "Tipo"]
        self.entries = {}

        for i, field in enumerate(form_fields):
            ttk.Label(frame, text=f"{field}:").grid(row=i, column=0, padx=5, pady=2, sticky=W)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=EW)
            self.entries[field.lower()] = entry
        
        frame.columnconfigure(1, weight=1)
        ttk.Button(frame, text="Añadir Sala", bootstyle="success", command=self.add_room).grid(row=len(form_fields), columnspan=2, pady=10)

    def create_statistics_section(self):
        frame = ttk.LabelFrame(self, text="Estadísticas de Ocupación")
        frame.pack(fill="both", expand=True, pady=10)
        
        self.stats_labels = {
            "total": ttk.Label(frame, text="Total de Salas: 0", font=("Arial", 12)),
            "ocupadas": ttk.Label(frame, text="Salas Ocupadas: 0", font=("Arial", 12)),
            "disponibilidad": ttk.Label(frame, text="Disponibilidad Promedio: 0%", font=("Arial", 12))
        }
        
        for label in self.stats_labels.values():
            label.pack(pady=2)

    def create_user_management_section(self):
        frame = ttk.LabelFrame(self, text="Gestión de Usuarios")
        frame.pack(fill="both", expand=True, pady=10)
        ttk.Label(frame, text="Roles y permisos en desarrollo", font=("Arial", 12)).pack(pady=5)

    def load_rooms(self):
        self.room_list.delete(*self.room_list.get_children())
        for room in get_rooms():
            self.room_list.insert("", "end", values=room)

    def add_room(self):
        name = self.entries["nombre"].get()
        capacity = self.entries["capacidad"].get()
        type_ = self.entries["tipo"].get()

        if name and capacity.isdigit() and type_:
            add_room(name, int(capacity), type_)
            self.load_rooms()
