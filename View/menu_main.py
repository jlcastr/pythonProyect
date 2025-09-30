import tkinter as tk
import sqlite3
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_setup import crear_conexion_y_tablas

def crear_menu_principal():
    """Crear ventana del menú principal con diseño profesional"""
    root = tk.Tk()
    root.title('S&M - Sistema de Manejo de Ventas')
    root.state('zoomed')
    root.resizable(True, True)
    root.configure(bg='#ecf0f1')
    
    # Intentar aplicar el icono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Título principal con estilo mejorado
    titulo = tk.Label(root, text="S&M - Sistema de Manejo de Ventas", 
                     font=("Arial", 28, "bold"), 
                     fg="#2c3e50", bg="#ecf0f1",
                     pady=30)
    titulo.pack()
    
    # Crear frame contenedor con recuadro negro
    frame_contenedor = tk.Frame(root, bg="#ecf0f1", pady=20)
    frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
    
    # Frame con borde negro (recuadro)
    frame_recuadro = tk.Frame(frame_contenedor, bg="#2c3e50", bd=1, relief="solid")
    frame_recuadro.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Frame interior con fondo claro
    frame_interior = tk.Frame(frame_recuadro, bg="#ffffff", bd=0)
    frame_interior.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Frame principal para los botones (dentro del recuadro)
    frame_botones = tk.Frame(frame_interior, bg="#ffffff")
    frame_botones.pack(expand=True, pady=40)
    
    # Funciones para efectos hover
    def on_enter(event, button, color):
        """Efecto al pasar el mouse sobre el botón"""
        button.configure(bg=color, relief="raised", bd=4)
    
    def on_leave(event, button, original_color):
        """Efecto al quitar el mouse del botón"""
        button.configure(bg=original_color, relief="raised", bd=3)
    
    def abrir_ventas():
        """Abrir el módulo de ventas"""
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        conn = sqlite3.connect("config/sqliteDB.db")
        cursor = conn.cursor()
        
        frame_ventas = tk.Frame(root)
        frame_ventas.pack(fill="both", expand=True)
        
        from View.Sales import crear_interfaz_ventas_en_frame
        crear_interfaz_ventas_en_frame(frame_ventas, conn, cursor, lambda: volver_al_menu(frame_ventas, conn))
    
    def volver_al_menu(frame_actual, conn):
        """Volver al menú principal"""
        conn.close()
        frame_actual.destroy()
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
    
    def abrir_reportes():
        """Abrir el módulo de reportes"""
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        frame_reportes = tk.Frame(root)
        frame_reportes.pack(fill="both", expand=True)
        
        from View.Report_menu import crear_menu_reportes
        crear_menu_reportes(frame_reportes, lambda: volver_al_menu_desde_reportes(frame_reportes))
    
    def volver_al_menu_desde_reportes(frame_actual):
        """Volver al menú principal desde reportes"""
        frame_actual.destroy()
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
    
    def abrir_configuraciones():
        """Abrir el módulo de configuraciones"""
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        frame_configuraciones = tk.Frame(root)
        frame_configuraciones.pack(fill="both", expand=True)
        
        from View.menu_settings_view import mostrar_configuraciones_en_frame
        mostrar_configuraciones_en_frame(frame_configuraciones, lambda: volver_al_menu_desde_configuraciones(frame_configuraciones))
    
    def volver_al_menu_desde_configuraciones(frame_actual):
        """Volver al menú principal desde configuraciones"""
        frame_actual.destroy()
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
    
    # Cargar imágenes para los botones
    try:
        img_ventas = tk.PhotoImage(file="Img/pago-en-efectivo.png")
        img_ventas = img_ventas.subsample(3, 3)
    except Exception:
        img_ventas = None
    
    try:
        img_reportes = tk.PhotoImage(file="Img/grafico.png")
        img_reportes = img_reportes.subsample(3, 3)
    except Exception:
        img_reportes = None
    
    try:
        img_configuraciones = tk.PhotoImage(file="Img/configuraciones.png")
        img_configuraciones = img_configuraciones.subsample(3, 3)
    except Exception:
        img_configuraciones = None
    
    try:
        img_salir = tk.PhotoImage(file="Img/cancelar.png")
        img_salir = img_salir.subsample(3, 3)
    except Exception:
        img_salir = None
    
    # Crear botones con estilo profesional
    # Botón VENTAS
    if img_ventas:
        btn_ventas = tk.Button(frame_botones, text="VENTAS", 
                              image=img_ventas, compound=tk.TOP,
                              command=abrir_ventas, 
                              font=("Arial", 18, "bold"),
                              width=200, height=200,
                              bg="#3498db", fg="white", 
                              relief="raised", bd=3,
                              padx=15, pady=20,
                              cursor="hand2")
    else:
        btn_ventas = tk.Button(frame_botones, text="💰 VENTAS", 
                              command=abrir_ventas,
                              font=("Arial", 16, "bold"),
                              width=22, height=12,
                              bg="#3498db", fg="white", 
                              relief="raised", bd=3,
                              padx=15, pady=15,
                              cursor="hand2")
    
    btn_ventas.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
    btn_ventas.bind("<Enter>", lambda e: on_enter(e, btn_ventas, "#2980b9"))
    btn_ventas.bind("<Leave>", lambda e: on_leave(e, btn_ventas, "#3498db"))
    
    if img_ventas:
        btn_ventas.image = img_ventas
    
    # Botón REPORTES
    if img_reportes:
        btn_reportes = tk.Button(frame_botones, text="REPORTES", 
                                image=img_reportes, compound=tk.TOP,
                                command=abrir_reportes, 
                                font=("Arial", 18, "bold"),
                                width=200, height=200,
                                bg="#e74c3c", fg="white", 
                                relief="raised", bd=3,
                                padx=15, pady=20,
                                cursor="hand2")
    else:
        btn_reportes = tk.Button(frame_botones, text="📊 REPORTES", 
                                command=abrir_reportes,
                                font=("Arial", 16, "bold"),
                                width=22, height=12,
                                bg="#e74c3c", fg="white", 
                                relief="raised", bd=3,
                                padx=15, pady=15,
                                cursor="hand2")
    
    btn_reportes.grid(row=0, column=1, padx=40, pady=30, sticky="nsew")
    btn_reportes.bind("<Enter>", lambda e: on_enter(e, btn_reportes, "#c0392b"))
    btn_reportes.bind("<Leave>", lambda e: on_leave(e, btn_reportes, "#e74c3c"))
    
    if img_reportes:
        btn_reportes.image = img_reportes
    
    # Botón AJUSTES
    if img_configuraciones:
        btn_configuraciones = tk.Button(frame_botones, text="AJUSTES", 
                                       image=img_configuraciones, compound=tk.TOP,
                                       command=abrir_configuraciones,
                                       font=("Arial", 18, "bold"),
                                       width=200, height=200,
                                       bg="#f39c12", fg="white", 
                                       relief="raised", bd=3,
                                       padx=15, pady=20,
                                       cursor="hand2")
    else:
        btn_configuraciones = tk.Button(frame_botones, text="⚙️ AJUSTES", 
                                       command=abrir_configuraciones,
                                       font=("Arial", 16, "bold"),
                                       width=22, height=12,
                                       bg="#f39c12", fg="white", 
                                       relief="raised", bd=3,
                                       padx=15, pady=15,
                                       cursor="hand2")
    
    btn_configuraciones.grid(row=1, column=0, padx=40, pady=30, sticky="nsew")
    btn_configuraciones.bind("<Enter>", lambda e: on_enter(e, btn_configuraciones, "#e67e22"))
    btn_configuraciones.bind("<Leave>", lambda e: on_leave(e, btn_configuraciones, "#f39c12"))
    
    if img_configuraciones:
        btn_configuraciones.image = img_configuraciones
    
    # Botón SALIR
    if img_salir:
        btn_salir = tk.Button(frame_botones, text="SALIR", 
                             image=img_salir, compound=tk.TOP,
                             command=root.quit,
                             font=("Arial", 18, "bold"),
                             width=200, height=200,
                             bg="#95a5a6", fg="white", 
                             relief="raised", bd=3,
                             padx=15, pady=20,
                             cursor="hand2")
    else:
        btn_salir = tk.Button(frame_botones, text="🚪 SALIR", 
                             command=root.quit,
                             font=("Arial", 16, "bold"),
                             width=22, height=12,
                             bg="#95a5a6", fg="white", 
                             relief="raised", bd=3,
                             padx=15, pady=15,
                             cursor="hand2")
    
    btn_salir.grid(row=1, column=1, padx=40, pady=30, sticky="nsew")
    btn_salir.bind("<Enter>", lambda e: on_enter(e, btn_salir, "#7f8c8d"))
    btn_salir.bind("<Leave>", lambda e: on_leave(e, btn_salir, "#95a5a6"))
    
    if img_salir:
        btn_salir.image = img_salir
    
    # Configurar el grid para distribución uniforme
    frame_botones.grid_columnconfigure(0, weight=1)
    frame_botones.grid_columnconfigure(1, weight=1)
    frame_botones.grid_rowconfigure(0, weight=1)
    frame_botones.grid_rowconfigure(1, weight=1)
    
    # Pie de página profesional
    pie_pagina = tk.Label(root, text="© 2025 S&M - Sistema de Gestión Empresarial | Versión 1.0", 
                         font=("Arial", 11), 
                         fg="#7f8c8d", bg="#ecf0f1")
    pie_pagina.pack(side="bottom", pady=15)
    
    root.mainloop()

if __name__ == '__main__':
    crear_conexion_y_tablas('config/sqliteDB.db')
    crear_menu_principal()
