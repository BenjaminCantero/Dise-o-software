import tkinter as tk
from tkinter import ttk

def crear_tarjeta_resumen(contenedor, titulo, valor, color):
    card = tk.Frame(contenedor, bg="white", bd=1, relief="solid",
                   highlightbackground="#dee2e6", highlightthickness=1)
    
    tk.Label(card, text=titulo, font=("Segoe UI", 11), bg="white").pack(pady=(15, 5), padx=10, anchor="w")
    tk.Label(card, text=valor, font=("Segoe UI", 24, "bold"), fg=color,
            bg="white").pack(pady=(0, 15), padx=10, anchor="w")
    
    return card

def crear_boton_accion(contenedor, texto, comando, color):
    btn = tk.Button(contenedor, text=texto, font=("Segoe UI", 10, "bold"),
                   bg=color, fg="white", activebackground=color,
                   relief="solid", padx=20, pady=10, command=comando)
    return btn

def crear_tabla(contenedor, columnas, altura=8):
    tree = ttk.Treeview(contenedor, columns=columnas, show="headings", height=altura)
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    
    return tree