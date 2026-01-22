import sqlite3
import os
from datetime import datetime
from cryptography.fernet import Fernet
from .sqlite_utils import db_optimizer

# Clave fija para ejemplo, en producción debe estar en variable de entorno o archivo seguro
FERNET_KEY = b'Ky9D34yPsE_LUzk-nBKX76doGj2IH8Jq7rjDdBGqRSs='
fernet = Fernet(FERNET_KEY)

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

def guardar_email_config(email, password, db_path="config/sales_system.db"):
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Encriptar la contraseña antes de guardar
        encrypted_password = fernet.encrypt(password.encode()).decode()
        
        # Limpiar tabla para asegurar un solo registro
        cursor.execute("DELETE FROM Emails")
        
        # Insertar el nuevo registro
        cursor.execute("INSERT INTO Emails (email, pass, createon, updateon) VALUES (?, ?, ?, ?)", 
                      (email, encrypted_password, now, now))
        
        conn.commit()
        
        # Verificar que solo hay un registro
        cursor.execute("SELECT COUNT(*) FROM Emails")
        count = cursor.fetchone()[0]
        print(f"[EMAIL_CONFIG] Registros en tabla Emails después del guardado: {count}")
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
    """Crear tabla para configuración de títulos con estructura mejorada"""
    with db_optimizer.get_connection() as (conn, cursor):
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='titles'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            # Crear tabla nueva con estructura mejorada
            cursor.execute("""
                CREATE TABLE titles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('sistema', 'reporte', 'ventana')),
                    activo BOOLEAN DEFAULT 1,
                    createon DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updateon DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tipo, activo) -- Solo un registro activo por tipo
                )
            """)
            print("Tabla titles creada con estructura mejorada (usando campo 'tipo')")
        else:
            # Verificar estructura actual
            cursor.execute("PRAGMA table_info(titles)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Si tiene la estructura antigua (isHeader, isReport, isWindow), mantenerla por compatibilidad
            if 'isHeader' in columns and 'tipo' not in columns:
                print("Manteniendo estructura existente por compatibilidad")
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
    Guardar configuración de títulos - Actualiza o inserta según el tipo
    Solo guarda títulos que no estén vacíos
    
    Args:
        titulo_sistema: Título principal del sistema
        titulo_reporte: Título para reportes
        titulo_ventana: Título para ventanas
    """
    # Verificar que al menos uno de los campos tenga contenido
    if not any([titulo_sistema.strip(), titulo_reporte.strip(), titulo_ventana.strip()]):
        print("❌ No se puede guardar: Todos los campos están vacíos")
        return False
    
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        guardados = []
        
        # Títulos a procesar con su tipo correspondiente
        titulos = [
            (titulo_sistema, 'sistema', 1, 0, 0),
            (titulo_reporte, 'reporte', 0, 1, 0),
            (titulo_ventana, 'ventana', 0, 0, 1)
        ]
        
        for titulo, tipo_nombre, is_header, is_report, is_window in titulos:
            if titulo and titulo.strip():  # Solo procesar si no está vacío
                # Verificar si ya existe un registro activo del mismo tipo
                cursor.execute("""
                    SELECT id FROM titles 
                    WHERE isHeader = ? AND isReport = ? AND isWindow = ? AND activo = 1
                """, (is_header, is_report, is_window))
                
                registro_existente = cursor.fetchone()
                
                if registro_existente:
                    # Actualizar el registro existente
                    cursor.execute("""
                        UPDATE titles 
                        SET title = ?, updateon = ? 
                        WHERE id = ?
                    """, (titulo.strip(), now, registro_existente[0]))
                    print(f"✅ Título {tipo_nombre} actualizado: '{titulo.strip()}'")
                    guardados.append(f"{tipo_nombre}: '{titulo.strip()}'")
                else:
                    # Insertar nuevo registro
                    cursor.execute("""
                        INSERT INTO titles (title, isHeader, isReport, isWindow, createon, activo) 
                        VALUES (?, ?, ?, ?, ?, 1)
                    """, (titulo.strip(), is_header, is_report, is_window, now))
                    print(f"✅ Título {tipo_nombre} creado: '{titulo.strip()}'")
                    guardados.append(f"{tipo_nombre}: '{titulo.strip()}'")
            else:
                print(f"⚠️ Título {tipo_nombre} omitido: campo vacío")
        
        if guardados:
            conn.commit()
            print(f"✅ Configuración completada - Guardados: {', '.join(guardados)}")
            return True
        else:
            print("❌ No se guardó ningún título: todos los campos estaban vacíos")
            return False

def guardar_titulo_config_mejorado(titulo_sistema, titulo_reporte, titulo_ventana):
    """
    Versión mejorada - Un registro por tipo usando campo 'tipo' (más eficiente)
    
    Args:
        titulo_sistema: Título principal del sistema
        titulo_reporte: Título para reportes
        titulo_ventana: Título para ventanas
    """
    with db_optimizer.get_connection() as (conn, cursor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verificar si la tabla tiene la estructura nueva
        cursor.execute("PRAGMA table_info(titles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'tipo' in columns:
            # Usar estructura nueva (más eficiente)
            titulos = [
                ('sistema', titulo_sistema),
                ('reporte', titulo_reporte),
                ('ventana', titulo_ventana)
            ]
            
            for tipo, titulo in titulos:
                if titulo.strip():
                    # Desactivar registros anteriores del mismo tipo
                    cursor.execute("UPDATE titles SET activo = 0, updateon = ? WHERE tipo = ? AND activo = 1", (now, tipo))
                    
                    # Insertar nuevo registro
                    cursor.execute("""
                        INSERT INTO titles (title, tipo, createon, activo) 
                        VALUES (?, ?, ?, 1)
                    """, (titulo.strip(), tipo, now))
                    
                    print(f"Título {tipo} guardado: '{titulo.strip()}'")
        else:
            # Usar estructura anterior por compatibilidad
            print("Usando estructura anterior por compatibilidad")
            guardar_titulo_config(titulo_sistema, titulo_reporte, titulo_ventana)
            return
        
        conn.commit()
        print(f"Configuración mejorada completada")

def eliminar_todos_los_titles():
    """
    Elimina todos los registros de la tabla titles
    """
    with db_optimizer.get_connection() as (conn, cursor):
        cursor.execute('DELETE FROM titles')
        registros_eliminados = cursor.rowcount
        conn.commit()
        
        cursor.execute('SELECT COUNT(*) FROM titles')
        registros_restantes = cursor.fetchone()[0]
        
        print(f"Se eliminaron {registros_eliminados} registros de la tabla titles")
        print(f"Registros restantes: {registros_restantes}")
        return registros_eliminados

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

def limpiar_tabla_titles():
    """
    Eliminar todos los registros de la tabla titles
    """
    with db_optimizer.get_connection() as (conn, cursor):
        try:
            cursor.execute("DELETE FROM titles")
            registros_eliminados = cursor.rowcount
            conn.commit()
            print(f"✅ Se eliminaron {registros_eliminados} registros de la tabla titles")
            return True
        except Exception as e:
            print(f"❌ Error al limpiar tabla titles: {e}")
            return False

def resetear_tabla_titles():
    """
    Eliminar todos los registros y resetear el contador de ID
    """
    with db_optimizer.get_connection() as (conn, cursor):
        try:
            cursor.execute("DELETE FROM titles")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='titles'")
            registros_eliminados = cursor.rowcount
            conn.commit()
            print(f"✅ Tabla titles reseteada completamente. Se eliminaron registros y se reinició el contador de ID")
            return True
        except Exception as e:
            print(f"❌ Error al resetear tabla titles: {e}")
            return False
