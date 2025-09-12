
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
    # Estilo personalizado para Treeview del reporte
    style = ttk.Style()
    style.theme_use("default")
    style.configure("report.Treeview",
                    background="#ffffff",
                    foreground="#333",
                    rowheight=24,
                    fieldbackground="#ffffff",
                    font=("Segoe UI", 10))
    style.configure("report.Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#4a90e2",
                    foreground="white")
    style.map("report.Treeview",
              background=[('selected', '#a7c7e7')])
    style.layout("report.Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'})
    ])
    style.configure("report.Treeview", borderwidth=0)
    style.map("report.Treeview.Heading",
              background=[('active', '#357ab8')])

    def cargar_ventas():
        lista_ventas.delete(0, tk.END)
        cursor.execute("SELECT id, fecha_venta FROM VentaMaster ORDER BY fecha_venta DESC")
        for venta in cursor.fetchall():
            lista_ventas.insert(tk.END, f"Fecha: {venta[1]}")

    def mostrar_resumen(event):
        seleccion = lista_ventas.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        cursor.execute("SELECT id FROM VentaMaster ORDER BY fecha_venta DESC")
        venta_id = cursor.fetchall()[idx][0]
        for row in tree_resumen.get_children():
            tree_resumen.delete(row)
        cursor.execute("""
            SELECT descripcion, precio, fecha_venta
            FROM ventas_items
            WHERE venta_master_id = ?
        """, (venta_id,))
        for item in cursor.fetchall():
            tree_resumen.insert("", tk.END, values=item)

    # Filtro de fechas en la parte superior izquierda
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(side="top", anchor="nw", padx=10, pady=(10,0), fill="x")
    tk.Label(frame_filtros, text="Fecha inicio:").pack(side="left")
    entry_inicio = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_inicio.pack(side="left", padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").pack(side="left")
    entry_fin = DateEntry(frame_filtros, width=12, date_pattern="yyyy-mm-dd")
    entry_fin.pack(side="left", padx=5)

    # Botón Descargar PDF en la parte superior derecha
    def descargar_pdf():
        from tkinter import messagebox
        messagebox.showinfo("Descargar PDF", "Función de descarga de PDF (por implementar)")
    btn_pdf = tk.Button(frame_filtros, text="Descargar PDF", command=descargar_pdf, bg="#357ab8", fg="white")
    btn_pdf.pack(side="right", padx=10)
    def filtrar_ventas():
        from tkinter import messagebox
        lista_ventas.delete(0, tk.END)
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
        query = "SELECT id, fecha_venta FROM VentaMaster"
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
        for venta in cursor.execute(query, params):
            lista_ventas.insert(tk.END, f"Fecha: {venta[1]}")
    btn_filtrar = tk.Button(frame_filtros, text="Filtrar", command=filtrar_ventas)
    btn_filtrar.pack(side="left", padx=10)

    # Frame izquierdo: lista de ventas
    frame_izq = tk.Frame(root)
    frame_izq.pack(side="left", fill="y", padx=10, pady=10)

    lista_ventas = tk.Listbox(frame_izq, width=35, height=25)
    lista_ventas.pack(fill="y", expand=True)
    lista_ventas.bind("<<ListboxSelect>>", mostrar_resumen)

    # Frame derecho: resumen de la venta seleccionada
    frame_der = tk.Frame(root)
    frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Botón Imprimir en la parte superior derecha
    def imprimir_reporte():
        # Aquí puedes agregar la lógica de impresión, por ahora solo muestra un mensaje
        from tkinter import messagebox
        messagebox.showinfo("Imprimir", "Función de impresión de reporte")

    btn_imprimir = tk.Button(frame_der, text="Imprimir", command=imprimir_reporte, bg="#357ab8", fg="white")
    btn_imprimir.pack(anchor="ne", padx=5, pady=5)

    label_resumen = tk.Label(frame_der, text="Resumen de la venta seleccionada:")
    label_resumen.pack()

    tree_resumen = ttk.Treeview(frame_der, columns=("descripcion", "precio", "fecha_venta"), show="headings", height=20)
    tree_resumen.heading("descripcion", text="Descripción")
    tree_resumen.heading("precio", text="Precio")
    tree_resumen.heading("fecha_venta", text="Fecha de venta")
    tree_resumen.column("descripcion", width=200)
    tree_resumen.column("precio", width=80, anchor="center")
    tree_resumen.column("fecha_venta", width=150, anchor="center")
    tree_resumen.pack(fill="both", expand=True)

    cargar_ventas()
    # Actualizar filtro al abrir
    filtrar_ventas()
    # No mainloop() aquí, solo cerrar conexión al cerrar la ventana
    def on_close():
        conn.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)