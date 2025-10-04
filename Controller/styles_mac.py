"""
Estilos específicos para macOS - Sistema de Manejo de Ventas S&M
Este archivo contiene configuraciones de estilos optimizadas para macOS
donde tk.Button no respeta colores de fondo correctamente.
"""

import tkinter as tk
from tkinter import ttk
import platform

def es_macos():
    """Detectar si estamos ejecutando en macOS"""
    return platform.system() == 'Darwin'

def configurar_estilos_macos():
    """
    Configurar estilos ttk específicos para macOS que sí respetan colores
    """
    style = ttk.Style()
    
    # Usar un tema base que funcione bien sin bordes en macOS
    try:
        style.theme_use('clam')  # Tema más limpio que 'aqua'
    except:
        style.theme_use('default')  # Fallback
    
    # =========================================================================
    # CONFIGURACIÓN BASE PARA ELIMINAR BORDES COMPLETAMENTE
    # =========================================================================
    
    # Configurar el estilo base TButton para eliminar todos los bordes por defecto
    style.configure("TButton",
                   borderwidth=0,
                   relief='flat',
                   highlightthickness=0,
                   focuscolor='none')
    
    style.map("TButton",
             borderwidth=[('active', 0), ('pressed', 0)],
             relief=[('active', 'flat'), ('pressed', 'flat')],
             highlightthickness=[('active', 0), ('pressed', 0)])
    
    # =========================================================================
    # ESTILOS PARA BOTONES DE VENTAS - MACROS COMPATIBLES
    # =========================================================================
    
    # Botón Agregar (Verde) - Sin bordes problemáticos
    style.configure("MacAgregar.TButton",
                   background='#27ae60',
                   foreground='black',
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(20, 8))
    
    style.map("MacAgregar.TButton",
             background=[('active', '#229954'),
                        ('pressed', '#1e8449')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón Cancelar (Rojo) - Sin bordes problemáticos
    style.configure("MacCancelar.TButton",
                   background='#e74c3c',
                   foreground='black',
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(20, 8))
    
    style.map("MacCancelar.TButton",
             background=[('active', '#c0392b'),
                        ('pressed', '#a93226')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón Eliminar (Rojo) - Sin bordes problemáticos
    style.configure("MacEliminar.TButton",
                   background='#e74c3c',
                   foreground='black',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 5))
    
    style.map("MacEliminar.TButton",
             background=[('active', '#c0392b'),
                        ('pressed', '#a93226')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón Modificar (Azul) - Sin bordes problemáticos
    style.configure("MacModificar.TButton",
                   background='#2980b9',
                   foreground='black',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 5))
    
    style.map("MacModificar.TButton",
             background=[('active', '#1f618d'),
                        ('pressed', '#1b4f72')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón Limpiar (Gris) - Sin bordes problemáticos
    style.configure("MacLimpiar.TButton",
                   background='#95a5a6',
                   foreground='black',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 5))
    
    style.map("MacLimpiar.TButton",
             background=[('active', '#7f8c8d'),
                        ('pressed', '#6c7b7d')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón Finalizar (Verde grande) - Sin bordes problemáticos
    style.configure("MacFinalizar.TButton",
                   background='#27ae60',
                   foreground='black',
                   font=('SF Pro Display', 13, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(30, 12))
    
    style.map("MacFinalizar.TButton",
             background=[('active', '#229954'),
                        ('pressed', '#1e8449')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # =========================================================================
    # ESTILOS PARA BOTONES DE MENÚ PRINCIPAL
    # =========================================================================
    
    # Cargar imagen de fondo para botones del menú principal en macOS
    try:
        from PIL import Image, ImageTk
        # Cargar imagen de fondo desde la carpeta Buttons
        btn_bg_image = Image.open('Img/Buttons/btnblanco250.png')
        btn_bg_photo = ImageTk.PhotoImage(btn_bg_image)
        
        # Almacenar la imagen en el style para evitar que se elimine por garbage collector
        style._btn_bg_image = btn_bg_photo
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo en macOS: {e}")
        btn_bg_photo = None
    
    # Botón Ventas - Con imagen de fondo
    style.configure("MacVentas.TButton",
                   foreground='#2c3e50',  # Texto oscuro para contrastar
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacVentas.TButton",
             foreground=[('active', '#1f618d'),
                        ('pressed', '#154360')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Reportes - Con imagen de fondo
    style.configure("MacReportes.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacReportes.TButton",
             foreground=[('active', '#a93226'),
                        ('pressed', '#922b21')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Ajustes - Con imagen de fondo
    style.configure("MacAjustes.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacAjustes.TButton",
             foreground=[('active', '#d68910'),
                        ('pressed', '#b7950b')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Inventario - Con imagen de fondo
    style.configure("MacInventario.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacInventario.TButton",
             foreground=[('active', '#1e8449'),
                        ('pressed', '#186a3b')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Clientes - Con imagen de fondo
    style.configure("MacClientes.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacClientes.TButton",
             foreground=[('active', '#7d3c98'),
                        ('pressed', '#6c3483')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Precios - Con imagen de fondo
    style.configure("MacPrecios.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacPrecios.TButton",
             foreground=[('active', '#d68910'),
                        ('pressed', '#b7950b')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Salir - Con imagen de fondo
    style.configure("MacSalir.TButton",
                   foreground='#2c3e50',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacSalir.TButton",
             foreground=[('active', '#424949'),
                        ('pressed', '#2e4053')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # =========================================================================
    # ESTILOS PARA BOTONES DE REPORTES
    # =========================================================================
    
    # Botón Volver - Sin bordes problemáticos
    style.configure("MacVolver.TButton",
                   background='#34495e',
                   foreground='white',  # Mantenemos blanco para botones oscuros
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 8))
    
    style.map("MacVolver.TButton",
             background=[('active', '#2c3e50'),
                        ('pressed', '#1b2631')],
             foreground=[('active', 'white'),  # Blanco en fondos oscuros
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botones de reporte - Sin bordes problemáticos
    style.configure("MacReporte.TButton",
                   background='#2980b9',
                   foreground='black',
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(20, 10))
    
    style.map("MacReporte.TButton",
             background=[('active', '#1f618d'),
                        ('pressed', '#1b4f72')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # =========================================================================
    # ESTILOS ADICIONALES
    # =========================================================================
    
    # Botones de acción elegantes - Sin bordes problemáticos
    style.configure("MacElegante.TButton",
                   background='#2c3e50',
                   foreground='white',  # Mantenemos blanco para botones oscuros
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(15, 8))
    
    style.map("MacElegante.TButton",
             background=[('active', '#34495e'),
                        ('pressed', '#1b2631')],
             foreground=[('active', 'white'),  # Blanco en fondos oscuros
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # =========================================================================
    # ESTILOS ESPECÍFICOS PARA SALES.PY - SIN BORDES
    # =========================================================================
    
    # Estilos adicionales para botones multiplataforma
    style.configure("MacAgregarSales.TButton",
                   background='#27ae60',
                   foreground='black',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   focuscolor='none',
                   padding=(20, 8))
    
    style.map("MacAgregarSales.TButton",
             background=[('active', '#229954')],
             foreground=[('active', 'black')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])
    
    style.configure("MacCancelarSales.TButton",
                   background='#e74c3c',
                   foreground='black',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,
                   relief='flat',
                   focuscolor='none',
                   padding=(20, 8))
    
    style.map("MacCancelarSales.TButton",
             background=[('active', '#c0392b')],
             foreground=[('active', 'black')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])
    
    # =========================================================================
    # ESTILOS PARA MENÚ DE CONFIGURACIONES - SIN BORDES PROBLEMÁTICOS
    # =========================================================================
    
    # Botones de configuración principales (Email, Logo, Apariencia, Teléfono)
    style.configure("MacConfig.TButton",
                   background='#3498db',  # Azul claro profesional
                   foreground='white',
                   font=('SF Pro Display', 12, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(30, 25))
    
    style.map("MacConfig.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#2471a3')],
             foreground=[('active', 'white'),
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Variante para popup de configuraciones
    style.configure("MacConfigPopup.TButton",
                   background='#3498db',  # Azul claro profesional
                   foreground='white',
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(30, 25))
    
    style.map("MacConfigPopup.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#2471a3')],
             foreground=[('active', 'white'),
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón de volver específico para configuraciones
    style.configure("MacVolverConfig.TButton",
                   background='#357ab8',  # Azul medio
                   foreground='white',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 8))
    
    style.map("MacVolverConfig.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#1f618d')],
             foreground=[('active', 'white'),
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # =========================================================================
    # ESTILOS PARA MENÚ DE REPORTES - SIN BORDES PROBLEMÁTICOS
    # =========================================================================
    
    # Botones de reporte principales (Reporte de Ventas, Historial, Inventario)
    style.configure("MacReportMenu.TButton",
                   background='#3498db',  # Mismo azul que configuraciones
                   foreground='white',
                   font=('SF Pro Display', 12, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(50, 30))
    
    style.map("MacReportMenu.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#2471a3')],
             foreground=[('active', 'white'),
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    # Botón de volver específico para reportes
    style.configure("MacVolverReport.TButton",
                   background='#357ab8',  # Mismo azul que configuraciones
                   foreground='white',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 8))
    
    style.map("MacVolverReport.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#1f618d')],
             foreground=[('active', 'white'),
                        ('pressed', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0)])
    
    return style

def crear_boton_macos(parent, text, command, estilo, **kwargs):
    """
    Crear un botón optimizado para macOS usando ttk.Button
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        estilo: Nombre del estilo (ej: "MacAgregar.TButton")
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón configurado para macOS
    """
    return ttk.Button(parent, text=text, command=command, style=estilo, cursor='hand2', **kwargs)

def crear_boton_sales_macos(parent, text, command, tipo_boton="agregar"):
    """
    Crear botones específicos para la interfaz de Sales.py sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        tipo_boton: Tipo de botón ("agregar", "cancelar", "eliminar", "modificar", "limpiar", "finalizar")
    
    Returns:
        ttk.Button: Botón configurado específicamente para Sales.py
    """
    estilos_map = {
        "agregar": "MacAgregar.TButton",
        "cancelar": "MacCancelar.TButton", 
        "eliminar": "MacEliminar.TButton",
        "modificar": "MacModificar.TButton",
        "limpiar": "MacLimpiar.TButton",
        "finalizar": "MacFinalizar.TButton"
    }
    
    estilo = estilos_map.get(tipo_boton, "MacAgregar.TButton")
    
    # Crear el botón con configuraciones adicionales para eliminar bordes
    boton = ttk.Button(parent, text=text, command=command, style=estilo, cursor='hand2')
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

def crear_boton_config_macos(parent, text, command, is_popup=False, **kwargs):
    """
    Crear botones específicos para el menú de configuraciones sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        is_popup: Si es True, usa estilo para popup, si es False para frame integrado
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón configurado específicamente para configuraciones
    """
    estilo = "MacConfigPopup.TButton" if is_popup else "MacConfig.TButton"
    
    # Crear el botón con configuraciones adicionales para eliminar bordes
    boton = ttk.Button(parent, text=text, command=command, style=estilo, cursor='hand2', **kwargs)
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

def crear_boton_volver_config_macos(parent, text, command, **kwargs):
    """
    Crear botón de volver específico para configuraciones sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón de volver configurado específicamente para configuraciones
    """
    # Crear el botón con configuraciones adicionales para eliminar bordes
    boton = ttk.Button(parent, text=text, command=command, style="MacVolverConfig.TButton", cursor='hand2', **kwargs)
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

def crear_boton_report_macos(parent, text, command, image=None, **kwargs):
    """
    Crear botones específicos para el menú de reportes sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        image: Imagen del botón (opcional)
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón configurado específicamente para reportes
    """
    # Crear el botón con configuraciones adicionales para eliminar bordes
    if image:
        boton = ttk.Button(parent, text=text, command=command, style="MacReportMenu.TButton", 
                          cursor='hand2', image=image, compound=tk.TOP, **kwargs)
        boton.image = image  # Mantener referencia de la imagen
    else:
        boton = ttk.Button(parent, text=text, command=command, style="MacReportMenu.TButton", 
                          cursor='hand2', **kwargs)
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

def crear_boton_volver_report_macos(parent, text, command, **kwargs):
    """
    Crear botón de volver específico para reportes sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón de volver configurado específicamente para reportes
    """
    # Crear el botón con configuraciones adicionales para eliminar bordes
    boton = ttk.Button(parent, text=text, command=command, style="MacVolverReport.TButton", 
                      cursor='hand2', **kwargs)
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

def crear_boton_email_macos(parent, text, command, tipo_boton="guardar", **kwargs):
    """
    Crear botones específicos para el módulo de email sin bordes problemáticos
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        tipo_boton: Tipo de botón ("guardar", "cancelar", "volver")
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        ttk.Button: Botón configurado específicamente para email
    """
    estilos_map = {
        "guardar": "MacEmailGuardar.TButton",
        "cancelar": "MacEmailCancelar.TButton", 
        "volver": "MacEmailVolver.TButton"
    }
    
    estilo = estilos_map.get(tipo_boton, "MacEmailGuardar.TButton")
    
    # Crear el botón con configuraciones adicionales para eliminar bordes
    boton = ttk.Button(parent, text=text, command=command, style=estilo, cursor='hand2', **kwargs)
    
    # Configuraciones adicionales para eliminar completamente los bordes en macOS
    try:
        boton.configure(takefocus=False)  # Eliminar el foco que puede causar bordes
    except:
        pass
    
    return boton

# =========================================================================
# COLORES Y CONSTANTES PARA MACOS
# =========================================================================

class ColoresMac:
    """Paleta de colores optimizada para macOS"""
    VERDE_PRINCIPAL = '#27ae60'
    VERDE_HOVER = '#229954'
    VERDE_PRESSED = '#1e8449'
    
    ROJO_PRINCIPAL = '#e74c3c'
    ROJO_HOVER = '#c0392b'
    ROJO_PRESSED = '#a93226'
    
    AZUL_PRINCIPAL = '#2980b9'
    AZUL_HOVER = '#1f618d'
    AZUL_PRESSED = '#1b4f72'
    
    GRIS_PRINCIPAL = '#95a5a6'
    GRIS_HOVER = '#7f8c8d'
    GRIS_PRESSED = '#6c7b7d'
    
    NARANJA_PRINCIPAL = '#f39c12'
    NARANJA_HOVER = '#e67e22'
    NARANJA_PRESSED = '#d68910'
    
    AZUL_CLARO = '#3498db'
    AZUL_CLARO_HOVER = '#2980b9'
    AZUL_CLARO_PRESSED = '#2471a3'
    
    FONDO_CLARO = '#ecf0f1'
    TEXT_OSCURO = '#2c3e50'
    TEXT_CLARO = '#7f8c8d'
    BLANCO = '#ffffff'

class FuentesMac:
    """Fuentes optimizadas para macOS"""
    PRINCIPAL = ('SF Pro Display', 16, 'bold')
    SECUNDARIA = ('SF Pro Display', 13, 'bold')
    BOTON_GRANDE = ('SF Pro Display', 13, 'bold')
    BOTON_NORMAL = ('SF Pro Display', 11, 'bold')
    BOTON_PEQUEÑO = ('SF Pro Display', 10, 'bold')
    TEXTO_NORMAL = ('SF Pro Display', 11)
    TEXTO_PEQUEÑO = ('SF Pro Display', 10)

# =========================================================================
# FUNCIÓN PRINCIPAL DE CONFIGURACIÓN
# =========================================================================

def configurar_app_para_macos():
    """
    Función principal para configurar toda la aplicación para macOS
    Debe ser llamada al inicio de la aplicación si se detecta macOS
    """
    if es_macos():
        style = configurar_estilos_macos()
        print("✅ Estilos de macOS configurados correctamente")
        return style
    else:
        print("⚠️  No es macOS, usar estilos estándar")
        return None

# =========================================================================
# EJEMPLOS DE USO
# =========================================================================

    # =========================================================================
    # ESTILOS PARA MÓDULO DE EMAIL - SIN BORDES PROBLEMÁTICOS
    # =========================================================================
    
    # Botón Guardar Email (Verde) - Sin bordes problemáticos
    style.configure("MacEmailGuardar.TButton",
                   background='#27ae60',
                   foreground='white',
                   font=('SF Pro Display', 11, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(20, 10),
                   insertcolor='white',  # Para modo oscuro
                   selectbackground='#27ae60',
                   selectforeground='white')
    
    style.map("MacEmailGuardar.TButton",
             background=[('active', '#229954'),
                        ('pressed', '#1e8449'),
                        ('focus', '#27ae60')],
             foreground=[('active', 'white'),
                        ('pressed', 'white'),
                        ('focus', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat'),
                    ('focus', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0),
                         ('focus', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0),
                                ('focus', 0)])
    
    # Botón Cancelar Email (Gris) - Sin bordes problemáticos
    style.configure("MacEmailCancelar.TButton",
                   background='#95a5a6',
                   foreground='white',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 5),
                   insertcolor='white',  # Para modo oscuro
                   selectbackground='#95a5a6',
                   selectforeground='white')
    
    style.map("MacEmailCancelar.TButton",
             background=[('active', '#7f8c8d'),
                        ('pressed', '#6c7b7d'),
                        ('focus', '#95a5a6')],
             foreground=[('active', 'white'),
                        ('pressed', 'white'),
                        ('focus', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat'),
                    ('focus', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0),
                         ('focus', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0),
                                ('focus', 0)])
    
    # Botón Volver Email (Azul) - Sin bordes problemáticos y más visible
    style.configure("MacEmailVolver.TButton",
                   background='#3498db',  # Azul más brillante y visible
                   foreground='white',
                   font=('SF Pro Display', 10, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   highlightthickness=0,  # Sin resaltado
                   padding=(15, 8),
                   insertcolor='white',  # Para modo oscuro
                   selectbackground='#3498db',
                   selectforeground='white')
    
    style.map("MacEmailVolver.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#1f618d'),
                        ('focus', '#3498db')],
             foreground=[('active', 'white'),
                        ('pressed', 'white'),
                        ('focus', 'white')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat'),
                    ('focus', 'flat')],
             borderwidth=[('active', 0),
                         ('pressed', 0),
                         ('focus', 0)],
             highlightthickness=[('active', 0),
                                ('pressed', 0),
                                ('focus', 0)])
    
    return style

def crear_boton_macos(parent, text, command, estilo, **kwargs):
    """
    Ejemplo de cómo usar los botones optimizados para macOS
    """
    # Configurar estilos
    style = configurar_estilos_macos()
    
    # Crear botones usando los estilos
    btn_agregar = crear_boton_macos(parent, "➕ Agregar", None, "MacAgregar.TButton")
    btn_cancelar = crear_boton_macos(parent, "❌ Cancelar", None, "MacCancelar.TButton")
    btn_eliminar = crear_boton_macos(parent, "🗑️ Eliminar", None, "MacEliminar.TButton")
    btn_modificar = crear_boton_macos(parent, "✏️ Modificar", None, "MacModificar.TButton")
    btn_limpiar = crear_boton_macos(parent, "🧹 Limpiar", None, "MacLimpiar.TButton")
    btn_finalizar = crear_boton_macos(parent, "✅ Finalizar", None, "MacFinalizar.TButton")
    
    return [btn_agregar, btn_cancelar, btn_eliminar, btn_modificar, btn_limpiar, btn_finalizar]

def crear_menu_principal_estandarizado_mac(parent_frame, titulo_seccion, botones_config):
    """
    Crear menú principal usando btnblanco250.png como fondo de botones y btnblanco2250.png para hover en macOS.
    
    Parámetros:
    - parent_frame: Frame contenedor donde se creará el menú
    - titulo_seccion: Título de la sección del menú
    - botones_config: Lista de diccionarios con configuración de botones:
      [{'texto': 'NOMBRE', 'comando': funcion, 'imagen': imagen_tk, 'fila': 0, 'columna': 0, 'columnspan': 1}]
    """
    from PIL import Image, ImageTk
    import tkinter as tk
    import os
    
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
                                   font=("SF Pro Display", 14, "bold"), bg="#f8f9fa", fg="#2c3e50")
    titulo_seccion_label.pack(pady=(0, 20))
    
    # Frame interno para organizar botones en grid
    grid_frame = tk.Frame(frame_centrado, bg="#f8f9fa")
    grid_frame.pack(expand=True)
    
    # Cargar imágenes de fondo para los botones (normal y hover) para macOS
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
        print(f"Error cargando imágenes de fondo para macOS: {e}")
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
        
        # Función para crear efecto hover en macOS
        def crear_efecto_hover_mac(canvas_obj, imagen_normal, imagen_hover, icono_img, texto_btn, x_centro, y_centro, x_icono, y_icono, x_texto, y_texto):
            def on_enter(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_hover)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="#2c3e50", 
                                     font=("SF Pro Display", 12, "bold"), justify=tk.CENTER)
            
            def on_leave(event):
                canvas_obj.delete("all")
                canvas_obj.create_image(x_centro, y_centro, image=imagen_normal)
                if icono_img:
                    canvas_obj.create_image(x_icono, y_icono, image=icono_img)
                canvas_obj.create_text(x_texto, y_texto, text=texto_btn, fill="#2c3e50", 
                                     font=("SF Pro Display", 12, "bold"), justify=tk.CENTER)
            
            canvas_obj.bind("<Enter>", on_enter)
            canvas_obj.bind("<Leave>", on_leave)
        
        # Crear botón con imagen de fondo personalizada e ícono superpuesto para macOS
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
                                 font=("SF Pro Display", 12, "bold"), justify=tk.CENTER)
            else:
                # Dibujar texto centrado
                canvas.create_text(130, 105, text=texto, fill="#2c3e50", 
                                 font=("SF Pro Display", 14, "bold"), justify=tk.CENTER)
            
            # Aplicar efecto hover
            if imagen:
                crear_efecto_hover_mac(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
                                     imagen, texto, 130, 105, 130, 85, 130, 160)
            else:
                crear_efecto_hover_mac(canvas, imagen_fondo_normal_tk, imagen_fondo_hover_tk, 
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
            # Fallback si no se puede cargar la imagen de fondo en macOS
            if imagen:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("SF Pro Display", 13, "bold"),
                                 relief='raised', bd=2, cursor='hand2',
                                 image=imagen, compound=tk.TOP,
                                 width=260, height=210)
                boton.image = imagen
            else:
                boton = tk.Button(grid_frame, text=texto, command=comando,
                                 bg='#3498db', fg='white', font=("SF Pro Display", 15, "bold"),
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

if __name__ == "__main__":
    # Test básico
    if es_macos():
        print("✅ Ejecutándose en macOS")
        style = configurar_estilos_macos()
        print("✅ Estilos configurados")
    else:
        print("⚠️  No es macOS")
