import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SistemaGestionSalas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Salas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        
        # Paleta de colores mejorada
        self.color_fondo = "#f8f9fa"
        self.color_sidebar = "#343a40"
        self.color_principal = "#007bff"
        self.color_secundario = "#0056b3"
        self.color_exito = "#28a745"
        self.color_advertencia = "#dc3545"
        self.color_texto = "#212529"
        self.color_borde = "#dee2e6"
        
        # Fuentes mejoradas
        self.titulo_font = ("Segoe UI", 18, "bold")
        self.subtitulo_font = ("Segoe UI", 14)
        self.normal_font = ("Segoe UI", 11)
        self.boton_font = ("Segoe UI", 10, "bold")
        
        # Configurar el estilo general
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configurar estilos personalizados
        self.style.configure("TFrame", background=self.color_fondo)
        self.style.configure("TLabel", background=self.color_fondo, 
                           foreground=self.color_texto, font=self.normal_font)
        self.style.configure("TButton", font=self.boton_font, 
                           borderwidth=1, relief="solid")
        self.style.map("TButton", 
                      foreground=[("active", "white")],
                      background=[("active", self.color_secundario)])
        
        # Contenedor principal
        self.main_frame = tk.Frame(root, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True)
        
        # ===== SIDEBAR MEJORADO =====
        self.sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo o título
        tk.Label(self.sidebar, 
                text="Gestión de Salas", 
                font=("Segoe UI", 16, "bold"), 
                bg=self.color_sidebar, 
                fg="white",
                pady=20).pack(fill="x")
        
        # Separador
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Opciones del menú
        menu_opciones = [
            ("Inicio", "home", self.mostrar_inicio),
            ("Reservar Sala", "calendar-plus", self.mostrar_reservas),
            ("Calendario", "calendar", self.mostrar_calendario),
            ("Salas", "door-open", self.mostrar_salas),
            ("Reportes", "file-text", self.mostrar_reportes),
            ("Configuración", "settings", self.mostrar_config)
        ]
        
        for texto, icono, comando in menu_opciones:
            btn = tk.Button(self.sidebar,
                          text=f"  {texto}",
                          font=self.normal_font,
                          bg=self.color_sidebar,
                          fg="white",
                          activebackground=self.color_secundario,
                          activeforeground="white",
                          anchor="w",
                          padx=15,
                          pady=12,
                          relief="flat",
                          command=comando)
            btn.pack(fill="x", padx=5)
        
        # Separador final
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Versión del sistema
        tk.Label(self.sidebar, 
                text="v2.0", 
                font=("Segoe UI", 8), 
                bg=self.color_sidebar, 
                fg="#adb5bd").pack(side="bottom", pady=10)
        
        # ===== CONTENIDO PRINCIPAL =====
        self.content_frame = tk.Frame(self.main_frame, bg=self.color_fondo, padx=30, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Mostrar panel de inicio por defecto
        self.mostrar_inicio()
    
    def mostrar_inicio(self):
        self.limpiar_contenido()
        
        # Título principal
        tk.Label(self.content_frame, 
                text="Panel Principal", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Tarjetas resumen
        resumen_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        resumen_frame.pack(fill="x", pady=(0, 30))
        
        resumen_data = [
            {"title": "Salas Disponibles", "value": "24", "color": self.color_principal},
            {"title": "Reservas Hoy", "value": "18", "color": self.color_exito},
            {"title": "En Mantenimiento", "value": "3", "color": self.color_advertencia},
            {"title": "Ocupación Total", "value": "78%", "color": "#6c757d"}
        ]
        
        for i, data in enumerate(resumen_data):
            card = tk.Frame(resumen_frame, bg="white", bd=1, relief="solid", 
                          highlightbackground=self.color_borde, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=5)
            
            tk.Label(card, 
                    text=data["title"], 
                    font=self.normal_font, 
                    bg="white").pack(pady=(15, 5), padx=10, anchor="w")
            
            tk.Label(card, 
                    text=data["value"], 
                    font=("Segoe UI", 24, "bold"), 
                    fg=data["color"], 
                    bg="white").pack(pady=(0, 15), padx=10, anchor="w")
        
        # Sección de acciones rápidas
        tk.Label(self.content_frame, 
                text="Acciones Rápidas", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))
        
        acciones_frame = tk.Frame(self.content_frame, bg=self.color_fondo)
        acciones_frame.pack(fill="x", pady=(0, 30))
        
        acciones = [
            {"text": "Nueva Reserva", "command": self.mostrar_reservas, "color": self.color_principal},
            {"text": "Ver Calendario", "command": self.mostrar_calendario, "color": "#17a2b8"},
            {"text": "Reportar Problema", "command": self.reportar_problema, "color": self.color_advertencia}
        ]
        
        for accion in acciones:
            btn = tk.Button(acciones_frame,
                          text=accion["text"],
                          font=self.boton_font,
                          bg=accion["color"],
                          fg="white",
                          activebackground=accion["color"],
                          relief="solid",
                          padx=20,
                          pady=10,
                          command=accion["command"])
            btn.pack(side="left", padx=10)
        
        # Sección de últimas reservas
        tk.Label(self.content_frame, 
                text="Últimas Reservas", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(10, 15))
        
        # Tabla de reservas recientes
        columns = ("Sala", "Responsable", "Fecha", "Hora", "Estado")
        self.tree_reservas = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=120, anchor="center")
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scrollbar.set)
        self.tree_reservas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Datos de ejemplo
        reservas = [
            ("A101", "Juan Pérez", "15/06/2023", "08:00-10:00", "Confirmada"),
            ("B205", "María Gómez", "15/06/2023", "10:00-12:00", "Pendiente"),
            ("C302", "Carlos Ruiz", "16/06/2023", "14:00-16:00", "Confirmada")
        ]
        
        for reserva in reservas:
            self.tree_reservas.insert("", "end", values=reserva)
    
    def mostrar_reservas(self):
        self.limpiar_contenido()
        
        # Título
        tk.Label(self.content_frame, 
                text="Nueva Reserva de Sala", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Contenedor del formulario
        form_container = tk.Frame(self.content_frame, bg="white", padx=20, pady=20,
                                highlightbackground=self.color_borde, highlightthickness=1)
        form_container.pack(fill="both", expand=True)
        
        # Formulario en dos columnas
        left_frame = tk.Frame(form_container, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        right_frame = tk.Frame(form_container, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        # Campos del formulario
        campos = [
            {"label": "Responsable", "frame": left_frame},
            {"label": "Departamento/Facultad", "frame": left_frame},
            {"label": "Correo Electrónico", "frame": left_frame},
            {"label": "Teléfono de Contacto", "frame": left_frame},
            {"label": "Sala a Reservar", "frame": right_frame},
            {"label": "Fecha de Reserva", "frame": right_frame},
            {"label": "Hora Inicio", "frame": right_frame},
            {"label": "Hora Término", "frame": right_frame},
            {"label": "Motivo", "frame": right_frame}
        ]
        
        self.entries = {}
        for campo in campos:
            frame = tk.Frame(campo["frame"], bg="white", pady=8)
            frame.pack(fill="x")
            
            tk.Label(frame, 
                    text=campo["label"] + ":", 
                    font=self.normal_font, 
                    bg="white").pack(anchor="w", pady=(0, 5))
            
            if campo["label"] == "Sala a Reservar":
                entry = ttk.Combobox(frame, font=self.normal_font, values=["A101", "B205", "C302", "D404"])
            elif campo["label"] == "Fecha de Reserva":
                entry = ttk.Entry(frame, font=self.normal_font)
                # Aquí podríamos añadir un date picker
            elif campo["label"] == "Motivo":
                entry = tk.Text(frame, font=self.normal_font, height=4, width=30,
                              highlightbackground=self.color_borde, highlightthickness=1)
            else:
                entry = ttk.Entry(frame, font=self.normal_font)
            
            entry.pack(fill="x", pady=(0, 10))
            self.entries[campo["label"]] = entry
        
        # Botones del formulario
        btn_frame = tk.Frame(form_container, bg="white", pady=20)
        btn_frame.pack(fill="x", side="bottom")
        
        tk.Button(btn_frame,
                 text="Cancelar",
                 font=self.boton_font,
                 bg="#6c757d",
                 fg="white",
                 padx=20,
                 pady=8,
                 command=self.mostrar_inicio).pack(side="left", padx=10)
        
        tk.Button(btn_frame,
                 text="Reservar Sala",
                 font=self.boton_font,
                 bg=self.color_principal,
                 fg="white",
                 padx=20,
                 pady=8).pack(side="right", padx=10)
    
    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # Métodos placeholder para otras secciones
    def mostrar_calendario(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Calendario de Reservas", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación del calendario
        tk.Label(self.content_frame, 
                text="Calendario en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)
    
    def mostrar_salas(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Gestión de Salas", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación de la gestión de salas
        tk.Label(self.content_frame, 
                text="Módulo en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)
    
    def mostrar_reportes(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Reportes y Estadísticas", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación de reportes
        tk.Label(self.content_frame, 
                text="Módulo en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)
    
    def mostrar_config(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Configuración del Sistema", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación de configuración
        tk.Label(self.content_frame, 
                text="Módulo en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)
    
    def reportar_problema(self):
        self.limpiar_contenido()
        tk.Label(self.content_frame, 
                text="Reportar Problema", 
                font=self.titulo_font, 
                bg=self.color_fondo).pack(anchor="nw", pady=(0, 20))
        
        # Aquí iría la implementación de reporte de problemas
        tk.Label(self.content_frame, 
                text="Formulario en desarrollo", 
                font=self.subtitulo_font, 
                bg=self.color_fondo).pack(pady=100)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionSalas(root)
    root.mainloop()