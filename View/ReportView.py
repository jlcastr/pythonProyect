import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime

def mostrar_historial_ventas_en_frame(parent_frame, callback_volver):
    """Mostrar historial de ventas dentro de un frame existente"""
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()
    
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Frame principal para el historial
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
    
    titulo = tk.Label(header_frame, text="HISTORIAL DE NOTAS DE VENTA", 
                     font=("Arial", 16, "bold"))
    titulo.pack(side="right")

    # Filtro de fechas
    frame_filtros = tk.Frame(main_frame)
    frame_filtros.pack(fill="x", pady=(0, 20))
    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_fin.pack(side="left", padx=5)

    # Frame contenedor para el diseño horizontal
    contenedor_horizontal = tk.Frame(main_frame)
    contenedor_horizontal.pack(fill="both", expand=True, pady=(0, 10))

    # Frame izquierdo para VentaMaster (40% del ancho)
    frame_izquierdo = tk.Frame(contenedor_horizontal, width=380, relief="solid", bd=1, bg="#f8f9fa")
    frame_izquierdo.pack(side="left", fill="y", padx=(0, 15))
    frame_izquierdo.pack_propagate(False)

    # Label para las ventas maestras con mejor estilo
    label_ventas = tk.Label(frame_izquierdo, text="📋 Ventas Realizadas", 
                           font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
    label_ventas.pack(anchor="w", pady=(8, 5), padx=5)

    # Treeview principal de VentaMaster (ventas maestras) - Diseño compacto
    tree_ventas_master = ttk.Treeview(frame_izquierdo, columns=("folio", "fecha_venta", "total"), show="headings", height=20)
    tree_ventas_master.heading("folio", text="Folio")
    tree_ventas_master.heading("fecha_venta", text="Fecha")
    tree_ventas_master.heading("total", text="Total")
    tree_ventas_master.column("folio", width=50, anchor="center")
    tree_ventas_master.column("fecha_venta", width=130, anchor="center")
    tree_ventas_master.column("total", width=85, anchor="center")
    tree_ventas_master.pack(fill="both", expand=True, pady=(0, 8), padx=5)
    
    # Scrollbar para VentaMaster
    scrollbar_ventas = ttk.Scrollbar(frame_izquierdo, orient="vertical", command=tree_ventas_master.yview)
    tree_ventas_master.configure(yscrollcommand=scrollbar_ventas.set)
    scrollbar_ventas.pack(side="right", fill="y")

    # Frame derecho para items (60% del ancho restante)
    frame_derecho = tk.Frame(contenedor_horizontal, relief="solid", bd=1, bg="#f8f9fa")
    frame_derecho.pack(side="right", fill="both", expand=True, padx=(15, 0))

    # Label para separar las secciones con mejor estilo
    label_separador = tk.Label(frame_derecho, text="🛍️ Items de la Venta Seleccionada", 
                              font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
    label_separador.pack(anchor="w", pady=(8, 5), padx=5)

    # Treeview secundario para items de la venta seleccionada
    tree_items = ttk.Treeview(frame_derecho, columns=("descripcion", "precio"), show="headings", height=20)
    tree_items.heading("descripcion", text="Descripción del Producto")
    tree_items.heading("precio", text="Precio")
    tree_items.column("descripcion", width=350, anchor="w")
    tree_items.column("precio", width=100, anchor="center")
    tree_items.pack(fill="both", expand=True, pady=(0, 8), padx=5)
    
    # Scrollbar para items
    scrollbar_items = ttk.Scrollbar(frame_derecho, orient="vertical", command=tree_items.yview)
    tree_items.configure(yscrollcommand=scrollbar_items.set)
    scrollbar_items.pack(side="right", fill="y")

    # Frame para el total general con mejor estilo
    frame_total = tk.Frame(main_frame, bg="#e3f2fd", relief="solid", bd=1)
    frame_total.pack(fill="x", pady=(10, 5), padx=5)
    
    total_general_var = tk.StringVar(value="💰 Total General: $0.00")
    label_total_general = tk.Label(frame_total, textvariable=total_general_var, 
                                  font=("Arial", 12, "bold"), bg="#e3f2fd", 
                                  fg="#1565c0", anchor="center", pady=8)
    label_total_general.pack(fill="x")

    def actualizar_total_general():
        total = 0.0
        for row_id in tree_ventas_master.get_children():
            values = tree_ventas_master.item(row_id, "values")
            if len(values) > 2:
                try:
                    # El total está en la tercera columna (índice 2)
                    total_str = values[2].replace("$", "").replace(",", "")
                    total += float(total_str)
                except Exception:
                    pass
        total_general_var.set(f"💰 Total General: ${total:,.2f}")

    def cargar_ventas():
        # Limpiar ambos treeviews
        for row in tree_ventas_master.get_children():
            tree_ventas_master.delete(row)
        for row in tree_items.get_children():
            tree_items.delete(row)
        
        # Consultar VentaMaster con total calculado
        cursor.execute("""
            SELECT vm.folio, vm.fecha_venta, vm.id,
                   COALESCE(SUM(vi.precio), 0) as total
            FROM VentaMaster vm
            LEFT JOIN ventas_items vi ON vm.id = vi.venta_master_id
            GROUP BY vm.id, vm.folio, vm.fecha_venta
            ORDER BY vm.fecha_venta DESC
        """)
        ventas = cursor.fetchall()
        for venta in ventas:
            folio, fecha, venta_id, total = venta
            tree_ventas_master.insert("", tk.END, values=(folio, fecha, f"${total:,.2f}"), tags=(venta_id,))
        
        actualizar_total_general()

    def filtrar_ventas():
        # Limpiar ambos treeviews
        for row in tree_ventas_master.get_children():
            tree_ventas_master.delete(row)
        for row in tree_items.get_children():
            tree_items.delete(row)
            
        fecha_inicio = entry_inicio.get().strip()
        fecha_fin = entry_fin.get().strip()
        
        query = """
            SELECT vm.folio, vm.fecha_venta, vm.id,
                   COALESCE(SUM(vi.precio), 0) as total
            FROM VentaMaster vm
            LEFT JOIN ventas_items vi ON vm.id = vi.venta_master_id
        """
        params = []
        if fecha_inicio and fecha_fin:
            query += " WHERE date(vm.fecha_venta) BETWEEN ? AND ?"
            params = [fecha_inicio, fecha_fin]
        elif fecha_inicio:
            query += " WHERE date(vm.fecha_venta) >= ?"
            params = [fecha_inicio]
        elif fecha_fin:
            query += " WHERE date(vm.fecha_venta) <= ?"
            params = [fecha_fin]
        
        query += " GROUP BY vm.id, vm.folio, vm.fecha_venta ORDER BY vm.fecha_venta DESC"
        
        ventas = list(cursor.execute(query, params))
        for venta in ventas:
            folio, fecha, venta_id, total = venta
            tree_ventas_master.insert("", tk.END, values=(folio, fecha, f"${total:,.2f}"), tags=(venta_id,))
        
        actualizar_total_general()

    def on_venta_select(event):
        """Cargar items cuando se selecciona una venta"""
        selection = tree_ventas_master.selection()
        if not selection:
            # Si no hay selección, mostrar total general
            actualizar_total_general()
            return
        
        # Limpiar el treeview de items
        for row in tree_items.get_children():
            tree_items.delete(row)
        
        # Obtener el ID de la venta seleccionada y su total
        item = selection[0]
        venta_id = tree_ventas_master.item(item, "tags")[0]
        valores_venta = tree_ventas_master.item(item, "values")
        total_venta = valores_venta[2] if len(valores_venta) > 2 else "$0.00"
        
        # Actualizar el total con el valor de la venta seleccionada
        total_general_var.set(f"💰 Total de Venta Seleccionada: {total_venta}")
        
        # Cargar los items de la venta seleccionada
        cursor.execute("""
            SELECT descripcion, precio 
            FROM ventas_items 
            WHERE venta_master_id = ? 
            ORDER BY id
        """, (venta_id,))
        
        items = cursor.fetchall()
        for item_data in items:
            descripcion, precio = item_data
            tree_items.insert("", tk.END, values=(descripcion, f"${precio:,.2f}"))

    # Función para volver al total general cuando se deselecciona
    def on_tree_click(event):
        """Detectar clic en área vacía para mostrar total general"""
        region = tree_ventas_master.identify_region(event.x, event.y)
        if region == "nothing":
            tree_ventas_master.selection_remove(tree_ventas_master.selection())
            # Limpiar items
            for row in tree_items.get_children():
                tree_items.delete(row)
            # Mostrar total general
            actualizar_total_general()

    # Vincular los eventos de selección
    tree_ventas_master.bind("<<TreeviewSelect>>", on_venta_select)
    tree_ventas_master.bind("<Button-1>", on_tree_click)

    btn_filtrar = tk.Button(frame_filtros, text="🔍 Filtrar", command=filtrar_ventas,
                           bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                           relief="raised", bd=2, padx=15, pady=5, cursor="hand2")
    btn_filtrar.pack(side="left", padx=10)

    # Llenar el listado al crear la interfaz
    cargar_ventas()


def mostrar_historial_ventas(parent=None):
    """Función original para mostrar en ventana separada (mantener compatibilidad)"""
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()

    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("Historial de notas de venta")
    root.geometry("1200x700")  # Aumentar ancho para diseño horizontal

    # Filtro de fechas
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(side="top", anchor="nw", padx=10, pady=(10,0), fill="x")
    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_fin.pack(side="left", padx=5)

    # Frame contenedor para el diseño horizontal
    contenedor_horizontal = tk.Frame(root)
    contenedor_horizontal.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    # Frame izquierdo para VentaMaster (40% del ancho)
    frame_izquierdo = tk.Frame(contenedor_horizontal, width=480, relief="solid", bd=1, bg="#f8f9fa")
    frame_izquierdo.pack(side="left", fill="y", padx=(0, 15))
    frame_izquierdo.pack_propagate(False)

    # Label para las ventas maestras con mejor estilo
    label_ventas = tk.Label(frame_izquierdo, text="📋 Ventas Realizadas", 
                           font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
    label_ventas.pack(anchor="w", pady=(8, 5), padx=5)

    # Treeview principal de VentaMaster
    tree_ventas_master = ttk.Treeview(frame_izquierdo, columns=("folio", "fecha_venta", "total"), show="headings", height=15)
    tree_ventas_master.heading("folio", text="Folio")
    tree_ventas_master.heading("fecha_venta", text="Fecha y Hora")  
    tree_ventas_master.heading("total", text="Total")
    tree_ventas_master.column("folio", width=80, anchor="center")
    tree_ventas_master.column("fecha_venta", width=150, anchor="center")
    tree_ventas_master.column("total", width=100, anchor="center")
    tree_ventas_master.pack(fill="both", expand=True, pady=(0, 10))

    # Frame derecho para items
    frame_derecho = tk.Frame(contenedor_horizontal)
    frame_derecho.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # Label para separar las secciones
    label_separador = tk.Label(frame_derecho, text="Items de la venta seleccionada:", 
                              font=("Arial", 12, "bold"))
    label_separador.pack(anchor="w", pady=(0, 5))

    # Treeview secundario para items
    tree_items = ttk.Treeview(frame_derecho, columns=("descripcion", "precio"), show="headings", height=15)
    tree_items.heading("descripcion", text="Descripción")
    tree_items.heading("precio", text="Precio")
    tree_items.column("descripcion", width=250)
    tree_items.column("precio", width=100, anchor="center")
    tree_items.pack(fill="both", expand=True, pady=(0, 10))

    # Label para mostrar el total general
    total_general_var = tk.StringVar(value="Total: $0.00")
    label_total_general = tk.Label(root, textvariable=total_general_var, font=("Segoe UI", 12, "bold"), anchor="e", pady=8)
    label_total_general.pack(fill="x", padx=10, pady=(0,10))

    def actualizar_total_general():
        total = 0.0
        for row_id in tree_ventas_master.get_children():
            values = tree_ventas_master.item(row_id, "values")
            if len(values) > 2:
                try:
                    total_str = values[2].replace("$", "").replace(",", "")
                    total += float(total_str)
                except Exception:
                    pass
        total_general_var.set(f"Total: ${total:,.2f}")

    def cargar_ventas():
        for row in tree_ventas_master.get_children():
            tree_ventas_master.delete(row)
        for row in tree_items.get_children():
            tree_items.delete(row)
        
        cursor.execute("""
            SELECT vm.folio, vm.fecha_venta, vm.id,
                   COALESCE(SUM(vi.precio), 0) as total
            FROM VentaMaster vm
            LEFT JOIN ventas_items vi ON vm.id = vi.venta_master_id
            GROUP BY vm.id, vm.folio, vm.fecha_venta
            ORDER BY vm.fecha_venta DESC
        """)
        ventas = cursor.fetchall()
        for venta in ventas:
            folio, fecha, venta_id, total = venta
            tree_ventas_master.insert("", tk.END, values=(folio, fecha, f"${total:,.2f}"), tags=(venta_id,))
        
        actualizar_total_general()

    def filtrar_ventas():
        for row in tree_ventas_master.get_children():
            tree_ventas_master.delete(row)
        for row in tree_items.get_children():
            tree_items.delete(row)
            
        fecha_inicio = entry_inicio.get().strip()
        fecha_fin = entry_fin.get().strip()
        
        query = """
            SELECT vm.folio, vm.fecha_venta, vm.id,
                   COALESCE(SUM(vi.precio), 0) as total
            FROM VentaMaster vm
            LEFT JOIN ventas_items vi ON vm.id = vi.venta_master_id
        """
        params = []
        if fecha_inicio and fecha_fin:
            query += " WHERE date(vm.fecha_venta) BETWEEN ? AND ?"
            params = [fecha_inicio, fecha_fin]
        elif fecha_inicio:
            query += " WHERE date(vm.fecha_venta) >= ?"
            params = [fecha_inicio]
        elif fecha_fin:
            query += " WHERE date(vm.fecha_venta) <= ?"
            params = [fecha_fin]
        
        query += " GROUP BY vm.id, vm.folio, vm.fecha_venta ORDER BY vm.fecha_venta DESC"
        
        ventas = list(cursor.execute(query, params))
        for venta in ventas:
            folio, fecha, venta_id, total = venta
            tree_ventas_master.insert("", tk.END, values=(folio, fecha, f"${total:,.2f}"), tags=(venta_id,))
        
        actualizar_total_general()

    def on_venta_select(event):
        selection = tree_ventas_master.selection()
        if not selection:
            # Si no hay selección, mostrar total general
            actualizar_total_general()
            return
        
        for row in tree_items.get_children():
            tree_items.delete(row)
        
        item = selection[0]
        venta_id = tree_ventas_master.item(item, "tags")[0]
        valores_venta = tree_ventas_master.item(item, "values")
        total_venta = valores_venta[2] if len(valores_venta) > 2 else "$0.00"
        
        # Actualizar el total con el valor de la venta seleccionada
        total_general_var.set(f"💰 Total de Venta Seleccionada: {total_venta}")
        
        cursor.execute("""
            SELECT descripcion, precio 
            FROM ventas_items 
            WHERE venta_master_id = ? 
            ORDER BY id
        """, (venta_id,))
        
        items = cursor.fetchall()
        for item_data in items:
            descripcion, precio = item_data
            tree_items.insert("", tk.END, values=(descripcion, f"${precio:,.2f}"))

    # Función para volver al total general en ventana separada
    def on_tree_click_separada(event):
        """Detectar clic en área vacía para mostrar total general"""
        region = tree_ventas_master.identify_region(event.x, event.y)
        if region == "nothing":
            tree_ventas_master.selection_remove(tree_ventas_master.selection())
            # Limpiar items
            for row in tree_items.get_children():
                tree_items.delete(row)
            # Mostrar total general
            actualizar_total_general()

    tree_ventas_master.bind("<<TreeviewSelect>>", on_venta_select)
    tree_ventas_master.bind("<Button-1>", on_tree_click_separada)

    btn_filtrar = tk.Button(frame_filtros, text="🔍 Filtrar", command=filtrar_ventas,
                           bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                           relief="raised", bd=2, padx=15, pady=5, cursor="hand2")
    btn_filtrar.pack(side="left", padx=10)

    # Llenar el listado al abrir la ventana
    cargar_ventas()

    # No mainloop() aquí, solo cerrar conexión al cerrar la ventana
    def on_close():
        conn.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)