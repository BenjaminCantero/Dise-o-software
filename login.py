# proyecto_gestion_salas/login.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from sistema_gestion import SistemaGestionSalas # Assuming sistema_gestion.py is in the same directory
from database_setup import get_db_connection, create_tables, insert_default_users
from utils import color_palette, font_styles

class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x400")
        self.root.configure(bg=color_palette["login_bg"])
        
        # Conexión a la base de datos y setup inicial
        # Each class instance will manage its own connection to the shared DB file
        self.conn = get_db_connection() 
        # Ensure tables and default users are created/verified at login startup
        create_tables(self.conn) 
        insert_default_users(self.conn)
        self.cursor = self.conn.cursor()
        
        # Marco principal
        frame = tk.Frame(self.root, bg=color_palette["login_frame_bg"], padx=20, pady=20, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        tk.Label(frame, text="Inicio de Sesión", font=font_styles["login_titulo"], 
                 bg=color_palette["login_frame_bg"], fg=color_palette["white"]).pack(pady=10)
        
        # Usuario
        tk.Label(frame, text="Usuario:", font=font_styles["login_label"], 
                 bg=color_palette["login_frame_bg"], fg=color_palette["white"]).pack(anchor="w", pady=(10, 5))
        self.entry_user = tk.Entry(frame, font=font_styles["login_entry"], relief="flat", 
                                   bg=color_palette["login_entry_bg"], fg=color_palette["login_entry_fg"])
        self.entry_user.pack(fill="x", pady=5)
        
        # Contraseña
        tk.Label(frame, text="Contraseña:", font=font_styles["login_label"], 
                 bg=color_palette["login_frame_bg"], fg=color_palette["white"]).pack(anchor="w", pady=(10, 5))
        self.entry_pass = tk.Entry(frame, font=font_styles["login_entry"], show="*", relief="flat", 
                                   bg=color_palette["login_entry_bg"], fg=color_palette["login_entry_fg"])
        self.entry_pass.pack(fill="x", pady=5)
        
        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar Sesión", font=font_styles["login_button"], 
                  bg=color_palette["principal"], fg=color_palette["white"], 
                  activebackground=color_palette["secundario"], activeforeground=color_palette["white"], 
                  relief="flat", command=self.validar_login).pack(pady=20, fill="x")
    
    def validar_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        self.cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        
        if result:
            role = result[0]
            messagebox.showinfo("Éxito", f"Bienvenido, {username} ({role})")
            self.root.destroy() 
            
            main_root = tk.Tk()
            app = SistemaGestionSalas(main_root, role)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()