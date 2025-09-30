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
    
    # Botón Ventas (Azul) - Sin bordes problemáticos
    style.configure("MacVentas.TButton",
                   background='#3498db',
                   foreground='black',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacVentas.TButton",
             background=[('active', '#2980b9'),
                        ('pressed', '#2471a3')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Reportes (Rojo) - Sin bordes problemáticos
    style.configure("MacReportes.TButton",
                   background='#e74c3c',
                   foreground='black',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacReportes.TButton",
             background=[('active', '#c0392b'),
                        ('pressed', '#a93226')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Ajustes (Naranja) - Sin bordes problemáticos
    style.configure("MacAjustes.TButton",
                   background='#f39c12',
                   foreground='black',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacAjustes.TButton",
             background=[('active', '#e67e22'),
                        ('pressed', '#d68910')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Botón Salir (Gris) - Sin bordes problemáticos
    style.configure("MacSalir.TButton",
                   background='#95a5a6',
                   foreground='black',
                   font=('SF Pro Display', 16, 'bold'),
                   borderwidth=0,  # Sin borde
                   relief='flat',  # Completamente plano
                   focuscolor='none',
                   padding=(50, 50))
    
    style.map("MacSalir.TButton",
             background=[('active', '#7f8c8d'),
                        ('pressed', '#6c7b7d')],
             foreground=[('active', 'black'),
                        ('pressed', 'black')],
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

if __name__ == "__main__":
    # Test básico
    if es_macos():
        print("✅ Ejecutándose en macOS")
        style = configurar_estilos_macos()
        print("✅ Estilos configurados")
    else:
        print("⚠️  No es macOS")
