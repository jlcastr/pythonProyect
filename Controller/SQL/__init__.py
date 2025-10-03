"""
Módulo SQL - Utilidades de base de datos SQLite
Funciones optimizadas para manejo de datos
"""

from .sqlite_utils import (
    db_optimizer,
    guardar_venta_optimizada,
    consulta_ventas_optimizada,
    verificar_rendimiento_db,
    aplicar_optimizaciones_iniciales
)

__all__ = [
    'db_optimizer',
    'guardar_venta_optimizada', 
    'consulta_ventas_optimizada',
    'verificar_rendimiento_db',
    'aplicar_optimizaciones_iniciales'
]