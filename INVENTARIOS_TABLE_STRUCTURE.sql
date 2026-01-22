-- Tabla de inventarios completa para sistema genérico y joyería
-- Compatible con SQLite y otros motores de base de datos

CREATE TABLE IF NOT EXISTS inventarios (
    -- === CAMPOS BÁSICOS ===
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_producto TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    marca TEXT,
    
    -- === PRECIOS Y COSTOS ===
    precio_compra DECIMAL(10,2),
    precio_venta DECIMAL(10,2) NOT NULL,
    precio_mayoreo DECIMAL(10,2),
    margen_ganancia DECIMAL(5,2),
    
    -- === INVENTARIO ===
    stock_actual INTEGER NOT NULL DEFAULT 0,
    
    -- === MEDIDAS Y PESO ===
    peso DECIMAL(8,3),
    dimensiones TEXT,
    unidad_medida TEXT DEFAULT 'PZA',
    
    -- === CAMPOS ESPECÍFICOS JOYERÍA ===
    -- Material
    tipo_metal TEXT,
    pureza_metal TEXT,
    peso_metal DECIMAL(8,3),
    peso_piedras DECIMAL(8,3),
    
    -- Piedras preciosas
    tiene_piedras BOOLEAN DEFAULT 0,
    tipo_piedra_principal TEXT,
    quilates_principal DECIMAL(6,2),
    calidad_piedra TEXT,
    color_piedra TEXT,
    corte_piedra TEXT,
    
    -- Características joyería
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
    
    -- === PROVEEDOR ===
    proveedor TEXT,
    numero_factura_compra TEXT,
    fecha_compra TEXT,
    
    -- === MULTIMEDIA ===
    imagen_principal TEXT,
    imagenes_adicionales TEXT,
    video_producto TEXT,

    
    -- === PROMOCIONES ===
    en_promocion BOOLEAN DEFAULT 0,
    precio_promocion DECIMAL(10,2),
    fecha_inicio_promocion TEXT,
    fecha_fin_promocion TEXT,
    

    codigo_sat TEXT,
    iva_aplicable BOOLEAN DEFAULT 1,
    exento_impuestos BOOLEAN DEFAULT 0,
    IsNacional BOOLEAN DEFAULT 1,
    
    -- === CONTROL DE SISTEMA ===
    activo BOOLEAN DEFAULT 1,
    fecha_creacion TEXT NOT NULL,
    fecha_actualizacion TEXT,
    usuario_creacion TEXT
);

-- === ÍNDICES PARA OPTIMIZACIÓN ===
CREATE INDEX IF NOT EXISTS idx_inventarios_codigo ON inventarios(codigo_producto);
CREATE INDEX IF NOT EXISTS idx_inventarios_nombre ON inventarios(nombre);
CREATE INDEX IF NOT EXISTS idx_inventarios_categoria ON inventarios(categoria);
CREATE INDEX IF NOT EXISTS idx_inventarios_marca ON inventarios(marca);
CREATE INDEX IF NOT EXISTS idx_inventarios_activo ON inventarios(activo);
CREATE INDEX IF NOT EXISTS idx_inventarios_stock ON inventarios(stock_actual);
CREATE INDEX IF NOT EXISTS idx_inventarios_precio ON inventarios(precio_venta);
CREATE INDEX IF NOT EXISTS idx_inventarios_promocion ON inventarios(en_promocion);
CREATE INDEX IF NOT EXISTS idx_inventarios_tipo_joya ON inventarios(tipo_joya);
CREATE INDEX IF NOT EXISTS idx_inventarios_metal ON inventarios(tipo_metal);
CREATE INDEX IF NOT EXISTS idx_inventarios_slug ON inventarios(slug);