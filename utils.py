import tkinter as tk
from tkinter import messagebox

def mostrar_mensaje(tipo, titulo, mensaje):
    if tipo == "info":
        messagebox.showinfo(titulo, mensaje)
    elif tipo == "warning":
        messagebox.showwarning(titulo, mensaje)
    elif tipo == "error":
        messagebox.showerror(titulo, mensaje)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def validar_entrada(entrada, tipo="texto"):
    if tipo == "texto":
        return bool(entrada.strip())
    elif tipo == "numero":
        return entrada.isdigit()
    elif tipo == "email":
        return "@" in entrada and "." in entrada
    return False

def formatear_fecha(fecha):
    return fecha.strftime("%d/%m/%Y")