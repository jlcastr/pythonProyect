import tkinter as tk
from tkinter import ttk
import sqlite3

def crear_menu_reportes(parent_frame, callback_volver):
    """Crear el menú de reportes con botones en cuadrícula"""
    
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
    btn_volver = tk.Button(frame_centrado, text="← Volver al Menú", 
                          command=callback_volver, 
                          bg="#357ab8", fg="white", 
                          font=("Arial", 10, "bold"))
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
        btn_reporte_ventas = tk.Button(frame_centrado, text="REPORTE DE\nVENTAS", 
                                      image=img_reporte_ventas, compound=tk.TOP,
                                      command=abrir_reporte_ventas,
                                      font=("Arial", 10, "bold"),
                                      width=170, height=110,
                                      bg="#357ab8", fg="white", relief="raised",
                                      bd=2, padx=10, pady=8)
    else:
        btn_reporte_ventas = tk.Button(frame_centrado, text="REPORTE DE\nVENTAS", 
                                      command=abrir_reporte_ventas,
                                      font=("Arial", 12, "bold"),
                                      width=18, height=6,
                                      bg="#357ab8", fg="white", relief="raised",
                                      bd=2, padx=5, pady=5)
    btn_reporte_ventas.grid(row=1, column=0, padx=20, pady=20)
    
    # Mantener referencia de la imagen
    if img_reporte_ventas:
        btn_reporte_ventas.image = img_reporte_ventas
    
    if img_historial:
        btn_historial_ventas = tk.Button(frame_centrado, text="HISTORIAL DE\nNOTAS DE VENTA", 
                                        image=img_historial, compound=tk.TOP,
                                        command=abrir_historial_ventas,
                                        font=("Arial", 10, "bold"),
                                        width=170, height=110,
                                        bg="#357ab8", fg="white", relief="raised",
                                        bd=2, padx=10, pady=8)
    else:
        btn_historial_ventas = tk.Button(frame_centrado, text="HISTORIAL DE\nNOTAS DE VENTA", 
                                        command=abrir_historial_ventas,
                                        font=("Arial", 12, "bold"),
                                        width=18, height=6,
                                        bg="#357ab8", fg="white", relief="raised",
                                        bd=2, padx=5, pady=5)
    btn_historial_ventas.grid(row=1, column=1, padx=20, pady=20)
    
    # Mantener referencia de la imagen
    if img_historial:
        btn_historial_ventas.image = img_historial
    
    # Fila 2 - Centrar el botón de inventario
    if img_inventario:
        btn_reporte_inventario = tk.Button(frame_centrado, text="REPORTE DE\nINVENTARIO", 
                                          image=img_inventario, compound=tk.TOP,
                                          command=abrir_reporte_inventario,
                                          font=("Arial", 10, "bold"),
                                          width=170, height=110,
                                          bg="#357ab8", fg="white", relief="raised",
                                          bd=2, padx=10, pady=8)
    else:
        btn_reporte_inventario = tk.Button(frame_centrado, text="REPORTE DE\nINVENTARIO", 
                                          command=abrir_reporte_inventario,
                                          font=("Arial", 12, "bold"),
                                          width=18, height=6,
                                          bg="#357ab8", fg="white", relief="raised",
                                          bd=2, padx=5, pady=5)
    btn_reporte_inventario.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
    
    # Mantener referencia de la imagen
    if img_inventario:
        btn_reporte_inventario.image = img_inventario
    
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