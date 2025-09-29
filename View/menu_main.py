import tkinter as tk
from tkinter import ttk
import sqlite3
from config.db_setup import crear_conexion_y_tablas

def crear_menu_principal():
    """Cr    if img_salir:
        btn_salir = tk.Button(frame_botones, text="SALIR", 
                             image=img_salir, compound=tk.TOP,a
                             command=root.quit,
                             font=("Arial", 16, "bold"),
                             width=140, height=150,
                             bg="#357ab8", fg="white", relief="raised",
                             bd=2, padx=5, pady=10,
                             anchor='center',
                             justify='center')
    else:
        btn_salir = tk.Button(frame_botones, text="🚺 SALIR", 
                             command=root.quit,
                             font=("Arial", 12, "bold"),
                             width=15, height=6,
                             bg="#357ab8", fg="white", relief="raised",
                             bd=2, padx=5, pady=5)
    btn_salir.grid(row=1, column=1, padx=20, pady=20)
    
    # Mantener referencia de la imagen de salir
    if img_salir:
        btn_salir.image = img_salirventana del menú principal con botones en cuadrícula"""
    root = tk.Tk()
    root.title("S&M - Sistema de Manejo de Ventas")
    
    # Configurar ventana en pantalla completa
    root.state('zoomed')  # Para Windows - maximiza la ventana
    # root.attributes('-fullscreen', True)  # Alternativa para pantalla completa real
    
    root.resizable(True, True)
    
    # Intentar aplicar el icono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Título principal
    titulo = tk.Label(root, text="S&M - Sistema de Manejo de Ventas", 
                     font=("Arial", 18, "bold"), pady=30)
    titulo.pack()
    
    # Frame principal para los botones
    frame_botones = tk.Frame(root)
    frame_botones.pack(expand=True)
    
    # Configurar estilo para los botones
    style = ttk.Style()
    style.configure("Menu.TButton", 
                   font=("Arial", 12, "bold"),
                   padding=(20, 15))
    
    def abrir_ventas():
        """Abrir el módulo de ventas en la misma ventana"""
        # Ocultar el menú principal
        titulo.pack_forget()
        frame_botones.pack_forget()
        
        # Crear conexión a la base de datos
        conn = sqlite3.connect("config/sqliteDB.db")
        cursor = conn.cursor()
        
        # Crear frame para ventas
        frame_ventas = tk.Frame(root)
        frame_ventas.pack(fill="both", expand=True)
        
        # Importar y crear la interfaz de ventas dentro del frame
        from View.Sales import crear_interfaz_ventas_en_frame
        crear_interfaz_ventas_en_frame(frame_ventas, conn, cursor, lambda: volver_al_menu(frame_ventas, conn))
    
    def volver_al_menu(frame_actual, conn):
        """Volver al menú principal"""
        conn.close()
        frame_actual.destroy()
        titulo.pack()
        frame_botones.pack(expand=True)
    
    def abrir_reportes():
        """Abrir el módulo de reportes en la misma ventana"""
        # Ocultar el menú principal
        titulo.pack_forget()
        frame_botones.pack_forget()
        
        # Crear frame para reportes
        frame_reportes = tk.Frame(root)
        frame_reportes.pack(fill="both", expand=True)
        
        # Importar y crear el menú de reportes dentro del frame
        from View.Report_menu import crear_menu_reportes
        crear_menu_reportes(frame_reportes, lambda: volver_al_menu_desde_reportes(frame_reportes))
    
    def volver_al_menu_desde_reportes(frame_actual):
        """Volver al menú principal desde reportes"""
        frame_actual.destroy()
        titulo.pack()
        frame_botones.pack(expand=True)
    
    def abrir_configuraciones():
        """Abrir el módulo de configuraciones"""
        from tkinter import messagebox
        messagebox.showinfo("Configuraciones", "Módulo de configuraciones en desarrollo")
    
    # Cargar imágenes para los botones
    try:
        img_ventas = tk.PhotoImage(file="Img/pago-en-efectivo.png")
        # Redimensionar imagen más pequeña para dar espacio al texto
        img_ventas = img_ventas.subsample(4, 4)  # Reducir aún más el tamaño
    except Exception:
        img_ventas = None
    
    try:
        img_reportes = tk.PhotoImage(file="Img/grafico.png")
        # Redimensionar imagen para el botón de reportes
        img_reportes = img_reportes.subsample(4, 4)  # Reducir tamaño similar a ventas
    except Exception:
        img_reportes = None
    
    try:
        img_configuraciones = tk.PhotoImage(file="Img/configuraciones.png")
        # Redimensionar imagen para el botón de configuraciones
        img_configuraciones = img_configuraciones.subsample(4, 4)  # Reducir tamaño similar a otros botones
    except Exception:
        img_configuraciones = None
    
    try:
        img_salir = tk.PhotoImage(file="Img/cancelar.png")
        # Redimensionar imagen para el botón de salir
        img_salir = img_salir.subsample(4, 4)  # Reducir tamaño similar a otros botones
    except Exception:
        img_salir = None
    
    # Crear botones en cuadrícula (2x2)
    # Fila 1
    if img_ventas:
        btn_ventas = tk.Button(frame_botones, text="VENTAS", 
                              image=img_ventas, compound=tk.TOP,
                              command=abrir_ventas, 
                              font=("Arial", 16, "bold"),
                              width=140, height=150,
                              bg="#357ab8", fg="white", relief="raised",
                              bd=2, padx=5, pady=10,
                              anchor='center',
                              justify='center')
    else:
        btn_ventas = ttk.Button(frame_botones, text="💰 VENTAS", 
                               command=abrir_ventas, style="Menu.TButton",
                               width=15)
    btn_ventas.grid(row=0, column=0, padx=20, pady=20)
    
    # Mantener referencia de la imagen
    if img_ventas:
        btn_ventas.image = img_ventas
    
    if img_reportes:
        btn_reportes = tk.Button(frame_botones, text="REPORTES", 
                                image=img_reportes, compound=tk.TOP,
                                command=abrir_reportes, 
                                font=("Arial", 16, "bold"),
                                width=140, height=150,
                                bg="#357ab8", fg="white", relief="raised",
                                bd=2, padx=5, pady=10,
                                anchor='center',
                                justify='center')
    else:
        btn_reportes = tk.Button(frame_botones, text="📊 REPORTES", 
                                command=abrir_reportes,
                                font=("Arial", 12, "bold"),
                                width=15, height=6,
                                bg="#357ab8", fg="white", relief="raised",
                                bd=2, padx=5, pady=5)
    btn_reportes.grid(row=0, column=1, padx=20, pady=20)
    
    # Mantener referencia de la imagen de reportes
    if img_reportes:
        btn_reportes.image = img_reportes
    
    # Fila 2
    if img_configuraciones:
        btn_configuraciones = tk.Button(frame_botones, text="AJUSTES", 
                                       image=img_configuraciones, compound=tk.TOP,
                                       command=abrir_configuraciones,
                                       font=("Arial", 16, "bold"),
                                       width=140, height=150,
                                       bg="#357ab8", fg="white", relief="raised",
                                       bd=2, padx=5, pady=10,
                                       anchor='center',
                                       justify='center')
    else:
        btn_configuraciones = tk.Button(frame_botones, text="AJUSTES", 
                                       command=abrir_configuraciones,
                                       font=("Arial", 12, "bold"),
                                       width=15, height=6,
                                       bg="#357ab8", fg="white", relief="raised",
                                       bd=2, padx=5, pady=5)
    btn_configuraciones.grid(row=1, column=0, padx=20, pady=20)
    
    # Mantener referencia de la imagen de configuraciones
    if img_configuraciones:
        btn_configuraciones.image = img_configuraciones
    
    if img_salir:
        btn_salir = tk.Button(frame_botones, text="SALIR", 
                             image=img_salir, compound=tk.TOP,
                             command=root.quit,
                             font=("Arial", 16, "bold"),
                             width=140, height=150,
                             bg="#357ab8", fg="white", relief="raised",
                             bd=2, padx=5, pady=10,
                             anchor='center',
                             justify='center')
    else:
        btn_salir = tk.Button(frame_botones, text="🚪 SALIR", 
                             command=root.quit,
                             font=("Arial", 12, "bold"),
                             width=15, height=6,
                             bg="#357ab8", fg="white", relief="raised",
                             bd=2, padx=5, pady=5)
    btn_salir.grid(row=1, column=1, padx=20, pady=20)
    
    # Mantener referencia de la imagen de salir
    if img_salir:
        btn_salir.image = img_salir
    
    # Centrar el frame de botones
    frame_botones.grid_columnconfigure(0, weight=1)
    frame_botones.grid_columnconfigure(1, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    # Crear la base de datos y las tablas si no existen
    crear_conexion_y_tablas("config/sqliteDB.db")
    crear_menu_principal()
