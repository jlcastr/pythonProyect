import sqlite3

def crear_conexion_y_tablas(db_path="sqliteDB.db"):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Crear tabla Emails
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            pass TEXT NOT NULL,
            createon TEXT NOT NULL,
            updateon TEXT
        )
    """)

    # Crear tabla VentaMaster
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VentaMaster (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folio INTEGER NOT NULL UNIQUE,
            fecha_venta TEXT NOT NULL,
            cliente TEXT
        )
    """)

    # Crear tabla ventas_items con relación a VentaMaster
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            fecha_venta TEXT NOT NULL,
            venta_master_id INTEGER,
            FOREIGN KEY (venta_master_id) REFERENCES VentaMaster(id)
        )
    """)

    # Migración: Agregar campo cliente a VentaMaster si no existe
    try:
        # Verificar si la columna cliente ya existe
        cursor.execute("PRAGMA table_info(VentaMaster)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'cliente' not in columns:
            cursor.execute("ALTER TABLE VentaMaster ADD COLUMN cliente TEXT")
            print("Campo 'cliente' agregado a la tabla VentaMaster")
    except sqlite3.Error as e:
        print(f"Error al agregar campo cliente: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_conexion_y_tablas()