import tkinter as tk
from tkinter import ttk
import sys
import os
import platform
from View.email_view import abrir_config_email, mostrar_config_email_en_frame

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion, crear_menu_estandarizado
from Controller.styles_mac import configurar_estilos_macos, crear_boton_config_macos, crear_boton_volver_config_macos, es_macos

# Funciones obsoletas eliminadas - ahora usa la función estandarizada crear_menu_estandarizado()

def mostrar_configuraciones_en_frame(parent_frame, callback_volver):
    """
    Mostrar menú de configuraciones dentro de un frame existente usando la función estandarizada
    
    Args:
        parent_frame: Frame padre donde mostrar las configuraciones
        callback_volver: Función a llamar para volver al menú anterior
    """
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
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
    
    # Funciones para cada botón
    def volver_a_menu_configuraciones():
        """Volver al menú de configuraciones desde una configuración específica"""
        # Limpiar el frame padre antes de crear el nuevo menú
        for widget in parent_frame.winfo_children():
            widget.destroy()
        mostrar_configuraciones_en_frame(parent_frame, callback_volver)
    
    def abrir_email():
        """Abrir configuración de email"""
        mostrar_config_email_en_frame(parent_frame, volver_a_menu_configuraciones)
    
    def abrir_logo():
        """Abrir configuración de logo"""
        from View.logo import mostrar_logo_en_frame
        mostrar_logo_en_frame(parent_frame, volver_a_menu_configuraciones)
    
    def abrir_apariencia():
        """Abrir configuración de apariencia"""
        from View.appearance import mostrar_apariencia_en_frame
        mostrar_apariencia_en_frame(parent_frame, volver_a_menu_configuraciones)
    
    def abrir_telefono():
        """Abrir configuración de teléfono"""
        from tkinter import messagebox
        messagebox.showinfo("📞 Teléfono", 
                           "Configuración de Teléfono\n\n"
                           "Esta funcionalidad estará disponible próximamente.\n"
                           "Permitirá configurar números de contacto para reportes y facturas.")
    
    # Configurar botones usando la función estandarizada
    botones_config = [
        {
            'texto': 'Email',
            'comando': abrir_email,
            'imagen': img_email,
            'fila': 0,
            'columna': 0
        },
        {
            'texto': 'Logo',
            'comando': abrir_logo,
            'imagen': img_logo,
            'fila': 0,
            'columna': 1
        },
        {
            'texto': 'Apariencia',
            'comando': abrir_apariencia,
            'imagen': img_apariencia,
            'fila': 1,
            'columna': 0
        },
        {
            'texto': 'Teléfono',
            'comando': abrir_telefono,
            'imagen': img_telefono,
            'fila': 1,
            'columna': 1
        }
    ]
    
    # Usar la función estandarizada para crear el menú
    crear_menu_estandarizado(
        parent_frame,
        "⚙️ CONFIGURACIONES",
        "🔧 Selecciona una Configuración:",
        botones_config,
        callback_volver,
        "💡 Configura los diferentes aspectos de tu aplicación"
    )

def mostrar_configuraciones(parent=None):
    """
    Función para mostrar configuraciones en ventana separada usando la función estandarizada
    
    Args:
        parent: Ventana padre (opcional)
    """
    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("⚙️ Configuraciones")
    root.geometry("600x500")
    root.resizable(True, True)
    root.configure(bg='#ecf0f1')
    
    # Configurar ícono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Cargar imágenes para los botones (más pequeñas)
    try:
        img_email_popup = tk.PhotoImage(file="Img/correo-electronico.png")
        img_email_popup = img_email_popup.subsample(6, 6)
    except Exception:
        img_email_popup = None
    
    try:
        img_logo_popup = tk.PhotoImage(file="Img/subir-imagen.png")
        img_logo_popup = img_logo_popup.subsample(6, 6)
    except Exception:
        img_logo_popup = None
    
    try:
        img_apariencia_popup = tk.PhotoImage(file="Img/rueda-de-color.png")
        img_apariencia_popup = img_apariencia_popup.subsample(6, 6)
    except Exception:
        img_apariencia_popup = None
    
    try:
        img_telefono_popup = tk.PhotoImage(file="Img/telefono2.png")
        img_telefono_popup = img_telefono_popup.subsample(6, 6)
    except Exception:
        img_telefono_popup = None
    
    # Funciones para botones en ventana separada
    def abrir_email_popup():
        abrir_config_email(root)
    
    def abrir_logo_popup():
        from View.logo import mostrar_logo
        mostrar_logo(root)
    
    def abrir_apariencia_popup():
        from View.appearance import mostrar_apariencia
        mostrar_apariencia(root)
    
    def abrir_telefono_popup():
        from tkinter import messagebox
        messagebox.showinfo("Teléfono", 
                           "Configuración de Teléfono\n\n"
                           "Esta funcionalidad estará disponible próximamente.", 
                           parent=root)
    
    # Configurar botones usando la función estandarizada
    botones_config = [
        {'texto': 'Email', 'comando': abrir_email_popup, 'imagen': img_email_popup, 'fila': 0, 'columna': 0},
        {'texto': 'Logo', 'comando': abrir_logo_popup, 'imagen': img_logo_popup, 'fila': 0, 'columna': 1},
        {'texto': 'Apariencia', 'comando': abrir_apariencia_popup, 'imagen': img_apariencia_popup, 'fila': 1, 'columna': 0},
        {'texto': 'Teléfono', 'comando': abrir_telefono_popup, 'imagen': img_telefono_popup, 'fila': 1, 'columna': 1}
    ]
    
    # Usar la función estandarizada para crear el menú
    crear_menu_estandarizado(
        root,
        "⚙️ CONFIGURACIONES",
        "🔧 Selecciona una Configuración:",
        botones_config,
        root.destroy,  # Callback para cerrar la ventana
        "💡 Configura los diferentes aspectos de tu aplicación"
    )
    
    # Manejar cierre de ventana
    def on_close():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
