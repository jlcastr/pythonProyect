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
import os
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


# ==================== FUNCIONES PARA CONFIGURACIÓN DE LOGOS ====================

def crear_tabla_logos_config():
    """Crear tabla para configuración de logos si no existe"""
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logos_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seccion TEXT NOT NULL UNIQUE,
                archivo_path TEXT NOT NULL,
                archivo_original TEXT,
                fecha_aplicado DATETIME NOT NULL,
                tamaño_kb REAL,
                dimensiones TEXT,
                aplicado_por TEXT,
                activo BOOLEAN DEFAULT 1,
                createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                updateon DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def guardar_logo_config(seccion, archivo_path, archivo_original, tamaño_kb, dimensiones, aplicado_por="Sistema"):
    """
    Guardar o actualizar configuración de logo en base de datos
    
    Args:
        seccion: 'ventanas', 'reportes', 'facturas'
        archivo_path: Ruta donde se guardó el archivo procesado
        archivo_original: Nombre del archivo original seleccionado
        tamaño_kb: Tamaño del archivo en KB
        dimensiones: Dimensiones como string "100x100"
        aplicado_por: Usuario que aplicó el cambio
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verificar si ya existe configuración para esta sección
        cursor.execute("SELECT id FROM logos_config WHERE seccion = ?", (seccion,))
        row = cursor.fetchone()
        
        if row:
            # Actualizar registro existente
            cursor.execute("""
                UPDATE logos_config 
                SET archivo_path=?, archivo_original=?, fecha_aplicado=?, 
                    tamaño_kb=?, dimensiones=?, aplicado_por=?, updateon=? 
                WHERE seccion=?
            """, (archivo_path, archivo_original, now, tamaño_kb, dimensiones, aplicado_por, now, seccion))
        else:
            # Insertar nuevo registro
            cursor.execute("""
                INSERT INTO logos_config 
                (seccion, archivo_path, archivo_original, fecha_aplicado, tamaño_kb, dimensiones, aplicado_por) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (seccion, archivo_path, archivo_original, now, tamaño_kb, dimensiones, aplicado_por))
        
        conn.commit()

def consultar_logo_config(seccion=None):
    """
    Consultar configuración de logos
    
    Args:
        seccion: Si se especifica, devuelve solo esa sección. Si es None, devuelve todas
    
    Returns:
        dict o list: Configuración de logo(s)
    """
    with db_optimizer.get_connection() as (conn, cursor):
        if seccion:
            cursor.execute("""
                SELECT seccion, archivo_path, archivo_original, fecha_aplicado, 
                       tamaño_kb, dimensiones, aplicado_por, activo
                FROM logos_config WHERE seccion = ? AND activo = 1
            """, (seccion,))
            row = cursor.fetchone()
            if row:
                return {
                    'seccion': row[0],
                    'archivo_path': row[1], 
                    'archivo_original': row[2],
                    'fecha_aplicado': row[3],
                    'tamaño_kb': row[4],
                    'dimensiones': row[5],
                    'aplicado_por': row[6],
                    'activo': row[7]
                }
            return None
        else:
            cursor.execute("""
                SELECT seccion, archivo_path, archivo_original, fecha_aplicado,
                       tamaño_kb, dimensiones, aplicado_por, activo
                FROM logos_config WHERE activo = 1
                ORDER BY seccion
            """)
            rows = cursor.fetchall()
            return [{
                'seccion': row[0],
                'archivo_path': row[1],
                'archivo_original': row[2], 
                'fecha_aplicado': row[3],
                'tamaño_kb': row[4],
                'dimensiones': row[5],
                'aplicado_por': row[6],
                'activo': row[7]
            } for row in rows]

def obtener_historial_logos(seccion=None, limit=10):
    """
    Obtener historial de cambios de logos
    
    Args:
        seccion: Filtrar por sección específica (opcional)
        limit: Límite de registros a devolver
    
    Returns:
        list: Lista de cambios históricos
    """
    with db_optimizer.get_connection() as (conn, cursor):
        if seccion:
            cursor.execute("""
                SELECT seccion, archivo_original, fecha_aplicado, aplicado_por, dimensiones, tamaño_kb
                FROM logos_config 
                WHERE seccion = ?
                ORDER BY fecha_aplicado DESC
                LIMIT ?
            """, (seccion, limit))
        else:
            cursor.execute("""
                SELECT seccion, archivo_original, fecha_aplicado, aplicado_por, dimensiones, tamaño_kb
                FROM logos_config 
                ORDER BY fecha_aplicado DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        return [{
            'seccion': row[0],
            'archivo_original': row[1],
            'fecha_aplicado': row[2],
            'aplicado_por': row[3],
            'dimensiones': row[4],
            'tamaño_kb': row[5]
        } for row in rows]

def eliminar_logo_config(seccion):
    """
    Marcar configuración de logo como inactiva (soft delete)
    
    Args:
        seccion: Sección del logo a desactivar
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE logos_config 
            SET activo = 0, updateon = ?
            WHERE seccion = ?
        """, (now, seccion))
        conn.commit()


# ==================== FUNCIONES PARA CONFIGURACIÓN DE TÍTULOS ====================

def crear_tabla_titles():
    """Crear tabla para configuración de títulos si no existe"""
    with db_optimizer.get_connection() as (conn, cursor):
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='titles'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            # Crear tabla nueva con todas las columnas
            cursor.execute("""
                CREATE TABLE titles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    isHeader BOOLEAN DEFAULT 0,
                    isReport BOOLEAN DEFAULT 0,
                    isWindow BOOLEAN DEFAULT 0,
                    activo BOOLEAN DEFAULT 1,
                    createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updateon DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tabla titles creada con éxito")
        else:
            # Verificar si necesita agregar columnas faltantes
            cursor.execute("PRAGMA table_info(titles)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'activo' not in columns:
                cursor.execute("ALTER TABLE titles ADD COLUMN activo BOOLEAN DEFAULT 1")
                print("Columna 'activo' agregada a la tabla titles")
                
            if 'createon' not in columns:
                cursor.execute("ALTER TABLE titles ADD COLUMN createon DATETIME DEFAULT CURRENT_TIMESTAMP")
                print("Columna 'createon' agregada a la tabla titles")
                
            if 'updateon' not in columns:
                cursor.execute("ALTER TABLE titles ADD COLUMN updateon DATETIME DEFAULT CURRENT_TIMESTAMP")
                print("Columna 'updateon' agregada a la tabla titles")
        
        conn.commit()

def guardar_titulo_config(titulo_sistema, titulo_reporte, titulo_ventana):
    """
    Guardar configuración de títulos
    
    Args:
        titulo_sistema: Título principal del sistema
        titulo_reporte: Título para reportes
        titulo_ventana: Título para ventanas
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Desactivar títulos anteriores
        cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE activo = 1", (now,))
        
        # Insertar nuevos títulos
        titulos = [
            (titulo_sistema, 1, 0, 0),  # isHeader = 1
            (titulo_reporte, 0, 1, 0),  # isReport = 1
            (titulo_ventana, 0, 0, 1)   # isWindow = 1
        ]
        
        for titulo, is_header, is_report, is_window in titulos:
            if titulo.strip():  # Solo guardar si no está vacío
                cursor.execute("""
                    INSERT INTO titles (title, isHeader, isReport, isWindow, createon, activo) 
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (titulo.strip(), is_header, is_report, is_window, now))
        
        conn.commit()
        print(f"Títulos guardados: Sistema='{titulo_sistema}', Reporte='{titulo_reporte}', Ventana='{titulo_ventana}'")

def consultar_titulo_config():
    """
    Consultar configuración actual de títulos
    
    Returns:
        dict: Títulos configurados por tipo
    """
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            SELECT title, isHeader, isReport, isWindow
            FROM titles 
            WHERE activo = 1
            ORDER BY createon DESC
        """)
        rows = cursor.fetchall()
        
        titulos = {
            'sistema': '',
            'reporte': '',
            'ventana': ''
        }
        
        for row in rows:
            titulo, is_header, is_report, is_window = row
            if is_header:
                titulos['sistema'] = titulo
            elif is_report:
                titulos['reporte'] = titulo
            elif is_window:
                titulos['ventana'] = titulo
        
        return titulos

def obtener_historial_titulos(limit=10):
    """
    Obtener historial de cambios de títulos
    
    Args:
        limit: Límite de registros a devolver
    
    Returns:
        list: Lista de cambios históricos
    """
    with db_optimizer.get_connection() as (conn, cursor):
        try:
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles 
                ORDER BY createon DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [{
                'titulo': row[0],
                'tipo': 'Sistema' if row[1] else 'Reporte' if row[2] else 'Ventana' if row[3] else 'Desconocido',
                'fecha_aplicado': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error al obtener historial de títulos: {e}")
            return []
    """Crear tabla para configuración de títulos si no existe"""
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isHeader BOOLEAN DEFAULT 0,
                isReport BOOLEAN DEFAULT 0,
                isWindow BOOLEAN DEFAULT 0,
                activo BOOLEAN DEFAULT 1,
                createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                updateon DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def guardar_titulo_config(titulo_sistema, titulo_reporte, titulo_ventana):
    """
    Guardar configuración de títulos
    
    Args:
        titulo_sistema: Título principal del sistema
        titulo_reporte: Título para reportes
        titulo_ventana: Título para ventanas
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verificar si la columna activo existe
        cursor.execute("PRAGMA table_info(titles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'activo' in columns:
            # Si existe la columna activo, desactivar títulos anteriores
            cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE activo = 1", (now,))
        
        # Insertar nuevos títulos
        titulos = [
            (titulo_sistema, 1, 0, 0),  # isHeader = 1
            (titulo_reporte, 0, 1, 0),  # isReport = 1
            (titulo_ventana, 0, 0, 1)   # isWindow = 1
        ]
        
        for titulo, is_header, is_report, is_window in titulos:
            if titulo.strip():  # Solo guardar si no está vacío
                if 'activo' in columns:
                    cursor.execute("""
                        INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (titulo.strip(), is_header, is_report, is_window, now))
                else:
                    # Sin columna activo, insertar directamente
                    cursor.execute("""
                        INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (titulo.strip(), is_header, is_report, is_window, now))
        
        conn.commit()

def consultar_titulo_config():
    """
    Consultar configuración actual de títulos
    
    Returns:
        dict: Títulos configurados por tipo
    """
    with db_optimizer.get_connection() as (conn, cursor):
        # Primero verificar si la columna activo existe
        cursor.execute("PRAGMA table_info(titles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'activo' in columns:
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow
                FROM titles 
                WHERE activo = 1
                ORDER BY createon DESC
            """)
        else:
            # Si no existe la columna activo, obtener los más recientes
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow
                FROM titles 
                ORDER BY createon DESC
                LIMIT 3
            """)
        
        rows = cursor.fetchall()
        
        titulos = {
            'sistema': '',
            'reporte': '',
            'ventana': ''
        }
        
        for row in rows:
            titulo, is_header, is_report, is_window = row
            if is_header:
                titulos['sistema'] = titulo
            elif is_report:
                titulos['reporte'] = titulo
            elif is_window:
                titulos['ventana'] = titulo
        
        return titulos

def obtener_historial_titulos(limit=10):
    """
    Obtener historial de cambios de títulos
    
    Args:
        limit: Límite de registros a devolver
    
    Returns:
        list: Lista de cambios históricos
    """
    with db_optimizer.get_connection() as (conn, cursor):
        try:
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles 
                ORDER BY createon DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [{
                'titulo': row[0],
                'tipo': 'Sistema' if row[1] else 'Reporte' if row[2] else 'Ventana' if row[3] else 'Desconocido',
                'fecha_aplicado': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error al obtener historial de títulos: {e}")
            return []

def obtener_imagen_logo(seccion):
    """
    Obtener la ruta de la imagen original desde la carpeta Logos
    
    Args:
        seccion: Sección del logo ('ventanas', 'reportes', 'facturas')
    
    Returns:
        str: Ruta del archivo de imagen en Logos/ o None si no existe
    """
    config = consultar_logo_config(seccion)
    if config and config['archivo_path'] and os.path.exists(config['archivo_path']):
        return config['archivo_path']
    return None

def listar_imagenes_logos():
    """
    Listar todas las imágenes guardadas en la carpeta Logos
    
    Returns:
        list: Lista de archivos de imagen disponibles
    """
    logos_dir = "Logos"
    if not os.path.exists(logos_dir):
        return []
    
    extensiones_imagen = ('.png', '.jpg', '.jpeg', '.ico', '.gif', '.bmp')
    imagenes = []
    
    for archivo in os.listdir(logos_dir):
        if archivo.lower().endswith(extensiones_imagen):
            ruta_completa = os.path.join(logos_dir, archivo)
            size_kb = os.path.getsize(ruta_completa) / 1024
            imagenes.append({
                'nombre': archivo,
                'ruta': ruta_completa,
                'tamaño_kb': size_kb,
                'fecha_modificacion': os.path.getmtime(ruta_completa)
            })
    
    # Ordenar por fecha de modificación (más recientes primero)
    imagenes.sort(key=lambda x: x['fecha_modificacion'], reverse=True)
    return imagenes


# ==================== FUNCIONES PARA CONFIGURACIÓN DE TÍTULOS ====================

def crear_tabla_titles():
    """Crear tabla para configuración de títulos si no existe"""
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isHeader BOOLEAN DEFAULT 0,
                isReport BOOLEAN DEFAULT 0,
                isWindow BOOLEAN DEFAULT 0,
                activo BOOLEAN DEFAULT 1,
                createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                updateon DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def guardar_titulo_config(title, isHeader=False, isReport=False, isWindow=False):
    """
    Guardar o actualizar configuración de título
    
    Args:
        title: Texto del título
        isHeader: Si es título principal del sistema
        isReport: Si es título para reportes
        isWindow: Si es título para ventanas
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determinar qué tipo de título es (solo uno puede estar activo por tipo)
        if isHeader:
            # Desactivar otros títulos principales
            cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE isHeader = 1", (now,))
            cursor.execute("""
                INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
                VALUES (?, 1, 0, 0, ?)
            """, (title, now))
        elif isReport:
            # Desactivar otros títulos de reporte
            cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE isReport = 1", (now,))
            cursor.execute("""
                INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
                VALUES (?, 0, 1, 0, ?)
            """, (title, now))
        elif isWindow:
            # Desactivar otros títulos de ventana
            cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE isWindow = 1", (now,))
            cursor.execute("""
                INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
                VALUES (?, 0, 0, 1, ?)
            """, (title, now))
        
        conn.commit()

def consultar_titulo_config(tipo=None):
    """
    Consultar configuración de títulos
    
    Args:
        tipo: 'header', 'report', 'window' o None para todos
    
    Returns:
        dict o list: Configuración de título(s)
    """
    with db_optimizer.get_connection() as (conn, cursor):
        if tipo == 'header':
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles WHERE isHeader = 1 AND activo = 1
                ORDER BY createon DESC LIMIT 1
            """)
        elif tipo == 'report':
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles WHERE isReport = 1 AND activo = 1
                ORDER BY createon DESC LIMIT 1
            """)
        elif tipo == 'window':
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles WHERE isWindow = 1 AND activo = 1
                ORDER BY createon DESC LIMIT 1
            """)
        else:
            cursor.execute("""
                SELECT title, isHeader, isReport, isWindow, createon
                FROM titles WHERE activo = 1
                ORDER BY createon DESC
            """)
        
        if tipo:
            row = cursor.fetchone()
            if row:
                return {
                    'title': row[0],
                    'isHeader': bool(row[1]),
                    'isReport': bool(row[2]),
                    'isWindow': bool(row[3]),
                    'createon': row[4]
                }
            return None
        else:
            rows = cursor.fetchall()
            return [{
                'title': row[0],
                'isHeader': bool(row[1]),
                'isReport': bool(row[2]),
                'isWindow': bool(row[3]),
                'createon': row[4]
            } for row in rows]

def obtener_historial_titulos(limit=10):
    """
    Obtener historial de cambios de títulos
    
    Args:
        limit: Límite de registros a devolver
    
    Returns:
        list: Lista de cambios históricos
    """
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            SELECT title, isHeader, isReport, isWindow, createon, activo
            FROM titles 
            ORDER BY createon DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        return [{
            'title': row[0],
            'isHeader': bool(row[1]),
            'isReport': bool(row[2]),
            'isWindow': bool(row[3]),
            'createon': row[4],
            'activo': bool(row[5])
        } for row in rows]


# ==================== FUNCIONES PARA CONFIGURACIÓN DE TÍTULOS ====================

def crear_tabla_titles():
    """Crear tabla para configuración de títulos si no existe"""
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isHeader BOOLEAN DEFAULT 0,
                isReport BOOLEAN DEFAULT 0,
                isWindow BOOLEAN DEFAULT 0,
                createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                updateon DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def guardar_title_config(title, is_header=False, is_report=False, is_window=False):
    """
    Guardar configuración de título en base de datos
    
    Args:
        title: Texto del título
        is_header: Si es título principal/header
        is_report: Si es título para reportes
        is_window: Si es título para ventanas
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO titles (title, isHeader, isReport, isWindow, createon) 
            VALUES (?, ?, ?, ?, ?)
        """, (title, is_header, is_report, is_window, now))
        
        conn.commit()
        return cursor.lastrowid

def consultar_title_config(is_header=None, is_report=None, is_window=None):
    """
    Consultar configuración de títulos
    
    Args:
        is_header: Filtrar por títulos de header
        is_report: Filtrar por títulos de reportes
        is_window: Filtrar por títulos de ventanas
    
    Returns:
        list: Lista de títulos que coinciden con los filtros
    """
    with db_optimizer.get_connection() as (conn, cursor):
        query = "SELECT id, title, isHeader, isReport, isWindow, createon, updateon FROM titles WHERE 1=1"
        params = []
        
        if is_header is not None:
            query += " AND isHeader = ?"
            params.append(is_header)
        
        if is_report is not None:
            query += " AND isReport = ?"
            params.append(is_report)
        
        if is_window is not None:
            query += " AND isWindow = ?"
            params.append(is_window)
        
        query += " ORDER BY createon DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [{
            'id': row[0],
            'title': row[1],
            'isHeader': bool(row[2]),
            'isReport': bool(row[3]),
            'isWindow': bool(row[4]),
            'createon': row[5],
            'updateon': row[6]
        } for row in rows]

def actualizar_title_config(title_id, title=None, is_header=None, is_report=None, is_window=None):
    """
    Actualizar configuración de título existente
    
    Args:
        title_id: ID del título a actualizar
        title: Nuevo texto del título (opcional)
        is_header: Nuevo valor para isHeader (opcional)
        is_report: Nuevo valor para isReport (opcional)
        is_window: Nuevo valor para isWindow (opcional)
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construir query dinámicamente
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if is_header is not None:
            updates.append("isHeader = ?")
            params.append(is_header)
        
        if is_report is not None:
            updates.append("isReport = ?")
            params.append(is_report)
        
        if is_window is not None:
            updates.append("isWindow = ?")
            params.append(is_window)
        
        if updates:
            updates.append("updateon = ?")
            params.append(now)
            params.append(title_id)
            
            query = f"UPDATE titles SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        
        return False

def eliminar_title_config(title_id):
    """
    Eliminar configuración de título
    
    Args:
        title_id: ID del título a eliminar
    """
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute("DELETE FROM titles WHERE id = ?", (title_id,))
        conn.commit()
        return cursor.rowcount > 0

def obtener_title_actual(tipo):
    """
    Obtener el título actual según el tipo
    
    Args:
        tipo: 'header', 'report', 'window'
    
    Returns:
        str: Título configurado o None si no existe
    """
    tipo_map = {
        'header': 'isHeader',
        'report': 'isReport', 
        'window': 'isWindow'
    }
    
    if tipo not in tipo_map:
        return None
    
    with db_optimizer.get_connection() as (conn, cursor):
        campo = tipo_map[tipo]
        cursor.execute(f"""
            SELECT title FROM titles 
            WHERE {campo} = 1 
            ORDER BY updateon DESC 
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        return row[0] if row else None
