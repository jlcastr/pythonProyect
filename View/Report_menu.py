import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os
import platform

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion
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
    """Crear el menú de reportes con botones en cuadrícula"""
    
    # Configurar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Configurar estilos específicos para macOS si es necesario
    if es_macos():
        configurar_estilos_macos()
    
    # Crear un frame centrado para los botones con fondo personalizado
    frame_centrado = tk.Frame(parent_frame, bg='#f8f9fa')
    frame_centrado.pack(expand=True)
    
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
    
    # Botón para volver al menú principal optimizado
    btn_volver = crear_boton_volver_report_optimizado(frame_centrado, "← Volver al Menú", callback_volver)
    btn_volver.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
    # Título del menú de reportes con fondo consistente
    titulo_reportes = tk.Label(frame_centrado, text="📊 MENÚ DE REPORTES", 
                              font=("Arial", 16, "bold"), fg="#2c3e50", bg='#f8f9fa')
    titulo_reportes.grid(row=0, column=1, pady=10, columnspan=2)
    
    def abrir_reporte_ventas():
        """Abrir el reporte de ventas en el mismo frame"""
        from View.ReportSales import mostrar_reporte_ventas_en_frame
        mostrar_reporte_ventas_en_frame(parent_frame, callback_volver)
    
    def abrir_historial_ventas():
        """Abrir el historial de notas de venta en el mismo frame"""
        from View.ReportView import mostrar_historial_ventas_en_frame
        mostrar_historial_ventas_en_frame(parent_frame, callback_volver)
    
    def abrir_reporte_inventario():
        """Abrir el reporte de inventario"""
        from tkinter import messagebox
        messagebox.showinfo("Reporte de Inventario", "Módulo de reporte de inventario en desarrollo")
    
    # Crear botones en cuadrícula optimizados (2x2, con el tercero en una segunda fila)
    # Fila 1
    btn_reporte_ventas = crear_boton_report_optimizado(frame_centrado, "REPORTE DE\nVENTAS", 
                                                      abrir_reporte_ventas, img_reporte_ventas)
    btn_reporte_ventas.grid(row=1, column=0, padx=20, pady=20, ipadx=50, ipady=30)
    
    btn_historial_ventas = crear_boton_report_optimizado(frame_centrado, "HISTORIAL DE\nNOTAS DE VENTA", 
                                                        abrir_historial_ventas, img_historial)
    btn_historial_ventas.grid(row=1, column=1, padx=20, pady=20, ipadx=50, ipady=30)
    
    # Fila 2 - Centrar el botón de inventario optimizado
    btn_reporte_inventario = crear_boton_report_optimizado(frame_centrado, "REPORTE DE\nINVENTARIO", 
                                                          abrir_reporte_inventario, img_inventario)
    btn_reporte_inventario.grid(row=2, column=0, columnspan=2, padx=20, pady=20, ipadx=50, ipady=30)
    
    # Centrar las columnas
    frame_centrado.grid_columnconfigure(0, weight=1)
    frame_centrado.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    # Prueba del menú de reportes
    root = tk.Tk()
    root.title("Menú de Reportes")
    root.geometry("600x400")
    
    def dummy_volver():
        print("Volver al menú principal")
    
    crear_menu_reportes(root, dummy_volver)
    root.mainloop()