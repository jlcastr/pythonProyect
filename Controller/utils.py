"""Funciones utilitarias para la lógica de interfaz y validaciones."""
import re
from tkinter import messagebox
from datetime import datetime
from .db_operations import obtener_siguiente_folio, finalizar_venta

def validar_decimal(texto):
    if texto == "":
        return True
    patron = r"^\d{0,6}(\.\d{0,2})?$"
    return re.match(patron, texto) is not None

def agregar_producto(entry_descripcion, entry_precio, entry_folio, tree, folio_actual, cursor):
    import tkinter as tk
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    if not descripcion or not precio:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.", parent=entry_descripcion.winfo_toplevel())
        return folio_actual
    try:
        precio_decimal = float(precio)
        if precio_decimal < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Precio inválido", "El precio debe ser un número decimal positivo.", parent=entry_precio.winfo_toplevel())
        return folio_actual
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Si no hay folio actual, generar uno
    if folio_actual is None:
        folio_actual = obtener_siguiente_folio(cursor)
        entry_folio.config(state="normal")
        entry_folio.delete(0, tk.END)
        entry_folio.insert(0, str(folio_actual))
        entry_folio.config(state="readonly")
    # Insertar en Treeview (solo en memoria)
    tree.insert("", tk.END, values=(descripcion, f"${precio_decimal:.2f}", fecha_venta, folio_actual))
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    return folio_actual

## finalizar_venta ahora se importa desde db_operations

def popup_imprimir_nota(imprimir):
    # No necesita tk
    imprimir()

def mostrar_popup_finalizar_venta(root, popup_imprimir_nota):
    import tkinter as tk
    popup = tk.Toplevel(root)
    popup.title("Finalizar venta")
    popup.geometry("350x150")
    popup.resizable(False, False)
    label = tk.Label(popup, text="¿Desea imprimir la nota de venta?", pady=20)
    label.pack()
    frame = tk.Frame(popup)
    frame.pack(pady=10)
    btn_imprimir = tk.Button(frame, text="Imprimir", width=12, command=lambda: [popup.destroy(), popup_imprimir_nota()])
    btn_imprimir.pack(side="left", padx=10)
    btn_no = tk.Button(frame, text="No", width=12, command=popup.destroy)
    btn_no.pack(side="left", padx=10)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)

def cancelar(tree, entry_descripcion, entry_precio, entry_folio):
    import tkinter as tk
    tree.delete(*tree.get_children())
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_folio.config(state="normal")
    import tkinter as tk
    entry_folio.delete(0, tk.END)
    entry_folio.config(state="readonly")
    return None, None

def imprimir(cursor, mostrar_popup_sin_productos):
    cursor.execute("SELECT MAX(id) FROM VentaMaster")
    venta_id = cursor.fetchone()[0]
    if venta_id:
        cursor.execute("""
            SELECT ventas_items.descripcion, ventas_items.precio, ventas_items.fecha_venta, VentaMaster.folio
            FROM ventas_items
            JOIN VentaMaster ON ventas_items.venta_master_id = VentaMaster.id
            WHERE ventas_items.venta_master_id = ?
        """, (venta_id,))
        productos = cursor.fetchall()
        if productos:
            print("Nota de venta:")
            for prod in productos:
                print(f"Descripción: {prod[0]}, Precio: ${prod[1]:.2f}, Fecha de venta: {prod[2]}, Folio: {prod[3]}")
            return
    mostrar_popup_sin_productos()

def limpiar_todo(tree):
    tree.delete(*tree.get_children())

def eliminar_seleccionado(tree):
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)
    else:
        parent = tree.winfo_toplevel()
        messagebox.showinfo("Selecciona un producto", "Debes seleccionar un producto para eliminar.", parent=parent)

def modificar_seleccionado(tree, entry_descripcion, entry_precio):
    import tkinter as tk
    selected = tree.selection()
    if selected:
        item = selected[0]
        values = tree.item(item, "values")
        descripcion, precio, fecha_venta, folio = values
        precio = precio.replace("$", "")
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, descripcion)
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, precio)
        tree.delete(item)
    else:
        messagebox.showinfo("Selecciona un producto", "Debes seleccionar un producto para modificar.", parent=entry_descripcion.winfo_toplevel())

def mostrar_popup_sin_productos(root):
    import tkinter as tk
    import tkinter as tk
    popup = tk.Toplevel(root)
    popup.title("Sin productos")
    popup.geometry("300x120")
    popup.resizable(False, False)
    label = tk.Label(popup, text="No hay productos para imprimir.", pady=20)
    label.pack()
    btn_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy)
    btn_cerrar.pack(pady=10)
    popup.transient(root)
    popup.grab_set()