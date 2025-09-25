# Consultar solo el correo almacenado
def consultar_email_config(db_path="config/sqliteDB.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Emails LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None
# Función para obtener email y contraseña desencriptada
def obtener_email_config(db_path="config/sqliteDB.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT email, pass FROM Emails LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        email, encrypted_password = row
        try:
            password = fernet.decrypt(encrypted_password.encode()).decode()
        except Exception:
            password = None
        return email, password
    return None, None

import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

# Clave fija para ejemplo, en producción debe estar en variable de entorno o archivo seguro
FERNET_KEY = b'Ky9D34yPsE_LUzk-nBKX76doGj2IH8Jq7rjDdBGqRSs='
fernet = Fernet(FERNET_KEY)

def guardar_email_config(email, password, db_path="config/sqliteDB.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Encriptar la contraseña antes de guardar
    encrypted_password = fernet.encrypt(password.encode()).decode()
    # Si ya existe un registro, actualiza; si no, inserta uno nuevo
    cursor.execute("SELECT id FROM Emails LIMIT 1")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE Emails SET email=?, pass=?, updateon=? WHERE id=?", (email, encrypted_password, now, row[0]))
    else:
        cursor.execute("INSERT INTO Emails (email, pass, createon) VALUES (?, ?, ?)", (email, encrypted_password, now))
    conn.commit()
    conn.close()
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
