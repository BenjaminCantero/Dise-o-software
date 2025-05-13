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