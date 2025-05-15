import tkinter as tk
from tkinter import ttk

class UIComponentes:
    def __init__(self):
        # Paleta de colores
        self.color_fondo = "#f8f9fa"
        self.color_sidebar = "#343a40"
        self.color_principal = "#007bff"
        self.color_secundario = "#0056b3"
        self.color_exito = "#28a745"
        self.color_advertencia = "#dc3545"
        self.color_texto = "#212529"
        self.color_borde = "#dee2e6"
        self.color_tarjeta = "#ffffff"

        # Fuentes
        self.titulo_font = ("Segoe UI", 18, "bold")
        self.subtitulo_font = ("Segoe UI", 14)
        self.normal_font = ("Segoe UI", 11)
        self.boton_font = ("Segoe UI", 10, "bold")

    def configurar_estilos(self, style):
        """Configura los estilos personalizados para la aplicación."""
        style.theme_use("clam")
        style.configure("TFrame", background=self.color_fondo)
        style.configure("TLabel", background=self.color_fondo,
                        foreground=self.color_texto, font=self.normal_font)
        style.configure("TButton", font=self.boton_font,
                        borderwidth=1, relief="solid")
        style.map("TButton",
                  foreground=[("active", "white")],
                  background=[("active", self.color_secundario)])

    def crear_label(self, parent, texto, fuente=None, color_fondo=None, color_texto=None):
        if fuente is None:
            fuente = self.normal_font
        if color_fondo is None:
            color_fondo = self.color_fondo
        if color_texto is None:
            color_texto = self.color_texto
        label = tk.Label(parent, text=texto, font=fuente, bg=color_fondo, fg=color_texto)
        return label

    def crear_boton(self, parent, texto, comando, ancho=20, color_fondo=None, color_texto="white"):
        if color_fondo is None:
            color_fondo = self.color_principal
        boton = tk.Button(parent,
                          text=texto,
                          font=self.boton_font,
                          bg=color_fondo,
                          fg=color_texto,
                          activebackground=self.color_secundario,
                          activeforeground="white",
                          relief="flat",
                          command=comando,
                          width=ancho)
        return boton

    def crear_frame(self, parent, color_fondo=None, padding=(0, 0)):
        if color_fondo is None:
            color_fondo = self.color_fondo
        frame = tk.Frame(parent, bg=color_fondo, padx=padding[0], pady=padding[1])
        return frame

    def crear_entry(self, parent, ancho=30):
        entry = ttk.Entry(parent, width=ancho)
        return entry