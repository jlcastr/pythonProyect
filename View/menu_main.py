import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_setup import crear_conexion_y_tablas
from Controller.styles import configurar_estilos_aplicacion, Colores, Fuentes
from Controller.styles_mac import configurar_estilos_macos, crear_boton_macos, es_macos

def crear_menu_principal():
    """Crear ventana del menú principal con diseño profesional"""
    root = tk.Tk()
    root.title('S&M - Sistema de Manejo de Ventas')
    root.state('zoomed')
    root.resizable(True, True)
    root.configure(bg=Colores.FONDO_PRINCIPAL)
    
    # Intentar aplicar el icono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Usar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Configurar estilos específicos para macOS
    if es_macos():
        configurar_estilos_macos()
    
    # Título principal con estilo mejorado
    titulo = tk.Label(root, text="S&M - Sistema de Manejo de Ventas", 
                     font=("Arial", 32, "bold"), 
                     fg="#2c3e50", bg="#ecf0f1",
                     pady=30)
    titulo.pack()
    
    # Crear frame contenedor con recuadro negro
    frame_contenedor = tk.Frame(root, bg=Colores.FONDO_PRINCIPAL, pady=20)
    frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
    
    # Frame con borde negro (recuadro)
    frame_recuadro = tk.Frame(frame_contenedor, bg=Colores.TEXTO_OSCURO, bd=1, relief="solid")
    frame_recuadro.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Frame interior con fondo claro
    frame_interior = tk.Frame(frame_recuadro, bg=Colores.BLANCO, bd=0)
    frame_interior.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Frame principal para los botones (dentro del recuadro)
    frame_botones = tk.Frame(frame_interior, bg=Colores.BLANCO)
    frame_botones.pack(expand=True, pady=40)
    
    # Los efectos hover ahora se manejan automáticamente por ttk.Style
    
    def abrir_ventas():
        """Abrir el módulo de ventas con transición suave"""
        # Crear el frame de ventas ANTES de ocultar el menú
        conn = sqlite3.connect("config/sqliteDB.db")
        cursor = conn.cursor()
        
        frame_ventas = tk.Frame(root, bg=Colores.FONDO_VENTAS)
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de ventas inmediatamente
        frame_ventas.pack(fill="both", expand=True)
        root.update_idletasks()
        
        from View.Sales import crear_interfaz_ventas_en_frame
        crear_interfaz_ventas_en_frame(frame_ventas, conn, cursor, lambda: volver_al_menu(frame_ventas, conn))
    
    def volver_al_menu(frame_actual, conn):
        """Volver al menú principal con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Cerrar conexión y destruir frame
        conn.close()
        frame_actual.destroy()
        
        # Reconfigurar estilos al volver al menú
        configurar_estilos_aplicacion()
    
    def abrir_reportes():
        """Abrir el módulo de reportes con transición suave"""
        # Crear el frame de reportes ANTES de ocultar el menú
        frame_reportes = tk.Frame(root, bg=Colores.FONDO_PRINCIPAL)
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de reportes inmediatamente
        frame_reportes.pack(fill="both", expand=True)
        root.update_idletasks()
        
        from View.Report_menu import crear_menu_reportes
        crear_menu_reportes(frame_reportes, lambda: volver_al_menu_desde_reportes(frame_reportes))
    
    def volver_al_menu_desde_reportes(frame_actual):
        """Volver al menú principal desde reportes con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    def abrir_configuraciones():
        """Abrir el módulo de configuraciones con transición suave"""
        # Crear el frame de configuraciones ANTES de ocultar el menú
        frame_configuraciones = tk.Frame(root, bg=Colores.FONDO_PRINCIPAL)
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de configuraciones inmediatamente
        frame_configuraciones.pack(fill="both", expand=True)
        root.update_idletasks()
        
        from View.menu_settings_view import mostrar_configuraciones_en_frame
        mostrar_configuraciones_en_frame(frame_configuraciones, lambda: volver_al_menu_desde_configuraciones(frame_configuraciones))
    
    def volver_al_menu_desde_configuraciones(frame_actual):
        """Volver al menú principal desde configuraciones con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    # Cargar imágenes para los botones (más pequeñas para dar espacio al texto)
    try:
        img_ventas = tk.PhotoImage(file="Img/pago-en-efectivo.png")
        img_ventas = img_ventas.subsample(4, 4)  # Más pequeñas
    except Exception:
        img_ventas = None
    
    try:
        img_reportes = tk.PhotoImage(file="Img/grafico.png")
        img_reportes = img_reportes.subsample(4, 4)  # Más pequeñas
    except Exception:
        img_reportes = None
    
    try:
        img_configuraciones = tk.PhotoImage(file="Img/configuraciones.png")
        img_configuraciones = img_configuraciones.subsample(4, 4)  # Más pequeñas
    except Exception:
        img_configuraciones = None
    
    try:
        img_salir = tk.PhotoImage(file="Img/cancelar.png")
        img_salir = img_salir.subsample(4, 4)  # Más pequeñas
    except Exception:
        img_salir = None
    
    # Crear botones con estilo profesional usando ttk
    # Botón VENTAS
    ventas_style = 'MacVentas.TButton' if es_macos() else 'Ventas.TButton'
    if img_ventas:
        btn_ventas = ttk.Button(frame_botones, text="VENTAS", 
                               image=img_ventas, compound=tk.TOP,
                               command=abrir_ventas,
                               style=ventas_style,
                               cursor="hand2")
        btn_ventas.image = img_ventas
    else:
        btn_ventas = ttk.Button(frame_botones, text="💰 VENTAS", 
                               command=abrir_ventas,
                               style=ventas_style,
                               cursor="hand2")
    
    btn_ventas.grid(row=0, column=0, padx=40, pady=30, sticky="nsew", ipadx=30, ipady=60)
    
    # Botón REPORTES
    reportes_style = 'MacReportes.TButton' if es_macos() else 'Reportes.TButton'
    if img_reportes:
        btn_reportes = ttk.Button(frame_botones, text="REPORTES", 
                                 image=img_reportes, compound=tk.TOP,
                                 command=abrir_reportes,
                                 style=reportes_style,
                                 cursor="hand2")
        btn_reportes.image = img_reportes
    else:
        btn_reportes = ttk.Button(frame_botones, text="📊 REPORTES", 
                                 command=abrir_reportes,
                                 style=reportes_style,
                                 cursor="hand2")
    
    btn_reportes.grid(row=0, column=1, padx=40, pady=30, sticky="nsew", ipadx=30, ipady=60)
    
    # Botón AJUSTES
    ajustes_style = 'MacAjustes.TButton' if es_macos() else 'Ajustes.TButton'
    if img_configuraciones:
        btn_configuraciones = ttk.Button(frame_botones, text="AJUSTES", 
                                         image=img_configuraciones, compound=tk.TOP,
                                         command=abrir_configuraciones,
                                         style=ajustes_style,
                                         cursor="hand2")
        btn_configuraciones.image = img_configuraciones
    else:
        btn_configuraciones = ttk.Button(frame_botones, text="⚙️ AJUSTES", 
                                         command=abrir_configuraciones,
                                         style=ajustes_style,
                                         cursor="hand2")
    
    btn_configuraciones.grid(row=1, column=0, padx=40, pady=30, sticky="nsew", ipadx=30, ipady=60)
    
    # Botón SALIR
    salir_style = 'MacSalir.TButton' if es_macos() else 'Salir.TButton'
    if img_salir:
        btn_salir = ttk.Button(frame_botones, text="SALIR", 
                              image=img_salir, compound=tk.TOP,
                              command=root.quit,
                              style=salir_style,
                              cursor="hand2")
        btn_salir.image = img_salir
    else:
        btn_salir = ttk.Button(frame_botones, text="🚪 SALIR", 
                              command=root.quit,
                              style=salir_style,
                              cursor="hand2")
    
    btn_salir.grid(row=1, column=1, padx=40, pady=30, sticky="nsew", ipadx=30, ipady=60)
    
    # Configurar el grid para distribución uniforme
    frame_botones.grid_columnconfigure(0, weight=1)
    frame_botones.grid_columnconfigure(1, weight=1)
    frame_botones.grid_rowconfigure(0, weight=1)
    frame_botones.grid_rowconfigure(1, weight=1)
    
    # Pie de página profesional
    pie_pagina = tk.Label(root, text="© 2025 S&M - Sistema de Gestión Empresarial | Versión 1.0", 
                         font=("Arial", 12), 
                         fg="#34495e", bg="#ecf0f1")
    pie_pagina.pack(side="bottom", pady=15)
    
    root.mainloop()

if __name__ == '__main__':
    crear_conexion_y_tablas('config/sqliteDB.db')
    crear_menu_principal()
