import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
from datetime import datetime

class RoomManagementApp(ttk.Frame):
    def __init__(self, root):
        super().__init__(root, padding=15)
        self.pack(fill="both", expand=True)
        
        # Configurar colores y estilos
        self.style = ttk.Style()
        self.style.configure("TLabelframe", borderwidth=2)
        self.style.configure("Custom.TButton", font=("Segoe UI", 10, "bold"))
        
        # Crear componentes principales
        self.create_header()
        
        # Crear paneles principales
        main_panel = ttk.PanedWindow(self, orient="horizontal")
        main_panel.pack(fill="both", expand=True, pady=10)
        
        # Panel izquierdo: Lista de salas y reservas
        left_panel = ttk.Frame(main_panel)
        self.create_room_list(left_panel)
        self.create_reservation_list(left_panel)
        main_panel.add(left_panel, weight=2)
        
        # Panel derecho: Formulario de reserva y gestión de usuarios
        right_panel = ttk.Frame(main_panel)
        self.create_reservation_form(right_panel)
        self.create_user_management_section(right_panel)
        main_panel.add(right_panel, weight=1)
        
        # Cargar datos iniciales
        self.load_rooms()
        
        # Añadir barra de estado
        self.status_var = ttk.StringVar(value="Sistema listo")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=5)
        status_bar.pack(side="bottom", fill="x")

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Intentar cargar logo si existe
        try:
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo = logo.resize((40, 40))
                logo_img = ImageTk.PhotoImage(logo)
                logo_label = ttk.Label(header_frame, image=logo_img)
                logo_label.image = logo_img  # Mantener referencia
                logo_label.pack(side="left", padx=(0, 10))
        except:
            pass  # Si no hay logo, continuar sin él
            
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side="left")
        
        ttk.Label(title_frame, text="Sistema de Gestión de Salas", 
                 font=("Segoe UI", 20, "bold"), 
                 bootstyle="primary").pack(anchor="w")
        ttk.Label(title_frame, text="Control y administración de espacios", 
                 font=("Segoe UI", 12)).pack(anchor="w")
        
        # Añadir botones de acción rápida
        actions_frame = ttk.Frame(header_frame)
        actions_frame.pack(side="right")
        
        ttk.Button(actions_frame, text="Actualizar", 
                  bootstyle="info-outline", 
                  command=self.load_rooms).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Configuración", 
                  bootstyle="secondary-outline").pack(side="left", padx=5)

    def create_room_list(self, parent):
        list_frame = ttk.LabelFrame(parent, text="Salas Disponibles", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Barra de búsqueda
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=(0, 5))
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(search_frame, text="🔍", width=3).pack(side="left", padx=(5, 0))
        
        # Filtros de sala
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtro:").pack(side="left", padx=(0, 5))
        filter_combobox = ttk.Combobox(filter_frame, values=["Todas las salas", "Disponibles", "Ocupadas"])
        filter_combobox.current(0)
        filter_combobox.pack(side="left", fill="x", expand=True)
        
        # Lista de salas con scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        columns = ("ID", "Nombre", "Capacidad", "Tipo", "Estado")
        self.room_list = ttk.Treeview(list_container, columns=columns, show="headings", bootstyle="primary")
        
        # Configurar columnas con anchos proporcionales
        self.room_list.heading("ID", text="#", anchor=CENTER)
        self.room_list.heading("Nombre", text="Nombre de Sala", anchor=W)
        self.room_list.heading("Capacidad", text="Capacidad", anchor=CENTER)
        self.room_list.heading("Tipo", text="Tipo", anchor=CENTER)
        self.room_list.heading("Estado", text="Estado", anchor=CENTER)
        
        self.room_list.column("ID", width=50, anchor=CENTER, stretch=False)
        self.room_list.column("Nombre", width=200, anchor=W, stretch=True)
        self.room_list.column("Capacidad", width=100, anchor=CENTER, stretch=False)
        self.room_list.column("Tipo", width=120, anchor=CENTER, stretch=False)
        self.room_list.column("Estado", width=100, anchor=CENTER, stretch=False)
        
        # Añadir scrollbars
        y_scrollbar = ttk.Scrollbar(list_container, orient=VERTICAL, command=self.room_list.yview)
        x_scrollbar = ttk.Scrollbar(list_container, orient=HORIZONTAL, command=self.room_list.xview)
        self.room_list.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Colocar elementos
        self.room_list.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

    def create_reservation_list(self, parent):
        reservation_frame = ttk.LabelFrame(parent, text="Reservas Activas", padding=10)
        reservation_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Lista de reservas con scrollbar
        reservation_container = ttk.Frame(reservation_frame)
        reservation_container.pack(fill="both", expand=True)
        
        columns = ("ID", "Sala", "Usuario", "Fecha Reserva", "Estado")
        self.reservation_list = ttk.Treeview(reservation_container, columns=columns, show="headings", bootstyle="primary")
        
        # Configurar columnas con anchos proporcionales
        self.reservation_list.heading("ID", text="#", anchor=CENTER)
        self.reservation_list.heading("Sala", text="Sala", anchor=W)
        self.reservation_list.heading("Usuario", text="Usuario", anchor=W)
        self.reservation_list.heading("Fecha Reserva", text="Fecha Reserva", anchor=CENTER)
        self.reservation_list.heading("Estado", text="Estado", anchor=CENTER)
        
        self.reservation_list.column("ID", width=50, anchor=CENTER, stretch=False)
        self.reservation_list.column("Sala", width=150, anchor=W, stretch=True)
        self.reservation_list.column("Usuario", width=150, anchor=W, stretch=True)
        self.reservation_list.column("Fecha Reserva", width=150, anchor=CENTER, stretch=False)
        self.reservation_list.column("Estado", width=100, anchor=CENTER, stretch=False)
        
        # Añadir scrollbars
        y_scrollbar = ttk.Scrollbar(reservation_container, orient=VERTICAL, command=self.reservation_list.yview)
        x_scrollbar = ttk.Scrollbar(reservation_container, orient=HORIZONTAL, command=self.reservation_list.xview)
        self.reservation_list.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Colocar elementos
        self.reservation_list.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        reservation_container.columnconfigure(0, weight=1)
        reservation_container.rowconfigure(0, weight=1)

    def create_reservation_form(self, parent):
        form_frame = ttk.LabelFrame(parent, text="Formulario de Reserva", padding=10)
        form_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Campos del formulario de reserva
        self.reservation_entries = {}
        form_fields = [
            {"name": "usuario", "label": "Usuario:", "type": "entry"},
            {"name": "fecha", "label": "Fecha de Reserva:", "type": "entry"},
            {"name": "sala", "label": "Sala:", "type": "combobox", "values": ["Sala A", "Sala B", "Sala C"]},
        ]
        
        for i, field in enumerate(form_fields):
            ttk.Label(form_frame, text=field["label"]).grid(row=i, column=0, padx=5, pady=8, sticky=W)
            
            if field["type"] == "entry":
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=8, sticky=EW)
                self.reservation_entries[field["name"]] = entry
            elif field["type"] == "combobox":
                combo = ttk.Combobox(form_frame, values=field["values"])
                combo.grid(row=i, column=1, padx=5, pady=8, sticky=EW)
                self.reservation_entries[field["name"]] = combo
        
        # Botones de acción para reserva
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(form_fields), column=0, columnspan=2, pady=10, sticky=EW)
        
        ttk.Button(button_frame, text="Limpiar", bootstyle="secondary-outline").pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Reservar", 
                  bootstyle="success", 
                  style="Custom.TButton",
                  command=self.make_reservation).pack(side="right")
        
        form_frame.columnconfigure(1, weight=1)

    def create_user_management_section(self, parent):
        user_frame = ttk.LabelFrame(parent, text="Gestión de Usuarios", padding=10)
        user_frame.pack(fill="both", expand=True)
        
        # Crear contenedor de usuarios
        user_container = ttk.Frame(user_frame)
        user_container.pack(fill="both", expand=True, pady=10)
        
        # Botón para solicitar acceso
        ttk.Button(user_container, text="Solicitar Acceso", bootstyle="primary-outline").pack(side="left", padx=5)

    def load_rooms(self):
        # Simulación de la carga de salas
        print("Cargando salas...")

    def make_reservation(self):
        # Simulación para hacer una reserva
        usuario = self.reservation_entries["usuario"].get()
        fecha = self.reservation_entries["fecha"].get()
        sala = self.reservation_entries["sala"].get()
        print(f"Reservando: {usuario} para {sala} el {fecha}")
        self.status_var.set("Reserva realizada exitosamente")

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = RoomManagementApp(root)
    root.mainloop()
