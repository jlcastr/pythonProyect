import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import os

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion

def crear_menu_reportes(parent_frame, callback_volver):
    """Crear el menú de reportes con botones en cuadrícula"""
    
    # Usar estilos centralizados con color #2c5aa0
    style = configurar_estilos_aplicacion()
    
    # Crear un frame centrado para los botones
    frame_centrado = tk.Frame(parent_frame)
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
    
    # Botón para volver al menú principal
    btn_volver = ttk.Button(frame_centrado, text="← Volver al Menú", 
                           command=callback_volver,
                           style='VolverButton.TButton')
    btn_volver.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
    # Título del menú de reportes
    titulo_reportes = tk.Label(frame_centrado, text="MENÚ DE REPORTES", 
                              font=("Arial", 16, "bold"))
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
    
    # Crear botones en cuadrícula (2x2, con el tercero en una segunda fila)
    # Fila 1
    if img_reporte_ventas:
        btn_reporte_ventas = ttk.Button(frame_centrado, text="REPORTE DE\nVENTAS", 
                                       image=img_reporte_ventas, compound=tk.TOP,
                                       command=abrir_reporte_ventas,
                                       style='ReportButton.TButton')
        btn_reporte_ventas.image = img_reporte_ventas
    else:
        btn_reporte_ventas = ttk.Button(frame_centrado, text="📊 REPORTE DE\nVENTAS", 
                                       command=abrir_reporte_ventas,
                                       style='ReportButton.TButton')
    btn_reporte_ventas.grid(row=1, column=0, padx=20, pady=20, ipadx=50, ipady=30)
    
    if img_historial:
        btn_historial_ventas = ttk.Button(frame_centrado, text="HISTORIAL DE\nNOTAS DE VENTA", 
                                         image=img_historial, compound=tk.TOP,
                                         command=abrir_historial_ventas,
                                         style='ReportButton.TButton')
        btn_historial_ventas.image = img_historial
    else:
        btn_historial_ventas = ttk.Button(frame_centrado, text="📋 HISTORIAL DE\nNOTAS DE VENTA", 
                                         command=abrir_historial_ventas,
                                         style='ReportButton.TButton')
    btn_historial_ventas.grid(row=1, column=1, padx=20, pady=20, ipadx=50, ipady=30)
    
    # Fila 2 - Centrar el botón de inventario
    if img_inventario:
        btn_reporte_inventario = ttk.Button(frame_centrado, text="REPORTE DE\nINVENTARIO", 
                                           image=img_inventario, compound=tk.TOP,
                                           command=abrir_reporte_inventario,
                                           style='ReportButton.TButton')
        btn_reporte_inventario.image = img_inventario
    else:
        btn_reporte_inventario = ttk.Button(frame_centrado, text="📦 REPORTE DE\nINVENTARIO", 
                                           command=abrir_reporte_inventario,
                                           style='ReportButton.TButton')
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