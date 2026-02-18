import sqlite3

def crear_conexion_y_tablas(db_path="sales_system.db"):

    conn = sqlite3.connect(db_path, check_same_thread=False)
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

    # Crear tabla configuraciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuraciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            IsLocal BOOLEAN NOT NULL DEFAULT 0,
            IsWeb BOOLEAN NOT NULL DEFAULT 0,
            IsPremiun BOOLEAN NOT NULL DEFAULT 0,
            IsGenerico BOOLEAN NOT NULL DEFAULT 1,
            IsJoyeria BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Crear tabla TipoMercancia
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TipoMercancia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_mercancia TEXT NOT NULL,
            descripcion TEXT,
            categoria_general TEXT NOT NULL,
            activo BOOLEAN DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insertar configuración por defecto si la tabla está vacía
    try:
        cursor.execute("SELECT COUNT(*) FROM configuraciones")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("""
                INSERT INTO configuraciones (IsLocal, IsWeb, IsPremiun, IsGenerico, IsJoyeria) 
                VALUES (0, 0, 0, 1, 0)
            """)
            print("Configuración por defecto creada")
    except sqlite3.Error as e:
        print(f"Error al crear configuración por defecto: {e}")

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

    # Optimizaciones de rendimiento
    try:
        # Crear índices para mejorar rendimiento de consultas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventamaster_fecha ON VentaMaster(fecha_venta)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventamaster_cliente ON VentaMaster(cliente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventamaster_folio ON VentaMaster(folio)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventaitems_venta_master ON ventas_items(venta_master_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventaitems_fecha ON ventas_items(fecha_venta)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_configuraciones_id ON configuraciones(id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipomercancia_categoria ON TipoMercancia(categoria_general)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipomercancia_activo ON TipoMercancia(activo)")
        
        # Configuraciones de rendimiento para SQLite
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging para mejor concurrencia
        cursor.execute("PRAGMA cache_size=10000")  # Aumentar caché a ~40MB
        cursor.execute("PRAGMA synchronous=NORMAL")  # Balance entre seguridad y velocidad
        cursor.execute("PRAGMA temp_store=MEMORY")  # Usar memoria para tablas temporales
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB de memoria mapeada
        
        print("Índices y optimizaciones aplicadas exitosamente")
    except sqlite3.Error as e:
        print(f"Error al aplicar optimizaciones: {e}")

    conn.commit()
    conn.close()

def obtener_conexion(db_path="sales_system.db"):
    """
    Obtener conexión a la base de datos SQLite
    
    Args:
        db_path (str): Ruta a la base de datos
        
    Returns:
        sqlite3.Connection: Conexión a la base de datos
    """
    try:
        # Crear las tablas si no existen
        crear_conexion_y_tablas(db_path)
        
        # Establecer conexión con check_same_thread=False para permitir uso en múltiples threads
        conn = sqlite3.connect(db_path, check_same_thread=False)
        
        # Configurar la conexión para optimizar rendimiento
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA foreign_keys=ON")  # Habilitar claves foráneas
        
        return conn
        
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def obtener_cursor(db_path="sales_system.db"):
    """
    Obtener cursor de la base de datos
    
    Args:
        db_path (str): Ruta a la base de datos
        
    Returns:
        sqlite3.Cursor: Cursor de la base de datos
    """
    try:
        conn = obtener_conexion(db_path)
        if conn:
            return conn.cursor()
        return None
    except Exception as e:
        print(f"Error obteniendo cursor: {e}")
        return None

if __name__ == "__main__":
    crear_conexion_y_tablas()