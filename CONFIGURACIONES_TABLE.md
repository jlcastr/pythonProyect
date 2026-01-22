# Tabla de Configuraciones

## Descripción
La tabla `configuraciones` almacena las configuraciones principales del sistema de ventas S&M.

## Estructura de la Tabla

| Campo       | Tipo    | Descripción                                    | Valor por Defecto |
|-------------|---------|------------------------------------------------|-------------------|
| id          | INTEGER | Clave primaria autoincremental                 | -                 |
| IsLocal     | BOOLEAN | Indica si el sistema opera en modo local      | 0 (False)         |
| IsWeb       | BOOLEAN | Indica si el sistema opera en modo web        | 0 (False)         |
| IsPremiun   | BOOLEAN | Indica si tiene características premium       | 0 (False)         |
| IsGenerico  | BOOLEAN | Indica si usa configuración genérica          | 1 (True)          |
| IsJoyeria   | BOOLEAN | Indica si está configurado para joyería      | 0 (False)         |

## SQL de Creación
```sql
CREATE TABLE IF NOT EXISTS configuraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    IsLocal BOOLEAN NOT NULL DEFAULT 0,
    IsWeb BOOLEAN NOT NULL DEFAULT 0,
    IsPremiun BOOLEAN NOT NULL DEFAULT 0,
    IsGenerico BOOLEAN NOT NULL DEFAULT 1,
    IsJoyeria BOOLEAN NOT NULL DEFAULT 0
);
```

## Funciones de API Disponibles

### get_configuraciones()
Obtiene la configuración actual del sistema.

**Retorna:**
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "IsLocal": false,
        "IsWeb": false,
        "IsPremiun": false,
        "IsGenerico": true,
        "IsJoyeria": false
    }
}
```

### update_configuraciones(configuraciones)
Actualiza la configuración del sistema.

**Parámetros:**
- `configuraciones`: Objeto con los valores booleanos a actualizar

**Ejemplo:**
```javascript
const nuevaConfig = {
    'IsLocal': true,
    'IsWeb': true,
    'IsPremiun': false,
    'IsGenerico': true,
    'IsJoyeria': false
};

api.update_configuraciones(nuevaConfig);
```

## Configuración por Defecto
Al crear la tabla, se inserta automáticamente un registro con la configuración por defecto:
- IsLocal: False
- IsWeb: False  
- IsPremiun: False
- IsGenerico: True (habilitado por defecto)
- IsJoyeria: False

## Notas de Implementación
- La tabla utiliza valores enteros (0/1) para representar booleanos en SQLite
- Las funciones de API convierten automáticamente entre booleanos de JavaScript/Python y enteros de SQLite
- Solo se mantiene un registro de configuración (el primer registro encontrado)
- Se creó un índice en el campo `id` para optimizar las consultas