"""
Módulo de estilos centralizados para la aplicación S&M - Sistema de Manejo de Ventas
Este archivo contiene todas las configuraciones de estilos ttk para mantener consistencia visual
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


def configurar_estilos_aplicacion():
    """
    Configura todos los estilos ttk para la aplicación.
    Incluye estilos para botones principales, reportes, configuraciones, etc.
    
    Returns:
        ttk.Style: Objeto Style configurado con todos los estilos de la aplicación
    """
    style = ttk.Style()
    style.theme_use('clam')  # Tema consistente multiplataforma
    
    # Configuración general para mejorar la apariencia
    style.configure('TButton', 
                   borderwidth=0,           # Eliminar bordes por defecto
                   focuscolor='none',       # Sin línea de enfoque
                   relief='flat')           # Diseño plano moderno
    
    # =========================================================================
    # ESTILOS PARA MENÚ PRINCIPAL - DISEÑO MODERNO
    # =========================================================================
    
    # Estilo base para botones principales
    style.configure('MainButton.TButton',
                   font=('Arial', 18, 'bold'),
                   foreground='white',
                   borderwidth=3,
                   relief='raised',
                   focuscolor='none')
    
    # Cargar imagen de fondo para botones del menú principal
    try:
        from PIL import Image, ImageTk
        # Cargar imagen de fondo desde la carpeta Buttons
        btn_bg_image = Image.open('Img/Buttons/btnblanco250.png')
        btn_bg_photo = ImageTk.PhotoImage(btn_bg_image)
        
        # Almacenar la imagen en el style para evitar que se elimine por garbage collector
        style._btn_bg_image = btn_bg_photo
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
        btn_bg_photo = None
    
    # Estilos específicos para cada botón del menú principal - CON IMAGEN DE FONDO
    style.configure('Ventas.TButton', 
                   foreground='#2c3e50',  # Texto oscuro para contrastar con fondo blanco
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,  # Sin borde para mostrar la imagen
                   relief='flat',  # Plano para mostrar imagen de fondo
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Reportes.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Ajustes.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Inventario.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Clientes.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Precios.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    style.configure('Salir.TButton', 
                   foreground='#2c3e50',
                   font=('Arial', 12, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   padding=(15, 10),
                   focuscolor='none')
    
    # Efectos hover suaves para botones con imagen de fondo
    style.map('Ventas.TButton', 
             foreground=[('active', '#1f618d'),   # Texto más oscuro en hover
                        ('pressed', '#154360')],  # Texto aún más oscuro al presionar
             relief=[('pressed', 'sunken')])      # Efecto hundido al presionar
    
    style.map('Reportes.TButton', 
             foreground=[('active', '#a93226'),   # Texto rojizo en hover
                        ('pressed', '#922b21')],
             relief=[('pressed', 'sunken')])
    
    style.map('Ajustes.TButton', 
             foreground=[('active', '#d68910'),   # Texto anaranjado en hover
                        ('pressed', '#b7950b')],
             relief=[('pressed', 'sunken')])
    
    style.map('Inventario.TButton', 
             foreground=[('active', '#1e8449'),   # Texto verde en hover
                        ('pressed', '#186a3b')],
             relief=[('pressed', 'sunken')])
    
    style.map('Clientes.TButton', 
             foreground=[('active', '#7d3c98'),   # Texto púrpura en hover
                        ('pressed', '#6c3483')],
             relief=[('pressed', 'sunken')])
    
    style.map('Precios.TButton', 
             foreground=[('active', '#d68910'),   # Texto amarillo en hover
                        ('pressed', '#b7950b')],
             relief=[('pressed', 'sunken')])
    
    style.map('Salir.TButton', 
             foreground=[('active', '#424949'),   # Texto gris en hover
                        ('pressed', '#2e4053')],
             relief=[('pressed', 'sunken')])
    
    # =========================================================================
    # ESTILOS PARA MENÚ DE REPORTES
    # =========================================================================
    
    # Estilo para botones de reportes
    style.configure('ReportButton.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#2980b9',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón volver
    style.configure('VolverButton.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#2980b9',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Efectos hover para botones de reportes
    style.map('ReportButton.TButton',
             background=[('active', '#1f618d')],
             foreground=[('active', 'white')])
    style.map('VolverButton.TButton',
             background=[('active', '#1f618d')],
             foreground=[('active', 'white')])
    
    # =========================================================================
    # ESTILOS PARA MENÚ DE CONFIGURACIONES
    # =========================================================================
    
    # Estilo para botones de configuración
    style.configure('Config.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#2980b9',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botones de configuración en popup
    style.configure('ConfigPopup.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#2980b9',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Efectos hover para botones de configuración
    style.map('Config.TButton',
             background=[('active', '#1f618d')],
             foreground=[('active', 'white')],
             relief=[('pressed', 'sunken')])
    style.map('ConfigPopup.TButton',
             background=[('active', '#1f618d')],
             foreground=[('active', 'white')],
             relief=[('pressed', 'sunken')])
    
    # =========================================================================
    # ESTILOS PARA MÓDULO DE VENTAS
    # =========================================================================
    
    # Estilo para botón Eliminar (Rojo)
    style.configure('EliminarVenta.TButton',
                   font=('Arial', 9, 'bold'),
                   foreground='white',
                   background='#e74c3c',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón Modificar (Azul)
    style.configure('ModificarVenta.TButton',
                   font=('Arial', 9, 'bold'),
                   foreground='white',
                   background='#2980b9',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón Finalizar Venta (Verde)
    style.configure('FinalizarVenta.TButton',
                   font=('Arial', 12, 'bold'),
                   foreground='white',
                   background='#27ae60',
                   borderwidth=3,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón Agregar (Verde claro)
    style.configure('AgregarVenta.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#27ae60',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón Cancelar (Rojo)
    style.configure('CancelarVenta.TButton',
                   font=('Arial', 10, 'bold'),
                   foreground='white',
                   background='#e74c3c',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Estilo para botón Limpiar (Gris)
    style.configure('LimpiarVenta.TButton',
                   font=('Arial', 9, 'bold'),
                   foreground='white',
                   background='#95a5a6',
                   borderwidth=2,
                   relief='raised',
                   focuscolor='none')
    
    # Efectos hover para botones de ventas
    style.map('EliminarVenta.TButton',
             background=[('active', '#c0392b')],
             foreground=[('active', 'white')])
    style.map('ModificarVenta.TButton',
             background=[('active', '#1f618d')],
             foreground=[('active', 'white')])
    style.map('FinalizarVenta.TButton',
             background=[('active', '#229954')],
             foreground=[('active', 'white')])
    style.map('AgregarVenta.TButton',
             background=[('active', '#229954')],
             foreground=[('active', 'white')])
    style.map('CancelarVenta.TButton',
             background=[('active', '#c0392b')],
             foreground=[('active', 'white')])
    style.map('LimpiarVenta.TButton',
             background=[('active', '#7f8c8d')],
             foreground=[('active', 'white')])
    
    # =========================================================================
    # ESTILOS ADICIONALES
    # =========================================================================
    
    # Estilo para botones secundarios
    style.configure('Secondary.TButton',
                   font=('Arial', 9, 'normal'),
                   foreground='#2c3e50',
                   background='#ecf0f1',
                   borderwidth=1,
                   relief='raised')
    
    style.map('Secondary.TButton',
             background=[('active', '#bdc3c7')],
             foreground=[('active', '#2c3e50')])
    
    # Configurar estilos de Treeview
    EstilosTreeview.configurar_treeview_minimal(style)
    EstilosTreeview.configurar_treeview_producto(style)
    
    return style


def aplicar_estilo_ventana(ventana, titulo="S&M - Sistema de Manejo de Ventas"):
    """
    Aplica configuraciones estándar a una ventana de la aplicación.
    
    Args:
        ventana: Objeto tk.Tk() o tk.Toplevel()
        titulo (str): Título de la ventana
    """
    ventana.title(titulo)
    ventana.configure(bg='#ecf0f1')
    
    # Intentar aplicar el icono
    try:
        ventana.iconbitmap('Img/SM2.ico')
    except Exception:
        pass


# Constantes de colores para uso en toda la aplicación
class Colores:
    """Paleta de colores consistente para toda la aplicación"""
    AZUL_PRINCIPAL = '#3498db'
    AZUL_HOVER = '#2980b9'
    ROJO_PRINCIPAL = '#e74c3c'
    ROJO_HOVER = '#c0392b'
    NARANJA_PRINCIPAL = '#f39c12'
    NARANJA_HOVER = '#e67e22'
    GRIS_PRINCIPAL = '#95a5a6'
    GRIS_HOVER = '#7f8c8d'
    AZUL_REPORTES = '#2980b9'
    AZUL_REPORTES_HOVER = '#1f618d'
    FONDO_PRINCIPAL = '#ecf0f1'
    TEXTO_OSCURO = '#2c3e50'
    TEXTO_CLARO = '#7f8c8d'
    BLANCO = '#ffffff'
    
    # Colores específicos para módulo de ventas
    FONDO_VENTAS = '#f8f9fa'
    TEXTO_SECUNDARIO = '#34495e'
    VERDE_VENTAS = '#27ae60'
    TREEVIEW_FONDO = '#fafafa'
    TREEVIEW_SELECCION = '#e0e0e0'
    TREEVIEW_HEADING = '#eaeaea'
    TREEVIEW_HEADING_HOVER = '#cccccc'
    FILAS_PAR = '#ffffff'
    FILAS_IMPAR = '#e6f2ff'


# Configuración de fuentes
class Fuentes:
    """Configuración de fuentes consistente"""
    TITULO_PRINCIPAL = ("Arial", 28, "bold")
    TITULO_SECUNDARIO = ("Arial", 16, "bold")
    TITULO_MODULO = ("Arial", 18, "bold")
    BOTON_PRINCIPAL = ("Arial", 18, "bold")
    BOTON_SECUNDARIO = ("Arial", 10, "bold")
    BOTON_PEQUEÑO = ("Arial", 9, "bold")
    BOTON_GRANDE = ("Arial", 12, "bold")
    TEXTO_NORMAL = ("Arial", 11)
    TEXTO_PEQUEÑO = ("Arial", 9)
    TEXTO_CAMPO = ("Arial", 10)
    TEXTO_CAMPO_BOLD = ("Arial", 10, "bold")
    TEXTO_LABEL = ("Arial", 11, "bold")
    TREEVIEW_FONT = ("Segoe UI", 10)
    TREEVIEW_HEADING_FONT = ("Segoe UI", 10, "bold")


# Configuraciones de Treeview centralizadas
class EstilosTreeview:
    """Configuraciones estándar para Treeview"""
    
    @staticmethod
    def configurar_treeview_minimal(style):
        """Configura el estilo minimal para Treeview"""
        style.configure("minimal.Treeview",
                       background=Colores.TREEVIEW_FONDO,
                       foreground="#222",
                       rowheight=24,
                       fieldbackground=Colores.TREEVIEW_FONDO,
                       font=Fuentes.TREEVIEW_FONT,
                       borderwidth=0)
        
        style.configure("minimal.Treeview.Heading",
                       font=Fuentes.TREEVIEW_HEADING_FONT,
                       background=Colores.TREEVIEW_HEADING,
                       foreground="#222",
                       borderwidth=0)
        
        style.layout("minimal.Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        style.map("minimal.Treeview",
                 background=[('selected', Colores.TREEVIEW_SELECCION)])
        style.map("minimal.Treeview.Heading",
                 background=[('active', Colores.TREEVIEW_HEADING_HOVER)])
    
    @staticmethod
    def configurar_treeview_producto(style):
        """Configura el estilo product para Treeview"""
        style.configure("product.Treeview",
                       background=Colores.TREEVIEW_FONDO,
                       foreground="#222",
                       rowheight=24,
                       fieldbackground=Colores.TREEVIEW_FONDO,
                       font=Fuentes.TREEVIEW_FONT,
                       borderwidth=0)
        
        style.configure("product.Treeview.Heading",
                       font=Fuentes.TREEVIEW_HEADING_FONT,
                       background=Colores.TREEVIEW_HEADING,
                       foreground="#222",
                       borderwidth=0)
        
        style.layout("product.Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        style.map("product.Treeview",
                 background=[('selected', Colores.TREEVIEW_SELECCION)])
        style.map("product.Treeview.Heading",
                 background=[('active', Colores.TREEVIEW_HEADING_HOVER)])


# Configuraciones de widgets específicos para el módulo de ventas
class EstilosVentas:
    """Configuraciones específicas para el módulo de ventas"""
    
    @staticmethod
    def crear_label_titulo(parent, texto):
        """Crea un label de título para el módulo de ventas"""
        return tk.Label(parent, text=texto, 
                       font=Fuentes.TITULO_MODULO, 
                       bg=Colores.FONDO_VENTAS, 
                       fg=Colores.TEXTO_OSCURO)
    
    @staticmethod
    def crear_label_campo(parent, texto):
        """Crea un label para campos de entrada"""
        return tk.Label(parent, text=texto, 
                       font=Fuentes.TEXTO_CAMPO_BOLD, 
                       bg=Colores.FONDO_VENTAS, 
                       fg=Colores.TEXTO_OSCURO)
    
    @staticmethod
    def crear_entry_campo(parent, width=35, readonly=False):
        """Crea un entry para campos de entrada"""
        state = "readonly" if readonly else "normal"
        return tk.Entry(parent, width=width, state=state,
                       font=Fuentes.TEXTO_CAMPO, 
                       relief='solid', bd=1)
    
    @staticmethod
    def crear_labelframe(parent, texto):
        """Crea un LabelFrame con estilo consistente"""
        return tk.LabelFrame(parent, text=texto, 
                           font=Fuentes.TEXTO_LABEL, 
                           bg=Colores.FONDO_VENTAS, 
                           fg=Colores.TEXTO_SECUNDARIO, 
                           relief='groove', bd=2)
    
    @staticmethod
    def crear_frame(parent):
        """Crea un Frame con fondo consistente"""
        return tk.Frame(parent, bg=Colores.FONDO_VENTAS)
    
    @staticmethod
    def configurar_filas_alternadas(tree):
        """Configura las filas alternadas del Treeview"""
        tree.tag_configure('oddrow', background=Colores.FILAS_IMPAR)
        tree.tag_configure('evenrow', background=Colores.FILAS_PAR)


def crear_menu_estandarizado(parent_frame, titulo_menu, titulo_seccion, botones_config, callback_volver, info_texto="💡 Información del menú"):
    """
    Crea un menú estandarizado con recuadro negro y disposición de botones consistente.
    
    Args:
        parent_frame: Frame padre donde se creará el menú
        titulo_menu (str): Título principal del menú (ej: "📊 MENÚ DE REPORTES")
        titulo_seccion (str): Título de la sección (ej: "📋 Selecciona un Reporte:")
        botones_config (list): Lista de diccionarios con configuración de botones:
            [
                {
                    'texto': 'TEXTO DEL BOTÓN',
                    'comando': funcion_callback,
                    'imagen': imagen_tk_opcional,
                    'fila': 0,
                    'columna': 0,
                    'columnspan': 1  # opcional, por defecto 1
                },
                ...
            ]
        callback_volver: Función para el botón "Volver al Menú Principal"
        info_texto (str): Texto informativo en la parte inferior
    
    Returns:
        tuple: (main_frame, grid_frame) para referencia si se necesita
    
    Ejemplo de uso:
        botones = [
            {'texto': 'REPORTE DE\\nVENTAS', 'comando': abrir_ventas, 'imagen': img_ventas, 'fila': 0, 'columna': 0},
            {'texto': 'HISTORIAL', 'comando': abrir_historial, 'imagen': img_historial, 'fila': 0, 'columna': 1},
            {'texto': 'INVENTARIO', 'comando': abrir_inventario, 'imagen': img_inventario, 'fila': 1, 'columna': 0, 'columnspan': 2}
        ]
        crear_menu_estandarizado(parent_frame, "📊 MENÚ DE REPORTES", "📋 Selecciona un Reporte:", 
                                botones, callback_volver, "💡 Genera reportes detallados")
    """
    # Configurar estilos centralizados
    configurar_estilos_aplicacion()
    
    # Frame principal con fondo personalizado
    main_frame = tk.Frame(parent_frame, bg='#ecf0f1')
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver FUERA del recuadro
    header_frame = tk.Frame(main_frame, bg='#ecf0f1')
    header_frame.pack(fill="x", pady=(0, 30))
    
    # Botón volver (estilo estándar)
    btn_volver = tk.Button(header_frame, text="← Volver al Menú Principal", 
                          command=callback_volver,
                          bg='#357ab8', fg='white', font=("Arial", 10, "bold"),
                          relief='raised', bd=2, cursor='hand2')
    btn_volver.pack(side="left")
    
    # Título del menú
    titulo = tk.Label(header_frame, text=titulo_menu, 
                     font=("Arial", 16, "bold"), fg="#2c3e50", bg='#ecf0f1')
    titulo.pack(side="right")
    
    # Frame contenedor con recuadro negro
    frame_contenedor = tk.Frame(main_frame, bg='#ecf0f1', pady=20)
    frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
    
    # Frame con borde negro (recuadro)
    frame_recuadro = tk.Frame(frame_contenedor, bg='#2c3e50', bd=1, relief="solid")
    frame_recuadro.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Frame interior con fondo claro
    frame_interior = tk.Frame(frame_recuadro, bg='#f8f9fa', bd=0)
    frame_interior.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Frame centrado para los botones dentro del recuadro
    frame_centrado = tk.Frame(frame_interior, bg='#f8f9fa')
    frame_centrado.pack(expand=True, pady=20)
    
    # Título de la sección
    titulo_seccion_label = tk.Label(frame_centrado, text=titulo_seccion, 
                                   font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#2c3e50")
    titulo_seccion_label.pack(pady=(0, 20))
    
    # Frame interno para organizar botones en grid
    grid_frame = tk.Frame(frame_centrado, bg="#f8f9fa")
    grid_frame.pack(expand=True)
    
    # Cargar imágenes de fondo para los botones (normal y hover)
    try:
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagen_fondo_normal_path = os.path.join(base_path, "Img", "Buttons", "cuadrado1.png")
        imagen_fondo_hover_path = os.path.join(base_path, "Img", "Buttons", "cuadrado2.png")
        
        # Cargar y redimensionar las imágenes de fondo (normal y hover) - tamaño optimizado
        imagen_fondo_normal_pil = Image.open(imagen_fondo_normal_path)
        imagen_fondo_normal_pil = imagen_fondo_normal_pil.resize((260, 210), Image.Resampling.LANCZOS)
        imagen_fondo_normal_tk = ImageTk.PhotoImage(imagen_fondo_normal_pil)
        
        imagen_fondo_hover_pil = Image.open(imagen_fondo_hover_path)
        imagen_fondo_hover_pil = imagen_fondo_hover_pil.resize((260, 210), Image.Resampling.LANCZOS)
        imagen_fondo_hover_tk = ImageTk.PhotoImage(imagen_fondo_hover_pil)
        
        imagen_fondo_tk = imagen_fondo_normal_tk  # Por compatibilidad con código existente
    except Exception as e:
        print(f"Error cargando imágenes de fondo: {e}")
        imagen_fondo_normal_tk = None
        imagen_fondo_hover_tk = None
        imagen_fondo_tk = None
    
    # Crear botones según configuración
    max_fila = 0
    max_columna = 0
    
    for boton_config in botones_config:
        texto = boton_config['texto']
        comando = boton_config['comando']
        imagen = boton_config.get('imagen')
        fila = boton_config['fila']
        columna = boton_config['columna']
        columnspan = boton_config.get('columnspan', 1)
        
        # Actualizar máximos para configurar el grid
        max_fila = max(max_fila, fila)
        max_columna = max(max_columna, columna)
        
        # Función para crear efecto hover
        def crear_efecto_hover(canvas_obj, imagen_normal, imagen_hover, icono_img, texto_btn, x_centro, y_centro, x_icono, y_icono, x_texto, y_texto):
            def on_enter(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_hover)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="white", 
                                     font=("Arial", 12, "bold"), justify=tk.CENTER)
            
            def on_leave(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_normal)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="white", 
                                     font=("Arial", 12, "bold"), justify=tk.CENTER)
            
            canvas_obj.bind("<Enter>", on_enter)
            canvas_obj.bind("<Leave>", on_leave)
        
        # Crear botón con imagen de fondo personalizada e ícono superpuesto
        if imagen_fondo_normal_tk and imagen_fondo_hover_tk:
            # Usar Canvas directo para superponer imágenes
            canvas = tk.Canvas(grid_frame, width=260, height=210, highlightthickness=0, 
                             bd=0, relief="flat", bg="#f8f9fa")
            
            # Dibujar estado inicial (normal)
            canvas.create_image(130, 105, image=imagen_fondo_normal_tk)
            if imagen:
                # Dibujar ícono más centrado
                canvas.create_image(130, 85, image=imagen)
                # Dibujar texto un poco más abajo
                canvas.create_text(130, 160, text=texto, fill="white", 
                                 font=("Arial", 12, "bold"), justify=tk.CENTER)
            else:
                # Dibujar texto centrado
                canvas.create_text(130, 105, text=texto, fill="white", 
                                 font=("Arial", 14, "bold"), justify=tk.CENTER)
            
            # Aplicar efecto hover
            if imagen:
                crear_efecto_hover(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
                                 imagen, texto, 130, 105, 130, 85, 130, 160)
            else:
                crear_efecto_hover(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
                                 None, texto, 130, 105, 130, 105, 130, 105)
            
            # Hacer clickeable (con closure correcto)
            canvas.bind("<Button-1>", lambda e, cmd=comando: cmd())
            canvas.configure(cursor='hand2')
            
            # Usar canvas directamente
            boton = canvas
            boton.imagen_fondo_normal = imagen_fondo_normal_tk
            boton.imagen_fondo_hover = imagen_fondo_hover_tk
            if imagen:
                boton.imagen_icono = imagen
        else:
            # Fallback si no se puede cargar la imagen de fondo
            if imagen:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("Arial", 13, "bold"),
                                 relief='raised', bd=2, cursor='hand2',
                                 image=imagen, compound=tk.TOP,
                                 width=260, height=210)
                boton.image = imagen
            else:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("Arial", 15, "bold"),
                                 relief='raised', bd=2, cursor='hand2',
                                 width=260, height=210)
        
        # Aplicar medidas reducidas para mejor distribución
        boton.grid(row=fila, column=columna, columnspan=columnspan,
                  padx=10, pady=10, sticky="nsew", ipadx=0, ipady=0)
    
    # Configurar peso de las celdas del grid para expansión uniforme
    # Asegurar que todas las filas y columnas tengan peso uniforme con altura más flexible
    for fila in range(max_fila + 1):
        grid_frame.grid_rowconfigure(fila, weight=1, minsize=100)  # Altura mínima más flexible
    
    # Para columnas, considerar el máximo entre columnas individuales y columnspan
    max_columnas_reales = max_columna + 1
    for boton_config in botones_config:
        columna = boton_config['columna']
        columnspan = boton_config.get('columnspan', 1)
        max_columnas_reales = max(max_columnas_reales, columna + columnspan)
    
    for columna in range(max_columnas_reales):
        grid_frame.grid_columnconfigure(columna, weight=1)
    
    # Información adicional
    info_frame = tk.Frame(frame_interior, bg="#f8f9fa")
    info_frame.pack(side="bottom", pady=(20, 15))
    
    info_label = tk.Label(info_frame, text=info_texto,
                         font=("Arial", 10), bg="#f8f9fa", fg="#7f8c8d")
    info_label.pack()
    
    return main_frame, grid_frame


def crear_recuadro_estandarizado(parent_frame, titulo_pantalla, callback_volver=None):
    """
    Crea el recuadro negro estándar reutilizable para cualquier pantalla.
    
    Args:
        parent_frame: Frame padre donde se creará el recuadro
        titulo_pantalla (str): Título de la pantalla (ej: "📊 MÓDULO DE VENTAS")
        callback_volver (function, optional): Función para el botón "Volver al Menú Principal"
    
    Returns:
        tuple: (main_frame, frame_centrado) donde:
            - main_frame: Frame principal con fondo gris
            - frame_centrado: Frame interior donde agregar el contenido de la pantalla
    
    Ejemplo de uso:
        main_frame, contenido_frame = crear_recuadro_estandarizado(
            parent_frame, "📊 MÓDULO DE VENTAS", callback_volver
        )
        # Agregar contenido específico al contenido_frame
        mi_label = tk.Label(contenido_frame, text="Mi contenido", bg='#f8f9fa')
        mi_label.pack()
    """
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Frame principal con fondo personalizado (como en crear_menu_estandarizado)
    main_frame = tk.Frame(parent_frame, bg='#ecf0f1')
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver FUERA del recuadro (solo si se proporciona callback)
    if callback_volver:
        header_frame = tk.Frame(main_frame, bg='#ecf0f1')
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Botón volver (estilo estándar)
        btn_volver = tk.Button(header_frame, text="← Volver al Menú Principal", 
                              command=callback_volver,
                              bg='#357ab8', fg='white', font=("Arial", 10, "bold"),
                              relief='raised', bd=2, cursor='hand2')
        btn_volver.pack(side="left")
        
        # Título del menú
        titulo = tk.Label(header_frame, text=titulo_pantalla, 
                         font=("Arial", 16, "bold"), fg="#2c3e50", bg='#ecf0f1')
        titulo.pack(side="right")
    else:
        # Solo título centrado sin botón volver
        titulo = tk.Label(main_frame, text=titulo_pantalla, 
                         font=("Arial", 16, "bold"), fg="#2c3e50", bg='#ecf0f1')
        titulo.pack(pady=(0, 30))
    
    # Frame contenedor con recuadro negro
    frame_contenedor = tk.Frame(main_frame, bg='#ecf0f1', pady=20)
    frame_contenedor.pack(expand=True, fill="both", padx=50, pady=20)
    
    # Frame con borde negro (recuadro)
    frame_recuadro = tk.Frame(frame_contenedor, bg='#2c3e50', bd=1, relief="solid")
    frame_recuadro.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Frame interior con fondo claro
    frame_interior = tk.Frame(frame_recuadro, bg='#f8f9fa', bd=0)
    frame_interior.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Frame centrado para el contenido dentro del recuadro
    frame_centrado = tk.Frame(frame_interior, bg='#f8f9fa')
    frame_centrado.pack(expand=True, fill="both", pady=20, padx=20)
    
    return main_frame, frame_centrado

def crear_menu_principal_estandarizado(parent_frame, titulo_seccion, botones_config):
    """
    Crear menú principal usando btnblanco250.png como fondo de botones.
    
    Parámetros:
    - parent_frame: Frame contenedor donde se creará el menú
    - titulo_seccion: Título de la sección del menú
    - botones_config: Lista de diccionarios con configuración de botones:
      [{'texto': 'NOMBRE', 'comando': funcion, 'imagen': imagen_tk, 'fila': 0, 'columna': 0, 'columnspan': 1}]
    """
    from PIL import Image, ImageTk
    
    # Frame contenedor principal con estilo profesional
    main_frame = tk.Frame(parent_frame, bg='#ecf0f1')
    main_frame.pack(expand=True, fill="both", padx=50, pady=20)
    
    # Frame con borde negro (recuadro)
    frame_recuadro = tk.Frame(main_frame, bg='#2c3e50', bd=1, relief="solid")
    frame_recuadro.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Frame interior con fondo claro
    frame_interior = tk.Frame(frame_recuadro, bg='#f8f9fa', bd=0)
    frame_interior.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Frame centrado para los botones dentro del recuadro
    frame_centrado = tk.Frame(frame_interior, bg='#f8f9fa')
    frame_centrado.pack(expand=True, pady=20)
    
    # Título de la sección
    titulo_seccion_label = tk.Label(frame_centrado, text=titulo_seccion, 
                                   font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#2c3e50")
    titulo_seccion_label.pack(pady=(0, 20))
    
    # Frame interno para organizar botones en grid
    grid_frame = tk.Frame(frame_centrado, bg="#f8f9fa")
    grid_frame.pack(expand=True)
    
    # Cargar imágenes de fondo para los botones (normal y hover)
    try:
        # Obtener la ruta base del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagen_fondo_normal_path = os.path.join(base_path, "Img", "Buttons", "btnblanco250.png")
        imagen_fondo_hover_path = os.path.join(base_path, "Img", "Buttons", "btnblanco2250.png")  # Imagen para hover
        
        # Cargar y redimensionar las imágenes de fondo (normal y hover)
        imagen_fondo_normal_pil = Image.open(imagen_fondo_normal_path)
        imagen_fondo_normal_pil = imagen_fondo_normal_pil.resize((260, 210), Image.Resampling.LANCZOS)
        imagen_fondo_normal_tk = ImageTk.PhotoImage(imagen_fondo_normal_pil)
        
        # Imagen para hover usando btnblanco2250.png
        imagen_fondo_hover_pil = Image.open(imagen_fondo_hover_path)
        imagen_fondo_hover_pil = imagen_fondo_hover_pil.resize((260, 210), Image.Resampling.LANCZOS)
        imagen_fondo_hover_tk = ImageTk.PhotoImage(imagen_fondo_hover_pil)
        
        imagen_fondo_tk = imagen_fondo_normal_tk  # Por compatibilidad con código existente
    except Exception as e:
        print(f"Error cargando imágenes de fondo: {e}")
        imagen_fondo_normal_tk = None
        imagen_fondo_hover_tk = None
        imagen_fondo_tk = None
    
    # Crear botones según configuración
    max_fila = 0
    max_columna = 0
    
    for boton_config in botones_config:
        texto = boton_config['texto']
        comando = boton_config['comando']
        imagen = boton_config.get('imagen')
        fila = boton_config['fila']
        columna = boton_config['columna']
        columnspan = boton_config.get('columnspan', 1)
        
        # Actualizar máximos para configurar el grid
        max_fila = max(max_fila, fila)
        max_columna = max(max_columna, columna)
        
        # Función para crear efecto hover
        def crear_efecto_hover(canvas_obj, imagen_normal, imagen_hover, icono_img, texto_btn, x_centro, y_centro, x_icono, y_icono, x_texto, y_texto):
            def on_enter(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_hover)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="#2c3e50", 
                                     font=("Arial", 12, "bold"), justify=tk.CENTER)
            
            def on_leave(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_normal)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="#2c3e50", 
                                     font=("Arial", 12, "bold"), justify=tk.CENTER)
            
            canvas_obj.bind("<Enter>", on_enter)
            canvas_obj.bind("<Leave>", on_leave)
        
        # Crear botón con imagen de fondo personalizada e ícono superpuesto
        if imagen_fondo_normal_tk and imagen_fondo_hover_tk:
            # Usar Canvas directo para superponer imágenes
            canvas = tk.Canvas(grid_frame, width=260, height=210, highlightthickness=0, 
                             bd=0, relief="flat", bg="#f8f9fa")
            
            # Dibujar estado inicial (normal)
            canvas.create_image(130, 105, image=imagen_fondo_normal_tk)
            if imagen:
                # Dibujar ícono más centrado
                canvas.create_image(130, 85, image=imagen)
                # Dibujar texto un poco más abajo
                canvas.create_text(130, 160, text=texto, fill="#2c3e50", 
                                 font=("Arial", 12, "bold"), justify=tk.CENTER)
            else:
                # Dibujar texto centrado
                canvas.create_text(130, 105, text=texto, fill="#2c3e50", 
                                 font=("Arial", 14, "bold"), justify=tk.CENTER)
            
            # Aplicar efecto hover
            if imagen:
                crear_efecto_hover(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
                                 imagen, texto, 130, 105, 130, 85, 130, 160)
            else:
                crear_efecto_hover(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
                                 None, texto, 130, 105, 130, 105, 130, 105)
            
            # Hacer clickeable (con closure correcto)
            canvas.bind("<Button-1>", lambda e, cmd=comando: cmd())
            canvas.configure(cursor='hand2')
            
            # Usar canvas directamente
            boton = canvas
            boton.imagen_fondo_normal = imagen_fondo_normal_tk
            boton.imagen_fondo_hover = imagen_fondo_hover_tk
            if imagen:
                boton.imagen_icono = imagen
        else:
            # Fallback si no se puede cargar la imagen de fondo
            if imagen:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("Arial", 13, "bold"),
                                 relief='raised', bd=2, cursor='hand2',
                                 image=imagen, compound=tk.TOP,
                                 width=260, height=210)
                boton.image = imagen
            else:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("Arial", 15, "bold"),
                                 relief='raised', bd=2, cursor='hand2',
                                 width=260, height=210)
        
        # Aplicar medidas reducidas para mejor distribución
        boton.grid(row=fila, column=columna, columnspan=columnspan,
                  padx=10, pady=10, sticky="nsew", ipadx=0, ipady=0)
    
    # Configurar expansión del grid
    for col in range(max_columna + 1):
        grid_frame.grid_columnconfigure(col, weight=1)
    for row in range(max_fila + 1):
        grid_frame.grid_rowconfigure(row, weight=1)
    
    return main_frame, grid_frame
