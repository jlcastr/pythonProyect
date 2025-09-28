import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime

def mostrar_historial_ventas(parent=None):
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()

    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("Historial de notas de venta")
    root.geometry("900x500")

    # Filtro de fechas
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(side="top", anchor="nw", padx=10, pady=(10,0), fill="x")
    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_fin.pack(side="left", padx=5)

    # Treeview principal de productos
    tree_general = ttk.Treeview(root, columns=("descripcion", "precio", "fecha_venta", "folio"), show="headings", height=18)
    tree_general.heading("descripcion", text="Descripción")
    tree_general.heading("precio", text="Precio")
    tree_general.heading("fecha_venta", text="Fecha de venta")
    tree_general.heading("folio", text="Folio")
    tree_general.column("descripcion", width=200)
    tree_general.column("precio", width=80, anchor="center")
    tree_general.column("fecha_venta", width=150, anchor="center")
    tree_general.column("folio", width=80, anchor="center")
    tree_general.pack(fill="both", expand=True, padx=10, pady=(0,0))

    # Label para mostrar el total general debajo del Treeview principal
    total_general_var = tk.StringVar(value="Total: $0.00")
    label_total_general = tk.Label(root, textvariable=total_general_var, font=("Segoe UI", 12, "bold"), anchor="e", pady=8)
    label_total_general.pack(fill="x", padx=10, pady=(0,10))

    def actualizar_total_general():
        total = 0.0
        for row_id in tree_general.get_children():
            values = tree_general.item(row_id, "values")
            if len(values) > 1:
                try:
                    total += float(values[1])
                except Exception:
                    pass
        total_general_var.set(f"Total: ${total:,.2f}")

    def cargar_ventas():
        for row in tree_general.get_children():
            tree_general.delete(row)
        cursor.execute("SELECT ventas_items.descripcion, ventas_items.precio, VentaMaster.fecha_venta, VentaMaster.folio FROM ventas_items INNER JOIN VentaMaster ON ventas_items.venta_master_id = VentaMaster.id ORDER BY VentaMaster.fecha_venta DESC")
        productos = cursor.fetchall()
        for prod in productos:
            tree_general.insert("", tk.END, values=prod)
        actualizar_total_general()

    def filtrar_ventas():
        for row in tree_general.get_children():
            tree_general.delete(row)
        fecha_inicio = entry_inicio.get().strip()
        fecha_fin = entry_fin.get().strip()
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
        productos = list(cursor.execute(query, params))
        for prod in productos:
            tree_general.insert("", tk.END, values=prod)
        actualizar_total_general()

    btn_filtrar = tk.Button(frame_filtros, text="Filtrar", command=filtrar_ventas)
    btn_filtrar.pack(side="left", padx=10)

    # Llenar el listado al abrir la ventana
    cargar_ventas()

    # No mainloop() aquí, solo cerrar conexión al cerrar la ventana
    def on_close():
        conn.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)