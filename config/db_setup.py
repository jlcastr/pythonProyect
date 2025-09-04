import sqlite3

def crear_conexion_y_tablas(db_path="sqliteDB.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla VentaMaster
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VentaMaster (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folio INTEGER NOT NULL UNIQUE,
            fecha_venta TEXT NOT NULL
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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_conexion_y_tablas()