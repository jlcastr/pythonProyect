
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

def mostrar_reporte_ventas(parent=None):
    conn = sqlite3.connect("config/sqliteDB.db")
    cursor = conn.cursor()

    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("Reporte de ventas")
    root.geometry("900x500")

    # Filtro de fechas
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
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
        query = "SELECT descripcion, precio, fecha_venta, venta_master_id FROM ventas_items"
        params = []
        if fecha_inicio and fecha_fin:
            query += " WHERE date(fecha_venta) BETWEEN ? AND ?"
            params = [fecha_inicio, fecha_fin]
        elif fecha_inicio:
            query += " WHERE date(fecha_venta) >= ?"
            params = [fecha_inicio]
        elif fecha_fin:
            query += " WHERE date(fecha_venta) <= ?"
            params = [fecha_fin]
        query += " ORDER BY fecha_venta DESC"
        for row in cursor.execute(query, params):
            tree.insert("", tk.END, values=row)

    btn_filtrar = tk.Button(frame_filtros, text="Filtrar", command=filtrar)
    btn_filtrar.pack(side="left", padx=10)

    # Tabla de resultados
    style = ttk.Style()
    style.theme_use("default")
    style.configure("minimal.Treeview",
                    background="#fafafa",
                    foreground="#222",
                    rowheight=24,
                    fieldbackground="#fafafa",
                    font=("Segoe UI", 10),
                    borderwidth=0)
    style.configure("minimal.Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#eaeaea",
                    foreground="#222",
                    borderwidth=0)
    style.layout("minimal.Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'})
    ])
    style.map("minimal.Treeview",
              background=[('selected', '#e0e0e0')])
    style.map("minimal.Treeview.Heading",
              background=[('active', '#cccccc')])

    tree = ttk.Treeview(root, columns=("descripcion", "precio", "fecha_venta", "venta_master_id"), show="headings", height=18, style="minimal.Treeview")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de venta")
    tree.heading("venta_master_id", text="Folio")
    tree.column("descripcion", width=200)
    tree.column("precio", width=80, anchor="center")
    tree.column("fecha_venta", width=150, anchor="center")
    tree.column("venta_master_id", width=80, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    filtrar()  # Mostrar todos al abrir

    def on_close():
        conn.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
