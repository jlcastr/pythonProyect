"""
Ejemplo de implementación de la tabla inventarios
integrada con el sistema de configuraciones existente
"""

import sqlite3
from datetime import datetime

class InventarioManager:
    """Manejador de inventarios con adaptación según configuración"""
    
    def __init__(self, db_path="config/sales_system.db"):
        self.db_path = db_path
        self.config = self._get_configuration()
    
    def _get_configuration(self):
        """Obtener configuración actual del sistema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM configuraciones LIMIT 1")
            row = cursor.fetchone()
            
            if row:
                return {
                    'IsGenerico': bool(row[4]),
                    'IsJoyeria': bool(row[5])
                }
            return {'IsGenerico': True, 'IsJoyeria': False}
        except:
            return {'IsGenerico': True, 'IsJoyeria': False}
        finally:
            conn.close()
    
    def crear_tabla_inventarios(self):
        """Crear tabla de inventarios"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventarios (
                -- Campos básicos
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_producto TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                categoria TEXT,
                marca TEXT,
                
                -- Precios
                precio_compra DECIMAL(10,2),
                precio_venta DECIMAL(10,2) NOT NULL,
                precio_mayoreo DECIMAL(10,2),
                margen_ganancia DECIMAL(5,2),
                
                -- Inventario
                stock_actual INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER DEFAULT 0,
                stock_maximo INTEGER DEFAULT 0,
                ubicacion TEXT,
                
                -- Medidas
                peso DECIMAL(8,3),
                dimensiones TEXT,
                unidad_medida TEXT DEFAULT 'PZA',
                
                -- Joyería - Material
                tipo_metal TEXT,
                pureza_metal TEXT,
                peso_metal DECIMAL(8,3),
                peso_piedras DECIMAL(8,3),
                
                -- Joyería - Piedras
                tiene_piedras BOOLEAN DEFAULT 0,
                tipo_piedra_principal TEXT,
                quilates_principal DECIMAL(6,2),
                calidad_piedra TEXT,
                color_piedra TEXT,
                corte_piedra TEXT,
                
                -- Joyería - Características
                talla TEXT,
                genero TEXT,
                estilo TEXT,
                tipo_joya TEXT,
                acabado TEXT,
                
                -- Certificación
                certificado BOOLEAN DEFAULT 0,
                laboratorio_certificacion TEXT,
                numero_certificado TEXT,
                fecha_certificacion TEXT,
                
                -- Proveedor
                proveedor TEXT,
                numero_factura_compra TEXT,
                fecha_compra TEXT,
                
                -- Multimedia
                imagen_principal TEXT,
                imagenes_adicionales TEXT,
                
                -- Promociones
                en_promocion BOOLEAN DEFAULT 0,
                precio_promocion DECIMAL(10,2),
                fecha_inicio_promocion TEXT,
                fecha_fin_promocion TEXT,
                
                -- Control
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TEXT NOT NULL,
                fecha_actualizacion TEXT,
                usuario_creacion TEXT
            )
        """)
        
        # Crear índices
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_inventarios_codigo ON inventarios(codigo_producto)",
            "CREATE INDEX IF NOT EXISTS idx_inventarios_nombre ON inventarios(nombre)",
            "CREATE INDEX IF NOT EXISTS idx_inventarios_categoria ON inventarios(categoria)",
            "CREATE INDEX IF NOT EXISTS idx_inventarios_activo ON inventarios(activo)",
            "CREATE INDEX IF NOT EXISTS idx_inventarios_stock ON inventarios(stock_actual)",
            "CREATE INDEX IF NOT EXISTS idx_inventarios_tipo_joya ON inventarios(tipo_joya)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        
        conn.commit()
        conn.close()
        print("Tabla inventarios creada exitosamente")
    
    def agregar_producto_generico(self, datos):
        """Agregar producto genérico"""
        campos_basicos = [
            'codigo_producto', 'nombre', 'descripcion', 'categoria',
            'precio_venta', 'stock_actual', 'marca', 'unidad_medida'
        ]
        
        return self._insertar_producto(datos, campos_basicos)
    
    def agregar_producto_joyeria(self, datos):
        """Agregar producto de joyería"""
        campos_joyeria = [
            'codigo_producto', 'nombre', 'descripcion', 'categoria',
            'precio_venta', 'stock_actual', 'tipo_metal', 'pureza_metal',
            'peso_metal', 'tiene_piedras', 'tipo_piedra_principal',
            'quilates_principal', 'tipo_joya', 'genero', 'talla'
        ]
        
        return self._insertar_producto(datos, campos_joyeria)
    
    def _insertar_producto(self, datos, campos_permitidos):
        """Insertar producto con campos específicos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Filtrar solo campos permitidos
            datos_filtrados = {k: v for k, v in datos.items() if k in campos_permitidos}
            datos_filtrados['fecha_creacion'] = datetime.now().isoformat()
            
            # Construir query dinámico
            columnas = ', '.join(datos_filtrados.keys())
            placeholders = ', '.join(['?' for _ in datos_filtrados])
            
            query = f"INSERT INTO inventarios ({columnas}) VALUES ({placeholders})"
            cursor.execute(query, list(datos_filtrados.values()))
            
            conn.commit()
            producto_id = cursor.lastrowid
            conn.close()
            
            return {"status": "success", "id": producto_id, "message": "Producto agregado exitosamente"}
            
        except sqlite3.IntegrityError as e:
            return {"status": "error", "message": f"Error de integridad: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Error: {e}"}
    
    def buscar_productos(self, filtros=None):
        """Buscar productos con filtros adaptativos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query base
            query = "SELECT * FROM inventarios WHERE activo = 1"
            params = []
            
            # Aplicar filtros según configuración
            if filtros:
                if 'categoria' in filtros:
                    query += " AND categoria = ?"
                    params.append(filtros['categoria'])
                
                if 'nombre' in filtros:
                    query += " AND nombre LIKE ?"
                    params.append(f"%{filtros['nombre']}%")
                
                # Filtros específicos de joyería solo si está habilitado
                if self.config['IsJoyeria']:
                    if 'tipo_joya' in filtros:
                        query += " AND tipo_joya = ?"
                        params.append(filtros['tipo_joya'])
                    
                    if 'tipo_metal' in filtros:
                        query += " AND tipo_metal = ?"
                        params.append(filtros['tipo_metal'])
            
            cursor.execute(query, params)
            productos = cursor.fetchall()
            conn.close()
            
            return {"status": "success", "data": productos}
            
        except Exception as e:
            return {"status": "error", "message": f"Error en búsqueda: {e}"}
    
    def get_campos_visibles(self):
        """Obtener campos que deben ser visibles según configuración"""
        campos_basicos = [
            'codigo_producto', 'nombre', 'descripcion', 'categoria',
            'precio_venta', 'stock_actual', 'marca'
        ]
        
        campos_joyeria = [
            'tipo_metal', 'pureza_metal', 'peso_metal', 'tipo_joya',
            'tiene_piedras', 'quilates_principal', 'talla'
        ]
        
        if self.config['IsJoyeria']:
            return campos_basicos + campos_joyeria
        else:
            return campos_basicos

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del manejador
    inventario = InventarioManager()
    
    # Crear tabla
    inventario.crear_tabla_inventarios()
    
    # Ejemplo producto genérico
    producto_generico = {
        'codigo_producto': 'GEN-001',
        'nombre': 'Laptop Dell',
        'descripcion': 'Laptop para oficina',
        'categoria': 'Electrónicos',
        'precio_venta': 15000.00,
        'stock_actual': 10,
        'marca': 'Dell',
        'unidad_medida': 'PZA'
    }
    
    # Ejemplo producto joyería
    producto_joyeria = {
        'codigo_producto': 'JOY-001',
        'nombre': 'Anillo de Oro',
        'descripcion': 'Anillo clásico en oro amarillo',
        'categoria': 'Anillos',
        'precio_venta': 8500.00,
        'stock_actual': 1,
        'tipo_metal': 'Oro Amarillo',
        'pureza_metal': '14k',
        'peso_metal': 2.5,
        'tipo_joya': 'Anillo',
        'genero': 'Unisex',
        'talla': '7'
    }
    
    # Agregar productos según configuración
    if inventario.config['IsGenerico']:
        result = inventario.agregar_producto_generico(producto_generico)
        print(f"Producto genérico: {result}")
    
    if inventario.config['IsJoyeria']:
        result = inventario.agregar_producto_joyeria(producto_joyeria)
        print(f"Producto joyería: {result}")
    
    # Mostrar campos visibles
    campos = inventario.get_campos_visibles()
    print(f"Campos visibles según configuración: {campos}")