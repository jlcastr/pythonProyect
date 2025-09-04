def obtener_siguiente_folio(cursor):
    cursor.execute("SELECT MAX(folio) FROM VentaMaster")
    result = cursor.fetchone()
    return (result[0] + 1) if result[0] else 1


def finalizar_venta(tree, entry_folio, conn, cursor, mostrar_popup_finalizar_venta, venta_actual_id, folio_actual):
    items = tree.get_children()
    if not items:
        from tkinter import messagebox
        parent = tree.winfo_toplevel()
        messagebox.showwarning("Sin productos", "No hay productos para finalizar la venta.", parent=parent)
        return None, None
    from datetime import datetime
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folio = folio_actual if folio_actual else obtener_siguiente_folio(cursor)
    # Crear registro en VentaMaster
    cursor.execute("INSERT INTO VentaMaster (folio, fecha_venta) VALUES (?, ?)", (folio, fecha_venta))
    venta_actual_id = cursor.lastrowid
    conn.commit()
    # Insertar los productos en ventas_items
    for item in items:
        values = tree.item(item, "values")
        descripcion, precio, fecha, folio_tree = values
        precio = precio.replace("$", "")
        cursor.execute(
            "INSERT INTO ventas_items (descripcion, precio, fecha_venta, venta_master_id) VALUES (?, ?, ?, ?)",
            (descripcion, float(precio), fecha, venta_actual_id)
        )
    conn.commit()
    mostrar_popup_finalizar_venta()
    # Limpiar para nueva venta
    tree.delete(*tree.get_children())
    entry_folio.config(state="normal")
    entry_folio.delete(0, "end")
    entry_folio.config(state="readonly")
    return None, None
