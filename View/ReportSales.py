import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

def mostrar_reporte_ventas_en_frame(parent_frame, callback_volver):
    """Mostrar reporte de ventas dentro de un frame existente"""
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()
    
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Frame principal para el reporte
    main_frame = tk.Frame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver
    header_frame = tk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 20))
    
    btn_volver = tk.Button(header_frame, text="← Volver al Menú de Reportes", 
                          command=lambda: [conn.close(), callback_volver()], 
                          bg="#2980b9", fg="white", 
                          font=("Arial", 10, "bold"), relief="raised", bd=2, cursor="hand2")
    btn_volver.pack(side="left")
    
    titulo = tk.Label(header_frame, text="📊 REPORTE DE VENTAS", 
                     font=("Arial", 16, "bold"), fg="#2c3e50")
    titulo.pack(side="right")

    # Filtro de fechas con estilo profesional
    frame_filtros = tk.Frame(main_frame, bg="#ecf0f1", relief="solid", bd=1)
    frame_filtros.pack(fill="x", pady=(0, 20), padx=5, ipady=8)

    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    from datetime import date
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd", mindate=date(1900, 1, 1))
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd", mindate=date(1900, 1, 1))
    entry_fin.pack(side="left", padx=5)

    # Frame contenedor para el TreeView con scrollbar
    tree_frame = tk.Frame(main_frame, relief="solid", bd=1, bg="#f8f9fa")
    tree_frame.pack(fill="both", expand=True, pady=(0, 10), padx=5)
    
    # Label para identificar la sección
    label_productos = tk.Label(tree_frame, text="📦 Productos Vendidos", 
                              font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
    label_productos.pack(anchor="w", pady=(8, 5), padx=5)
    
    # Treeview principal de productos con mejor diseño
    tree = ttk.Treeview(tree_frame, columns=("descripcion", "precio", "fecha_venta", "folio"), show="headings", height=18)
    tree.heading("descripcion", text="Descripción del Producto")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de Venta")
    tree.heading("folio", text="Folio")
    tree.column("descripcion", width=250, anchor="w")
    tree.column("precio", width=100, anchor="center")
    tree.column("fecha_venta", width=150, anchor="center")
    tree.column("folio", width=80, anchor="center")
    tree.pack(fill="both", expand=True, pady=(0, 8), padx=5)
    
    # Scrollbar para el TreeView
    scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_tree.set)
    scrollbar_tree.pack(side="right", fill="y")

    # Frame para el total general con mejor estilo
    frame_total = tk.Frame(main_frame, bg="#e3f2fd", relief="solid", bd=1)
    frame_total.pack(fill="x", pady=(10, 5), padx=5)
    
    total_general_var = tk.StringVar(value="💰 Total de Ventas: $0.00")
    label_total_general = tk.Label(frame_total, textvariable=total_general_var, 
                                  font=("Arial", 12, "bold"), bg="#e3f2fd", 
                                  fg="#1565c0", anchor="center", pady=8)
    label_total_general.pack(fill="x")

    def actualizar_total_general():
        total = 0.0
        for row_id in tree.get_children():
            values = tree.item(row_id, "values")
            if len(values) > 1:
                try:
                    total += float(values[1])
                except Exception:
                    pass
        total_general_var.set(f"💰 Total de Ventas: ${total:,.2f}")

    def filtrar():
        from tkinter import messagebox
        for row in tree.get_children():
            tree.delete(row)
        fecha_inicio = entry_inicio.get().strip()
        fecha_fin = entry_fin.get().strip()
        # Validación de fechas
        if fecha_inicio and fecha_fin:
            try:
                d_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                d_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                if d_inicio > d_fin:
                    messagebox.showwarning("Validación de fechas", "La fecha inicio no puede ser mayor que la fecha final.")
                    return
            except Exception:
                pass
        query = "SELECT ventas_items.descripcion, ventas_items.precio, VentaMaster.fecha_venta, VentaMaster.folio FROM ventas_items INNER JOIN VentaMaster ON ventas_items.venta_master_id = VentaMaster.id"
        params = []
        if fecha_inicio and fecha_fin:
            query += " WHERE date(VentaMaster.fecha_venta) BETWEEN ? AND ?"
            params = [fecha_inicio, fecha_fin]
        elif fecha_inicio:
            query += " WHERE date(VentaMaster.fecha_venta) >= ?"
            params = [fecha_inicio]
        elif fecha_fin:
            query += " WHERE date(VentaMaster.fecha_venta) <= ?"
            params = [fecha_fin]
        query += " ORDER BY VentaMaster.fecha_venta DESC"
        for row in cursor.execute(query, params):
            tree.insert("", tk.END, values=row)
        actualizar_total_general()

    btn_filtrar = tk.Button(frame_filtros, text="🔍 Filtrar", command=filtrar,
                           bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                           relief="raised", bd=2, padx=15, pady=5, cursor="hand2")
    btn_filtrar.pack(side="left", padx=(20, 10))

    # Cargar datos al crear la interfaz
    filtrar()


def mostrar_reporte_ventas(parent=None):
    """Función original para mostrar en ventana separada (mantener compatibilidad)"""
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()

    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("📊 Reporte de Ventas")
    root.geometry("1000x600")
    root.configure(bg='#ecf0f1')

    # Filtro de fechas con estilo profesional
    frame_filtros = tk.Frame(root, bg="#ecf0f1", relief="solid", bd=1)
    frame_filtros.pack(fill="x", padx=10, pady=10, ipady=8)

    tk.Label(frame_filtros, text="📅 Fecha inicio:", bg="#ecf0f1", font=("Arial", 10, "bold"), fg="#34495e").pack(side="left", padx=(10, 5))
    from datetime import date
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd", mindate=date(1900, 1, 1))
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="📅 Fecha fin:", bg="#ecf0f1", font=("Arial", 10, "bold"), fg="#34495e").pack(side="left", padx=(15, 5))
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd", mindate=date(1900, 1, 1))
    entry_fin.pack(side="left", padx=5)

    def filtrar():
        from tkinter import messagebox
        for row in tree.get_children():
            tree.delete(row)
        fecha_inicio = entry_inicio.get().strip()
        fecha_fin = entry_fin.get().strip()
        # Validación de fechas
        if fecha_inicio and fecha_fin:
            try:
                d_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                d_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                if d_inicio > d_fin:
                    messagebox.showwarning("Validación de fechas", "La fecha inicio no puede ser mayor que la fecha final.")
                    return
            except Exception:
                pass
        query = "SELECT ventas_items.descripcion, ventas_items.precio, VentaMaster.fecha_venta, VentaMaster.folio FROM ventas_items INNER JOIN VentaMaster ON ventas_items.venta_master_id = VentaMaster.id"
        params = []
        if fecha_inicio and fecha_fin:
            query += " WHERE date(VentaMaster.fecha_venta) BETWEEN ? AND ?"
            params = [fecha_inicio, fecha_fin]
        elif fecha_inicio:
            query += " WHERE date(VentaMaster.fecha_venta) >= ?"
            params = [fecha_inicio]
        elif fecha_fin:
            query += " WHERE date(VentaMaster.fecha_venta) <= ?"
            params = [fecha_fin]
        query += " ORDER BY VentaMaster.fecha_venta DESC"
        for row in cursor.execute(query, params):
            tree.insert("", tk.END, values=row)
        actualizar_total_general()

    btn_filtrar = tk.Button(frame_filtros, text="🔍 Filtrar", command=filtrar,
                           bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                           relief="raised", bd=2, padx=15, pady=5, cursor="hand2")
    btn_filtrar.pack(side="left", padx=(20, 10))

    # Frame contenedor para el TreeView con scrollbar
    tree_frame = tk.Frame(root, relief="solid", bd=1, bg="#f8f9fa")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
    
    # Label para identificar la sección
    label_productos = tk.Label(tree_frame, text="📦 Productos Vendidos", 
                              font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
    label_productos.pack(anchor="w", pady=(8, 5), padx=5)
    
    # Treeview principal de productos con mejor diseño
    tree = ttk.Treeview(tree_frame, columns=("descripcion", "precio", "fecha_venta", "folio"), show="headings", height=18)
    tree.heading("descripcion", text="Descripción del Producto")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de Venta")
    tree.heading("folio", text="Folio")
    tree.column("descripcion", width=300, anchor="w")
    tree.column("precio", width=100, anchor="center")
    tree.column("fecha_venta", width=150, anchor="center")
    tree.column("folio", width=80, anchor="center")
    tree.pack(fill="both", expand=True, pady=(0, 8), padx=5)
    
    # Scrollbar para el TreeView
    scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_tree.set)
    scrollbar_tree.pack(side="right", fill="y")

    # Frame para el total general con mejor estilo
    frame_total = tk.Frame(root, bg="#e3f2fd", relief="solid", bd=1)
    frame_total.pack(fill="x", padx=10, pady=(10, 10))
    
    total_general_var = tk.StringVar(value="💰 Total de Ventas: $0.00")
    label_total_general = tk.Label(frame_total, textvariable=total_general_var, 
                                  font=("Arial", 12, "bold"), bg="#e3f2fd", 
                                  fg="#1565c0", anchor="center", pady=8)
    label_total_general.pack(fill="x")

    def actualizar_total_general():
        total = 0.0
        for row_id in tree.get_children():
            values = tree.item(row_id, "values")
            if len(values) > 1:
                try:
                    total += float(values[1])
                except Exception:
                    pass
        total_general_var.set(f"💰 Total de Ventas: ${total:,.2f}")

    filtrar()  # Mostrar todos al abrir

    def on_close():
        conn.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)