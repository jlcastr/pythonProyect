# Consultar solo el correo almacenado
def consultar_email_config(db_path="config/sales_system.db"):
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("SELECT email FROM Emails LIMIT 1")
        row = cursor.fetchone()
        if row:
            return row[0]
        return None
# Función para obtener email y contraseña desencriptada
def obtener_email_config(db_path="config/sales_system.db"):
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("SELECT email, pass FROM Emails LIMIT 1")
        row = cursor.fetchone()
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
from .sqlite_utils import db_optimizer

# Clave fija para ejemplo, en producción debe estar en variable de entorno o archivo seguro
FERNET_KEY = b'Ky9D34yPsE_LUzk-nBKX76doGj2IH8Jq7rjDdBGqRSs='
fernet = Fernet(FERNET_KEY)

def guardar_email_config(email, password, db_path="config/sales_system.db"):
    with db_optimizer.get_connection() as (conn, cursor):
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
def obtener_siguiente_folio(cursor):
    cursor.execute("SELECT MAX(folio) FROM VentaMaster")
    result = cursor.fetchone()
    return (result[0] + 1) if result[0] else 1


def finalizar_venta(tree, entry_folio, conn, cursor, mostrar_popup_finalizar_venta, venta_actual_id, folio_actual, cliente_nombre=None):
    """Función optimizada para finalizar venta usando transacciones"""
    items = tree.get_children()
    if not items:
        from tkinter import messagebox
        parent = tree.winfo_toplevel()
        messagebox.showwarning("Sin productos", "No hay productos para finalizar la venta.", parent=parent)
        return None, None
    
    from datetime import datetime
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folio = folio_actual if folio_actual else obtener_siguiente_folio(cursor)
    
    try:
        # Iniciar transacción para operación atómica
        cursor.execute("BEGIN TRANSACTION")
        
        # Crear registro en VentaMaster con cliente
        cursor.execute(
            "INSERT INTO VentaMaster (folio, fecha_venta, cliente) VALUES (?, ?, ?)", 
            (folio, fecha_venta, cliente_nombre)
        )
        venta_actual_id = cursor.lastrowid
        
        # Preparar datos para inserción masiva de items
        items_data = []
        for item in items:
            values = tree.item(item, "values")
            descripcion, precio, fecha, folio_tree = values
            precio = precio.replace("$", "")
            items_data.append((descripcion, float(precio), fecha, venta_actual_id))
        
        # Inserción masiva optimizada de items
        cursor.executemany(
            "INSERT INTO ventas_items (descripcion, precio, fecha_venta, venta_master_id) VALUES (?, ?, ?, ?)",
            items_data
        )
        
        # Confirmar transacción
        conn.commit()
        
        mostrar_popup_finalizar_venta()
        
        # Limpiar para nueva venta
        tree.delete(*tree.get_children())
        entry_folio.config(state="normal")
        entry_folio.delete(0, "end")
        entry_folio.config(state="readonly")
        
        return None, None
        
    except sqlite3.Error as e:
        # Revertir cambios en caso de error
        conn.rollback()
        from tkinter import messagebox
        parent = tree.winfo_toplevel()
        messagebox.showerror("Error de base de datos", f"Error al finalizar venta: {e}", parent=parent)
        return None, None
