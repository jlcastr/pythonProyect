# Documentación: Tabla de Inventarios

## Descripción General
Tabla diseñada para manejar inventarios tanto de productos genéricos como de joyería, con campos específicos que se adaptan según el tipo de negocio configurado en la tabla `configuraciones`.

## Estructura Detallada de Campos

### 🔹 **Campos Básicos (Obligatorios)**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | INTEGER | Clave primaria autoincremental | 1, 2, 3... |
| `codigo_producto` | TEXT | SKU único del producto | "SKU001", "JOY-ANI-001" |
| `nombre` | TEXT | Nombre comercial del producto | "Anillo de Compromiso", "Laptop HP" |
| `descripcion` | TEXT | Descripción detallada | "Anillo en oro blanco 18k con diamante central" |
| `categoria` | TEXT | Categoría del producto | "Anillos", "Electrónicos", "Collares" |
| `precio_venta` | DECIMAL | Precio de venta al público | 15000.00 |

### 💰 **Campos de Precios y Costos**

| Campo | Tipo | Descripción | Uso |
|-------|------|-------------|-----|
| `precio_compra` | DECIMAL | Costo de adquisición | Control de márgenes |
| `precio_mayoreo` | DECIMAL | Precio para mayoristas | Ventas en volumen |
| `margen_ganancia` | DECIMAL | Porcentaje de ganancia | Análisis de rentabilidad |

### 📦 **Campos de Inventario**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `stock_actual` | INTEGER | Cantidad disponible | 25 |
| `stock_minimo` | INTEGER | Alerta de reposición | 5 |
| `stock_maximo` | INTEGER | Límite máximo | 100 |
| `ubicacion` | TEXT | Ubicación física | "Estante A-1", "Vitrina Principal" |

### 💎 **Campos Específicos para Joyería**

#### Material y Metal
| Campo | Tipo | Descripción | Valores Típicos |
|-------|------|-------------|-----------------|
| `tipo_metal` | TEXT | Tipo de metal | Oro, Plata, Platino, Acero |
| `pureza_metal` | TEXT | Pureza del metal | 14k, 18k, 24k, 925 |
| `peso_metal` | DECIMAL | Peso en gramos | 3.45 |

#### Piedras Preciosas
| Campo | Tipo | Descripción | Valores |
|-------|------|-------------|---------|
| `tiene_piedras` | BOOLEAN | Si contiene piedras | 0 = No, 1 = Sí |
| `tipo_piedra_principal` | TEXT | Tipo de piedra principal | Diamante, Esmeralda, Rubí |
| `quilates_principal` | DECIMAL | Quilates de la piedra | 0.50, 1.00, 2.25 |
| `calidad_piedra` | TEXT | Calidad gemológica | VVS1, VS1, SI1, SI2 |
| `color_piedra` | TEXT | Color de la piedra | D, E, F, G, H, I, J |

#### Características Físicas
| Campo | Tipo | Descripción | Ejemplos |
|-------|------|-------------|----------|
| `talla` | TEXT | Talla (anillos) | 6, 7, 8, 9 |
| `genero` | TEXT | Género objetivo | Masculino, Femenino, Unisex |
| `tipo_joya` | TEXT | Tipo de joyería | Anillo, Collar, Pulsera, Aretes |
| `estilo` | TEXT | Estilo de diseño | Clásico, Moderno, Vintage |

### 📋 **Campos de Certificación**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `certificado` | BOOLEAN | Tiene certificación | 1 = Certificado |
| `laboratorio_certificacion` | TEXT | Laboratorio emisor | GIA, AGS, SSEF |
| `numero_certificado` | TEXT | Número del certificado | "GIA-12345678" |

### 🖼️ **Campos Multimedia**

| Campo | Tipo | Descripción | Uso |
|-------|------|-------------|-----|
| `imagen_principal` | TEXT | URL imagen principal | Para mostrar en listados |
| `imagenes_adicionales` | TEXT | JSON con más imágenes | Para galerías detalladas |
| `video_producto` | TEXT | URL del video | Demostraciones del producto |

### 🎯 **Campos de Marketing**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `en_promocion` | BOOLEAN | En promoción activa | 1 = En promoción |
| `precio_promocion` | DECIMAL | Precio con descuento | 12000.00 |
| `tags` | TEXT | Etiquetas de búsqueda | "elegante,boda,compromiso" |

## Índices Recomendados

```sql
-- Búsquedas frecuentes
idx_inventarios_codigo      -- Búsqueda por código
idx_inventarios_nombre      -- Búsqueda por nombre
idx_inventarios_categoria   -- Filtrado por categoría
idx_inventarios_activo     -- Productos activos
idx_inventarios_stock      -- Control de inventario
idx_inventarios_precio     -- Filtrado por precio

-- Específicos para joyería
idx_inventarios_tipo_joya  -- Filtrado por tipo de joya
idx_inventarios_metal      -- Filtrado por metal
```

## Configuración Adaptativa

El sistema puede usar diferentes campos según la configuración:

### Modo Genérico (`IsGenerico = 1`)
- Se usan principalmente campos básicos
- Los campos de joyería se ignoran o se ocultan
- Enfoque en stock, precios y categorías generales

### Modo Joyería (`IsJoyeria = 1`)
- Se habilitan todos los campos específicos de joyería
- Validaciones especiales para metales y piedras
- Interfaz especializada para características gemológicas

## Ejemplos de Registros

### Producto Genérico:
```sql
INSERT INTO inventarios (
    codigo_producto, nombre, descripcion, categoria, 
    precio_venta, stock_actual, unidad_medida
) VALUES (
    'ELEC-001', 'Laptop HP Pavilion', 
    'Laptop HP con procesador Intel i5', 'Electrónicos',
    25000.00, 5, 'PZA'
);
```

### Producto de Joyería:
```sql
INSERT INTO inventarios (
    codigo_producto, nombre, descripcion, categoria,
    precio_venta, stock_actual, tipo_metal, pureza_metal,
    peso_metal, tiene_piedras, tipo_piedra_principal,
    quilates_principal, tipo_joya, genero
) VALUES (
    'JOY-ANI-001', 'Anillo de Compromiso Clásico',
    'Anillo en oro blanco con diamante solitario', 'Anillos',
    45000.00, 1, 'Oro Blanco', '18k',
    3.50, 1, 'Diamante',
    1.00, 'Anillo', 'Femenino'
);
```

## Recomendaciones de Implementación

1. **Validaciones Condicionales**: Crear validaciones que dependan de la configuración del sistema
2. **Interfaz Adaptativa**: Mostrar/ocultar campos según el modo (genérico/joyería)
3. **Búsquedas Especializadas**: Implementar búsquedas específicas para cada modo
4. **Reportes Diferenciados**: Generar reportes adaptados al tipo de inventario
5. **Importación/Exportación**: Crear plantillas diferentes para cada modo