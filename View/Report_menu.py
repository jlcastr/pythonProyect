import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os
import platform

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion, crear_menu_estandarizado
from Controller.styles_mac import configurar_estilos_macos, crear_boton_report_macos, crear_boton_volver_report_macos, es_macos

def crear_boton_report_optimizado(parent, text, command, image=None):
    """
    Crear botón optimizado para reportes en la plataforma actual
    """
    is_macos = platform.system() == 'Darwin'
    
    if is_macos:
        # En macOS usar los estilos optimizados sin bordes
        return crear_boton_report_macos(parent, text, command, image)
    else:
        # En Windows/Linux usar tk.Button normal
        if image:
            boton = tk.Button(parent, text=text, command=command,
                             bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                             relief='raised', bd=2, cursor='hand2',
                             image=image, compound=tk.TOP)
            boton.image = image  # Mantener referencia de la imagen
        else:
            boton = tk.Button(parent, text=text, command=command,
                             bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                             relief='raised', bd=2, cursor='hand2')
        return boton

def crear_boton_volver_report_optimizado(parent, text, command):
    """
    Crear botón de volver optimizado para reportes en la plataforma actual
    """
    is_macos = platform.system() == 'Darwin'
    
    if is_macos:
        # En macOS usar los estilos optimizados sin bordes
        return crear_boton_volver_report_macos(parent, text, command)
    else:
        # En Windows/Linux usar tk.Button normal
        return tk.Button(parent, text=text, command=command,
                        bg='#357ab8', fg='white', font=("Arial", 10, "bold"),
                        relief='raised', bd=2, cursor='hand2')

def crear_menu_reportes(parent_frame, callback_volver):
    """Crear el menú de reportes usando la función estandarizada"""
    
    # Cargar imágenes para los botones de reportes
    try:
        img_reporte_ventas = tk.PhotoImage(file="Img/reporte-de-negocios.png")
        img_reporte_ventas = img_reporte_ventas.subsample(6, 6)  # Tamaño reducido para que quepa completamente
    except Exception:
        img_reporte_ventas = None
    
    try:
        img_historial = tk.PhotoImage(file="Img/historial-de-transacciones.png")
        img_historial = img_historial.subsample(6, 6)  # Tamaño reducido para que quepa completamente
    except Exception:
        img_historial = None
    
    try:
        img_inventario = tk.PhotoImage(file="Img/inventario.png")
        img_inventario = img_inventario.subsample(6, 6)  # Tamaño reducido para que quepa completamente
    except Exception:
        img_inventario = None
    
    # Funciones para cada botón
    def volver_a_menu_reportes():
        """Volver al menú de reportes desde un reporte específico"""
        # Limpiar el frame padre antes de crear el nuevo menú
        for widget in parent_frame.winfo_children():
            widget.destroy()
        crear_menu_reportes(parent_frame, callback_volver)
    
    def abrir_reporte_ventas():
        """Abrir el reporte de ventas en el mismo frame"""
        from View.ReportSales import mostrar_reporte_ventas_en_frame
        mostrar_reporte_ventas_en_frame(parent_frame, volver_a_menu_reportes)
    
    def abrir_historial_ventas():
        """Abrir el historial de notas de venta en el mismo frame"""
        from View.ReportHistorySales import mostrar_historial_ventas_en_frame
        mostrar_historial_ventas_en_frame(parent_frame, volver_a_menu_reportes)
    
    def abrir_reporte_inventario():
        """Abrir el reporte de inventario"""
        from tkinter import messagebox
        messagebox.showinfo("Reporte de Inventario", "Módulo de reporte de inventario en desarrollo")
    
    # Configurar botones usando la función estandarizada
    botones_config = [
        {
            'texto': 'REPORTE DE\nVENTAS',
            'comando': abrir_reporte_ventas,
            'imagen': img_reporte_ventas,
            'fila': 0,
            'columna': 0
        },
        {
            'texto': 'NOTAS DE\nVENTA',
            'comando': abrir_historial_ventas,
            'imagen': img_historial,
            'fila': 0,
            'columna': 1
        },
        {
            'texto': 'REPORTE DE\nINVENTARIO',
            'comando': abrir_reporte_inventario,
            'imagen': img_inventario,
            'fila': 1,
            'columna': 0,
            'columnspan': 2
        }
    ]
    
    # Usar la función estandarizada para crear el menú
    crear_menu_estandarizado(
        parent_frame,
        "📊 MENÚ DE REPORTES",
        "📋 Selecciona un Reporte:",
        botones_config,
        callback_volver,
        "💡 Genera reportes detallados de tu negocio"
    )

if __name__ == "__main__":
    # Prueba del menú de reportes
    root = tk.Tk()
    root.title("Menú de Reportes")
    root.geometry("600x400")
    
    def dummy_volver():
        print("Volver al menú principal")
    
    crear_menu_reportes(root, dummy_volver)
    root.mainloop()