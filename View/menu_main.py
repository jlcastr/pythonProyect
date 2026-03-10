import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_setup import crear_conexion_y_tablas, obtener_conexion
from Controller.styles import configurar_estilos_aplicacion, Colores, Fuentes
from Controller.styles_mac import configurar_estilos_macos, crear_boton_macos, es_macos

def crear_menu_principal():
    """Crear ventana del menú principal con diseño profesional y adaptativo"""
    root = tk.Tk()
    root.title('Sistema de Manejo de Ventas')
    
    # Configuración inicial de ventana adaptativa
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calcular tamaño de ventana basado en resolución
    if screen_width >= 1920:
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
    elif screen_width >= 1366:
        window_width = int(screen_width * 0.90)
        window_height = int(screen_height * 0.90)
    else:
        window_width = int(screen_width * 0.95)
        window_height = int(screen_height * 0.95)
    
    # Centrar ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(True, True)
    root.configure(bg='#ecf0f1')
    
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
    
    # Variables globales para manejo de redimensionamiento
    current_config = None
    menu_elements = {}
    last_window_size = (0, 0)
    
    def recrear_menu_adaptativo():
        """Recrear el menú con la nueva configuración adaptativa"""
        print("🔄 Recreando menú con nueva resolución...")

    def on_window_resize(event=None):
        """Función que detecta cambios de resolución"""
        nonlocal last_window_size, current_config
        
        # Solo procesar eventos de la ventana principal
        if event and event.widget != root:
            return
            
        try:
            # Obtener resolución actual de pantalla
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            current_size = (screen_width, screen_height)
            
            # Solo informar si cambió la resolución de pantalla
            if current_size != last_window_size:
                last_window_size = current_size
                
                # Obtener nueva configuración adaptativa
                from Controller.styles import obtener_configuracion_adaptativa
                new_config = obtener_configuracion_adaptativa(root)
                
                if new_config != current_config:
                    current_config = new_config
                    print(f"🖥️  Resolución detectada: {screen_width}x{screen_height}")
                    print(f"📐 Nueva configuración: Botones {new_config['button_width']}x{new_config['button_height']}, Íconos {new_config['icon_size']}px")
                    print("💡 Reinicia la aplicación para ver los cambios aplicados")
                    
        except Exception as e:
            print(f"Error detectando resolución: {e}")
    
    # Detectar cambios de resolución
    root.bind('<Configure>', on_window_resize)
    
    # Función para crear título visual con logo
    def crear_titulo_visual():
        # Frame contenedor para el título
        titulo_frame = tk.Frame(root, bg='#ecf0f1', pady=20)
        titulo_frame.pack(pady=(20, 10))
        
        # Intentar cargar logo desde la configuración de BD
        logo_img = None
        try:
            from Controller.SQL.db_operations import consultar_logo_config
            config_logo = consultar_logo_config('ventanas')
            
            if config_logo and config_logo['archivo_path'] and os.path.exists(config_logo['archivo_path']):
                # Cargar logo desde la carpeta Logos
                from PIL import Image, ImageTk
                img = Image.open(config_logo['archivo_path'])
                img = img.resize((80, 80), Image.Resampling.LANCZOS)  # Tamaño apropiado para título
                logo_img = ImageTk.PhotoImage(img)
            elif os.path.exists('Img/SM2.ico'):
                # Fallback al logo por defecto
                from PIL import Image, ImageTk
                img = Image.open('Img/SM2.ico')
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                logo_img = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
        
        if logo_img:
            # Frame horizontal para logo + texto
            contenido_frame = tk.Frame(titulo_frame, bg='#ecf0f1')
            contenido_frame.pack()
            
            # Logo
            logo_label = tk.Label(contenido_frame, image=logo_img, bg='#ecf0f1')
            logo_label.image = logo_img  # Mantener referencia
            logo_label.pack(side='left', padx=(0, 20))
            
            # Texto del título
            texto_frame = tk.Frame(contenido_frame, bg='#ecf0f1')
            texto_frame.pack(side='left')
            
            # Título principal
            titulo_principal = tk.Label(texto_frame, text="Sistema de Manejo de Ventas", 
                                       font=("Arial", 28, "bold"), 
                                       fg="#2c3e50", bg="#ecf0f1")
            titulo_principal.pack()
            
            # Subtítulo
            subtitulo = tk.Label(texto_frame, text="Gestión Empresarial Profesional", 
                               font=("Arial", 14), 
                               fg="#7f8c8d", bg="#ecf0f1")
            subtitulo.pack()
        else:
            # Sin logo, solo texto centrado
            titulo_principal = tk.Label(titulo_frame, text="Sistema de Manejo de Ventas", 
                                       font=("Arial", 32, "bold"), 
                                       fg="#2c3e50", bg="#ecf0f1")
            titulo_principal.pack()
            
            subtitulo = tk.Label(titulo_frame, text="Gestión Empresarial Profesional", 
                               font=("Arial", 16), 
                               fg="#7f8c8d", bg="#ecf0f1")
            subtitulo.pack()
        
        return titulo_frame
    
    # Crear título visual
    titulo = crear_titulo_visual()
    

    
    def abrir_ventas():
        """Abrir el módulo de ventas con transición suave"""
        # Crear el frame de ventas ANTES de ocultar el menú
        conn = obtener_conexion()
        if not conn:
            print("[ERROR] No se puede conectar a la base de datos")
            return
        cursor = conn.cursor()
        
        frame_ventas = tk.Frame(root, bg='#ecf0f1')
        
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
        frame_reportes = tk.Frame(root, bg='#ecf0f1')
        
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
        frame_configuraciones = tk.Frame(root, bg='#ecf0f1')
        
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
    
    def abrir_inventario():
        """Abrir el módulo de inventario con transición suave"""
        # Crear el frame de inventario ANTES de ocultar el menú
        frame_inventario = tk.Frame(root, bg='#ecf0f1')
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de inventario inmediatamente
        frame_inventario.pack(fill="both", expand=True)
        root.update_idletasks()
        
        # Por ahora, mostrar un placeholder hasta que se implemente el módulo
        placeholder_label = tk.Label(frame_inventario, 
                                   text="📦 MÓDULO DE INVENTARIO\n\nEn desarrollo...",
                                   font=("Arial", 20, "bold"),
                                   fg="#2c3e50", bg="#ecf0f1")
        placeholder_label.pack(expand=True)
        
        # Botón para volver al menú
        btn_volver = tk.Button(frame_inventario, text="← Volver al Menú",
                              command=lambda: volver_al_menu_desde_inventario(frame_inventario),
                              font=("Arial", 12), bg="#3498db", fg="white",
                              padx=20, pady=10)
        btn_volver.pack(pady=20)
    
    def volver_al_menu_desde_inventario(frame_actual):
        """Volver al menú principal desde inventario con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    def abrir_inventario():
        """Abrir el módulo de inventario con transición suave"""
        # Crear el frame de inventario ANTES de ocultar el menú
        frame_inventario = tk.Frame(root, bg='#ecf0f1')
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de inventario inmediatamente
        frame_inventario.pack(fill="both", expand=True)
        root.update_idletasks()
        
        # Por ahora, mostrar un placeholder hasta que se implemente el módulo
        placeholder_label = tk.Label(frame_inventario, 
                                   text="📦 MÓDULO DE INVENTARIO\n\nEn desarrollo...",
                                   font=("Arial", 20, "bold"),
                                   fg="#2c3e50", bg="#ecf0f1")
        placeholder_label.pack(expand=True)
        
        # Botón para volver al menú
        btn_volver = tk.Button(frame_inventario, text="← Volver al Menú",
                              command=lambda: volver_al_menu_desde_inventario(frame_inventario),
                              font=("Arial", 12), bg="#3498db", fg="white",
                              padx=20, pady=10)
        btn_volver.pack(pady=20)
    
    def volver_al_menu_desde_inventario(frame_actual):
        """Volver al menú principal desde inventario con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    def abrir_clientes():
        """Abrir el módulo de clientes con transición suave"""
        # Crear el frame de clientes ANTES de ocultar el menú
        frame_clientes = tk.Frame(root, bg='#ecf0f1')
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de clientes inmediatamente
        frame_clientes.pack(fill="both", expand=True)
        root.update_idletasks()
        
        # Por ahora, mostrar un placeholder hasta que se implemente el módulo
        placeholder_label = tk.Label(frame_clientes, 
                                   text="👥 MÓDULO DE CLIENTES\n\nEn desarrollo...",
                                   font=("Arial", 20, "bold"),
                                   fg="#2c3e50", bg="#ecf0f1")
        placeholder_label.pack(expand=True)
        
        # Botón para volver al menú
        btn_volver = tk.Button(frame_clientes, text="← Volver al Menú",
                              command=lambda: volver_al_menu_desde_clientes(frame_clientes),
                              font=("Arial", 12), bg="#3498db", fg="white",
                              padx=20, pady=10)
        btn_volver.pack(pady=20)
    
    def volver_al_menu_desde_clientes(frame_actual):
        """Volver al menú principal desde clientes con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    def abrir_precios():
        """Abrir el módulo de precios con transición suave"""
        # Crear el frame de precios ANTES de ocultar el menú
        frame_precios = tk.Frame(root, bg='#ecf0f1')
        
        # Ocultar elementos del menú
        titulo.pack_forget()
        frame_contenedor.pack_forget()
        pie_pagina.pack_forget()
        
        # Mostrar frame de precios inmediatamente
        frame_precios.pack(fill="both", expand=True)
        root.update_idletasks()
        
        # Por ahora, mostrar un placeholder hasta que se implemente el módulo
        placeholder_label = tk.Label(frame_precios, 
                                   text="💰 MÓDULO DE PRECIOS\n\nEn desarrollo...",
                                   font=("Arial", 20, "bold"),
                                   fg="#2c3e50", bg="#ecf0f1")
        placeholder_label.pack(expand=True)
        
        # Botón para volver al menú
        btn_volver = tk.Button(frame_precios, text="← Volver al Menú",
                              command=lambda: volver_al_menu_desde_precios(frame_precios),
                              font=("Arial", 12), bg="#3498db", fg="white",
                              padx=20, pady=10)
        btn_volver.pack(pady=20)
    
    def volver_al_menu_desde_precios(frame_actual):
        """Volver al menú principal desde precios con transición suave"""
        # Mostrar elementos del menú ANTES de destruir el frame actual
        titulo.pack()
        frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
        pie_pagina.pack(side="bottom", pady=15)
        
        # Forzar actualización inmediata de la interfaz
        root.update_idletasks()
        
        # Destruir frame y reconfigurar estilos
        frame_actual.destroy()
        configurar_estilos_aplicacion()
    
    # Obtener configuración adaptativa para íconos usando la ventana actual
    from Controller.styles import obtener_configuracion_adaptativa
    config = obtener_configuracion_adaptativa(root)
    current_config = config  # Guardar configuración inicial
    icon_size = config['icon_size']
    
    # Cargar imágenes adaptativas para los botones
    try:
        from PIL import Image, ImageTk
        # Cargar imágenes con tamaño adaptativo
        img_ventas = ImageTk.PhotoImage(Image.open("Img/pago-en-efectivo.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_ventas = None
    
    try:
        img_reportes = ImageTk.PhotoImage(Image.open("Img/grafico.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_reportes = None
    
    try:
        img_configuraciones = ImageTk.PhotoImage(Image.open("Img/configuraciones.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_configuraciones = None
    
    try:
        img_inventario = ImageTk.PhotoImage(Image.open("Img/inventario2.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_inventario = None
    
    try:
        img_clientes = ImageTk.PhotoImage(Image.open("Img/agregar-usuario.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_clientes = None
    
    try:
        img_precios = ImageTk.PhotoImage(Image.open("Img/dinero.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_precios = None
    
    try:
        img_salir = ImageTk.PhotoImage(Image.open("Img/cancelar.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS))
    except Exception:
        img_salir = None
    
    # Configuración de botones para crear_menu_principal_estandarizado
    botones_config = [
        {'texto': 'VENTAS', 'comando': abrir_ventas, 'imagen': img_ventas, 'fila': 0, 'columna': 0},
        {'texto': 'REPORTES', 'comando': abrir_reportes, 'imagen': img_reportes, 'fila': 0, 'columna': 1},
        {'texto': 'INVENTARIO', 'comando': abrir_inventario, 'imagen': img_inventario, 'fila': 0, 'columna': 2},
        {'texto': 'CLIENTES', 'comando': abrir_clientes, 'imagen': img_clientes, 'fila': 1, 'columna': 0},
        {'texto': 'AJUSTES', 'comando': abrir_configuraciones, 'imagen': img_configuraciones, 'fila': 1, 'columna': 1},
        {'texto': 'PRECIOS', 'comando': abrir_precios, 'imagen': img_precios, 'fila': 1, 'columna': 2},
        {'texto': 'SALIR', 'comando': root.quit, 'imagen': img_salir, 'fila': 2, 'columna': 1, 'columnspan': 1}
    ]
    
    # Usar la función estandarizada para crear el menú con btnblanco250.png
    if es_macos():
        from Controller.styles_mac import crear_menu_principal_estandarizado_mac
        frame_contenedor, grid_frame = crear_menu_principal_estandarizado_mac(root, "Menú Principal", botones_config)
    else:
        from Controller.styles import crear_menu_principal_estandarizado
        frame_contenedor, grid_frame = crear_menu_principal_estandarizado(root, "Menú Principal", botones_config)
    
    # Pie de página profesional
    pie_pagina = tk.Label(root, text="© 2025 Sistema de Gestión Empresarial | Versión 1.0", 
                         font=("Arial", 12), 
                         fg="#34495e", bg="#ecf0f1")
    pie_pagina.pack(side="bottom", pady=15)
    
    root.mainloop()

if __name__ == '__main__':
    # crear_conexion_y_tablas('sales_system.db')  # Comentado para evitar crear BD automáticamente
    crear_menu_principal()
