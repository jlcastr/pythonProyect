import tkinter as tk
from tkinter import ttk
import sys
import os
from View.email_view import abrir_config_email, mostrar_config_email_en_frame

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion

def mostrar_configuraciones_en_frame(parent_frame, callback_volver):
    """
    Mostrar menú de configuraciones dentro de un frame existente
    
    Args:
        parent_frame: Frame padre donde mostrar las configuraciones
        callback_volver: Función a llamar para volver al menú anterior
    """
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Cargar imagen de configuración para el título
    try:
        img_configuracion = tk.PhotoImage(file="Img/configuracion.png")
        img_configuracion = img_configuracion.subsample(4, 4)  # Medida 4 (aún más pequeña)
    except Exception:
        img_configuracion = None
    
    # Usar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Frame principal para las configuraciones
    main_frame = tk.Frame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver
    header_frame = tk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 30))
    
    btn_volver = tk.Button(header_frame, text="← Volver al Menú Principal", 
                          command=callback_volver, 
                          bg="#357ab8", fg="white", 
                          font=("Arial", 10, "bold"))
    btn_volver.pack(side="left")
    
    # Título con imagen de configuración
    if img_configuracion:
        titulo = tk.Label(header_frame, text=" CONFIGURACIONES", 
                         font=("Arial", 16, "bold"), fg="#2c3e50",
                         compound=tk.LEFT, image=img_configuracion)
        titulo.image = img_configuracion
        titulo.pack(side="right")
    else:
        titulo = tk.Label(header_frame, text="⚙️ CONFIGURACIONES", 
                         font=("Arial", 16, "bold"), fg="#2c3e50")
        titulo.pack(side="right")
    
    # Frame contenedor para los botones con estilo
    botones_frame = tk.Frame(main_frame, bg="#ecf0f1", relief="solid", bd=2)
    botones_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título de la sección
    titulo_seccion = tk.Label(botones_frame, text="🔧 Selecciona una Configuración:", 
                             font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
    titulo_seccion.pack(pady=(20, 30))
    
    # Configurar grid para centrar botones
    botones_frame.grid_rowconfigure(1, weight=1)
    botones_frame.grid_rowconfigure(2, weight=1)
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)
    
    # Frame interno para organizar botones en grid
    grid_frame = tk.Frame(botones_frame, bg="#ecf0f1")
    grid_frame.pack(expand=True)
    
    # Los botones ahora usarán ttk.Button con estilo consistente
    
    # Cargar imágenes para los botones (más pequeñas para mantener tamaño original)
    try:
        img_email = tk.PhotoImage(file="Img/correo-electronico.png")
        img_email = img_email.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_email = None
    
    try:
        img_logo = tk.PhotoImage(file="Img/subir-imagen.png")
        img_logo = img_logo.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_logo = None
    
    try:
        img_apariencia = tk.PhotoImage(file="Img/rueda-de-color.png")
        img_apariencia = img_apariencia.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_apariencia = None
    
    try:
        img_telefono = tk.PhotoImage(file="Img/telefono2.png")
        img_telefono = img_telefono.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_telefono = None
    
    # Funciones para cada botón (placeholder por ahora)
    def abrir_email():
        """Abrir configuración de email"""
        mostrar_config_email_en_frame(parent_frame, 
                                     lambda: mostrar_configuraciones_en_frame(parent_frame, callback_volver))
    
    def abrir_logo():
        """Abrir configuración de logo"""
        from tkinter import messagebox
        messagebox.showinfo("🖼️ Logo", 
                           "Configuración de Logo\n\n"
                           "Esta funcionalidad estará disponible próximamente.\n"
                           "Permitirá cambiar el logo de la aplicación y reportes.")
    
    def abrir_apariencia():
        """Abrir configuración de apariencia"""
        from tkinter import messagebox
        messagebox.showinfo("🎨 Apariencia", 
                           "Configuración de Apariencia\n\n"
                           "Esta funcionalidad estará disponible próximamente.\n"
                           "Permitirá cambiar temas, colores y fuentes de la aplicación.")
    
    def abrir_telefono():
        """Abrir configuración de teléfono"""
        from tkinter import messagebox
        messagebox.showinfo("📞 Teléfono", 
                           "Configuración de Teléfono\n\n"
                           "Esta funcionalidad estará disponible próximamente.\n"
                           "Permitirá configurar números de contacto para reportes y facturas.")
    
    # Botón Email (fila 0, columna 0) con imagen
    if img_email:
        btn_email = ttk.Button(grid_frame, text="Email", 
                              image=img_email, compound=tk.TOP,
                              command=abrir_email, style='Config.TButton',
                              cursor="hand2")
        btn_email.image = img_email  # Mantener referencia de la imagen
    else:
        btn_email = ttk.Button(grid_frame, text="Email", 
                              command=abrir_email, style='Config.TButton',
                              cursor="hand2")
    btn_email.grid(row=0, column=0, padx=15, pady=15, sticky="nsew", ipadx=30, ipady=25)
    
    # Botón Logo (fila 0, columna 1) con imagen
    if img_logo:
        btn_logo = ttk.Button(grid_frame, text="Logo", 
                             image=img_logo, compound=tk.TOP,
                             command=abrir_logo, style='Config.TButton',
                             cursor="hand2")
        btn_logo.image = img_logo  # Mantener referencia de la imagen
    else:
        btn_logo = ttk.Button(grid_frame, text="Logo", 
                             command=abrir_logo, style='Config.TButton',
                             cursor="hand2")
    btn_logo.grid(row=0, column=1, padx=15, pady=15, sticky="nsew", ipadx=30, ipady=25)
    
    # Botón Apariencia (fila 1, columna 0) con imagen
    if img_apariencia:
        btn_apariencia = ttk.Button(grid_frame, text="Apariencia", 
                                   image=img_apariencia, compound=tk.TOP,
                                   command=abrir_apariencia, style='Config.TButton',
                                   cursor="hand2")
        btn_apariencia.image = img_apariencia  # Mantener referencia de la imagen
    else:
        btn_apariencia = ttk.Button(grid_frame, text="Apariencia", 
                                   command=abrir_apariencia, style='Config.TButton',
                                   cursor="hand2")
    btn_apariencia.grid(row=1, column=0, padx=15, pady=15, sticky="nsew", ipadx=30, ipady=25)
    
    # Botón Teléfono (fila 1, columna 1) con imagen
    if img_telefono:
        btn_telefono = ttk.Button(grid_frame, text="Teléfono", 
                                 image=img_telefono, compound=tk.TOP,
                                 command=abrir_telefono, style='Config.TButton',
                                 cursor="hand2")
        btn_telefono.image = img_telefono  # Mantener referencia de la imagen
    else:
        btn_telefono = ttk.Button(grid_frame, text="Teléfono", 
                                 command=abrir_telefono, style='Config.TButton',
                                 cursor="hand2")
    btn_telefono.grid(row=1, column=1, padx=15, pady=15, sticky="nsew", ipadx=30, ipady=25)
    
    # Configurar peso de las celdas del grid para que se expandan uniformemente
    grid_frame.grid_rowconfigure(0, weight=1)
    grid_frame.grid_rowconfigure(1, weight=1)
    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)
    
    # Los efectos hover ahora se manejan automáticamente por ttk.Style
    
    # Información adicional
    info_frame = tk.Frame(botones_frame, bg="#ecf0f1")
    info_frame.pack(side="bottom", pady=(20, 15))
    
    info_label = tk.Label(info_frame, 
                         text="💡 Configura los diferentes aspectos de tu aplicación",
                         font=("Arial", 10), bg="#ecf0f1", fg="#7f8c8d")
    info_label.pack()

def mostrar_configuraciones(parent=None):
    """
    Función para mostrar configuraciones en ventana separada (mantener compatibilidad)
    
    Args:
        parent: Ventana padre (opcional)
    """
    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("⚙️ Configuraciones")
    root.geometry("600x500")
    root.resizable(True, True)
    
    # Configurar ícono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Cargar imagen de configuración para el título
    try:
        img_configuracion_popup = tk.PhotoImage(file="Img/configuracion.png")
        img_configuracion_popup = img_configuracion_popup.subsample(4, 4)  # Medida 4 (aún más pequeña)
    except Exception:
        img_configuracion_popup = None
    
    # Usar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Frame principal
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título con imagen de configuración
    if img_configuracion_popup:
        titulo = tk.Label(main_frame, text=" CONFIGURACIONES", 
                         font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#2c3e50",
                         compound=tk.LEFT, image=img_configuracion_popup)
        titulo.image = img_configuracion_popup
        titulo.pack(pady=(10, 30))
    else:
        titulo = tk.Label(main_frame, text="⚙️ CONFIGURACIONES", 
                         font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#2c3e50")
        titulo.pack(pady=(10, 30))
    
    # Frame para botones
    botones_frame = tk.Frame(main_frame, bg="#ecf0f1", relief="solid", bd=2)
    botones_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Título de sección
    titulo_seccion = tk.Label(botones_frame, text="🔧 Selecciona una Configuración:", 
                             font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
    titulo_seccion.pack(pady=(20, 30))
    
    # Grid frame
    grid_frame = tk.Frame(botones_frame, bg="#ecf0f1")
    grid_frame.pack(expand=True)
    
    # Cargar imágenes para los botones en ventana separada (más pequeñas)
    try:
        img_email_popup = tk.PhotoImage(file="Img/correo-electronico.png")
        img_email_popup = img_email_popup.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_email_popup = None
    
    try:
        img_logo_popup = tk.PhotoImage(file="Img/subir-imagen.png")
        img_logo_popup = img_logo_popup.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_logo_popup = None
    
    try:
        img_apariencia_popup = tk.PhotoImage(file="Img/rueda-de-color.png")
        img_apariencia_popup = img_apariencia_popup.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_apariencia_popup = None
    
    try:
        img_telefono_popup = tk.PhotoImage(file="Img/telefono2.png")
        img_telefono_popup = img_telefono_popup.subsample(6, 6)  # Redimensionar imagen más pequeña
    except Exception:
        img_telefono_popup = None
    
    # Los botones usarán ttk.Button con estilo consistente
    
    # Funciones para botones en ventana separada
    def abrir_email_popup():
        abrir_config_email(root)
    
    def abrir_logo_popup():
        from tkinter import messagebox
        messagebox.showinfo("Logo", 
                           "Configuración de Logo\n\n"
                           "Esta funcionalidad estará disponible próximamente.", 
                           parent=root)
    
    def abrir_apariencia_popup():
        from tkinter import messagebox
        messagebox.showinfo("Apariencia", 
                           "Configuración de Apariencia\n\n"
                           "Esta funcionalidad estará disponible próximamente.", 
                           parent=root)
    
    def abrir_telefono_popup():
        from tkinter import messagebox
        messagebox.showinfo("Teléfono", 
                           "Configuración de Teléfono\n\n"
                           "Esta funcionalidad estará disponible próximamente.", 
                           parent=root)
    
    # Crear botones con ttk.Button para consistencia multiplataforma
    if img_email_popup:
        btn_email = ttk.Button(grid_frame, text="Email", 
                              image=img_email_popup, compound=tk.TOP,
                              command=abrir_email_popup, style='ConfigPopup.TButton',
                              cursor="hand2")
        btn_email.image = img_email_popup  # Mantener referencia de la imagen
    else:
        btn_email = ttk.Button(grid_frame, text="Email", 
                              command=abrir_email_popup, style='ConfigPopup.TButton',
                              cursor="hand2")
    btn_email.grid(row=0, column=0, padx=20, pady=20, ipadx=30, ipady=25)
    
    if img_logo_popup:
        btn_logo = ttk.Button(grid_frame, text="Logo", 
                             image=img_logo_popup, compound=tk.TOP,
                             command=abrir_logo_popup, style='ConfigPopup.TButton',
                             cursor="hand2")
        btn_logo.image = img_logo_popup  # Mantener referencia de la imagen
    else:
        btn_logo = ttk.Button(grid_frame, text="Logo", 
                             command=abrir_logo_popup, style='ConfigPopup.TButton',
                             cursor="hand2")
    btn_logo.grid(row=0, column=1, padx=20, pady=20, ipadx=30, ipady=25)
    
    if img_apariencia_popup:
        btn_apariencia = ttk.Button(grid_frame, text="Apariencia", 
                                   image=img_apariencia_popup, compound=tk.TOP,
                                   command=abrir_apariencia_popup, style='ConfigPopup.TButton',
                                   cursor="hand2")
        btn_apariencia.image = img_apariencia_popup  # Mantener referencia de la imagen
    else:
        btn_apariencia = ttk.Button(grid_frame, text="Apariencia", 
                                   command=abrir_apariencia_popup, style='ConfigPopup.TButton',
                                   cursor="hand2")
    btn_apariencia.grid(row=1, column=0, padx=20, pady=20, ipadx=30, ipady=25)
    
    if img_telefono_popup:
        btn_telefono = ttk.Button(grid_frame, text="Teléfono", 
                                 image=img_telefono_popup, compound=tk.TOP,
                                 command=abrir_telefono_popup, style='ConfigPopup.TButton',
                                 cursor="hand2")
        btn_telefono.image = img_telefono_popup  # Mantener referencia de la imagen
    else:
        btn_telefono = ttk.Button(grid_frame, text="Teléfono", 
                                 command=abrir_telefono_popup, style='ConfigPopup.TButton',
                                 cursor="hand2")
    btn_telefono.grid(row=1, column=1, padx=20, pady=20, ipadx=30, ipady=25)
    
    # Los efectos hover se manejan automáticamente por ttk.Style
    
    # Información
    info_label = tk.Label(botones_frame, 
                         text="💡 Configura los diferentes aspectos de tu aplicación",
                         font=("Arial", 10), bg="#ecf0f1", fg="#7f8c8d")
    info_label.pack(side="bottom", pady=15)
    
    # Manejar cierre de ventana
    def on_close():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
