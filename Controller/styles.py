"""
Módulo de estilos centralizados para la aplicación S&M - Sistema de Manejo de Ventas
Este archivo contiene todas las configuraciones de estilos ttk para mantener consistencia visual
"""

import tkinter as tk
from tkinter import ttk


def configurar_estilos_aplicacion():
    """
    Configura todos los estilos ttk para la aplicación.
    Incluye estilos para botones principales, reportes, configuraciones, etc.
    
    Returns:
        ttk.Style: Objeto Style configurado con todos los estilos de la aplicación
    """
    style = ttk.Style()
    style.theme_use('clam')  # Tema consistente multiplataforma
    
    # =========================================================================
    # ESTILOS PARA MENÚ PRINCIPAL
    # =========================================================================
    
    # Estilo base para botones principales
    style.configure('MainButton.TButton',
                   font=('Arial', 18, 'bold'),
                   foreground='white',
                   borderwidth=3,
                   relief='raised',
                   focuscolor='none')
    
    # Estilos específicos para cada botón del menú principal
    style.configure('Ventas.TButton', 
                   background='#3498db',
                   foreground='white',
                   font=('Arial', 14, 'bold'),
                   borderwidth=2,
                   relief='raised',
                   padding=(10, 10))
    style.configure('Reportes.TButton', 
                   background='#e74c3c',
                   foreground='white',
                   font=('Arial', 14, 'bold'),
                   borderwidth=2,
                   relief='raised',
                   padding=(10, 10))
    style.configure('Ajustes.TButton', 
                   background='#f39c12',
                   foreground='white',
                   font=('Arial', 14, 'bold'),
                   borderwidth=2,
                   relief='raised',
                   padding=(10, 10))
    style.configure('Salir.TButton', 
                   background='#95a5a6',
                   foreground='white',
                   font=('Arial', 14, 'bold'),
                   borderwidth=2,
                   relief='raised',
                   padding=(10, 10))
    
    # Efectos hover para botones principales
    style.map('Ventas.TButton', 
             background=[('active', '#2980b9')],
             foreground=[('active', 'white')])
    style.map('Reportes.TButton', 
             background=[('active', '#c0392b')],
             foreground=[('active', 'white')])
    style.map('Ajustes.TButton', 
             background=[('active', '#e67e22')],
             foreground=[('active', 'white')])
    style.map('Salir.TButton', 
             background=[('active', '#7f8c8d')],
             foreground=[('active', 'white')])
    
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
