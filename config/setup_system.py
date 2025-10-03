#!/usr/bin/env python3
"""
Script simple para configuración inicial del sistema
Ejecutar una sola vez después de la instalación
"""

if __name__ == "__main__":
    try:
        from Controller.SQL.sqlite_utils import aplicar_optimizaciones_iniciales
        
        print("🛠️  CONFIGURACIÓN INICIAL - Sistema de Ventas")
        print("="*50)
        
        if aplicar_optimizaciones_iniciales():
            print("\n🎉 ¡Sistema configurado y optimizado!")
            print("Puedes comenzar a usar la aplicación.")
        else:
            print("❌ Error en la configuración inicial")
            
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Asegúrate de ejecutar desde el directorio raíz del proyecto")