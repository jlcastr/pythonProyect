#!/usr/bin/env python3
"""
Script de prueba para el plugin de impresora térmica
"""

import sys
import os
from datetime import datetime

# Agregar el directorio padre al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from Controller.plugins.printer_plugin import printer_plugin, setup_printer, print_sale_receipt, print_test_page
    print("✅ Plugin importado correctamente")
except ImportError as e:
    print(f"❌ Error importando plugin: {e}")
    sys.exit(1)

def test_printer_plugin():
    """Probar funcionalidades del plugin"""
    
    print("\n🖨️  PRUEBA DEL PLUGIN DE IMPRESORA TÉRMICA")
    print("=" * 50)
    
    # 1. Verificar estado inicial
    print("\n1. Estado inicial:")
    status = printer_plugin.get_status()
    print(f"   Conectado: {status['connected']}")
    print(f"   ESC/POS disponible: {status['escpos_available']}")
    
    # 2. Detectar impresoras USB
    print("\n2. Detección de impresoras USB:")
    usb_printers = printer_plugin.detect_usb_printers()
    if usb_printers:
        print(f"   Encontradas {len(usb_printers)} impresoras:")
        for printer in usb_printers:
            print(f"   - {printer['name']} ({printer['vendor_id']}:{printer['product_id']})")
    else:
        print("   No se encontraron impresoras USB o ESC/POS no disponible")
    
    # 3. Conectar a archivo de prueba
    print("\n3. Conectando a archivo de prueba...")
    test_file = 'printer_test_output.bin'
    if setup_printer('file', filepath=test_file):
        print(f"   ✅ Conectado a {test_file}")
        
        # 4. Imprimir página de prueba
        print("\n4. Imprimiendo página de prueba...")
        if print_test_page():
            print("   ✅ Página de prueba impresa")
            
            # Mostrar contenido del archivo si es texto legible
            try:
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if content.strip():
                    print("   📄 Contenido generado:")
                    print("   " + "─" * 40)
                    for line in content.split('\n')[:10]:  # Mostrar solo las primeras 10 líneas
                        if line.strip():
                            print(f"   {line}")
                    if len(content.split('\n')) > 10:
                        print("   [...más líneas...]")
                    print("   " + "─" * 40)
            except:
                print("   📄 Archivo binario generado correctamente")
        else:
            print("   ❌ Error imprimiendo página de prueba")
        
        # 5. Imprimir recibo de venta de prueba
        print("\n5. Imprimiendo recibo de venta de prueba...")
        test_items = [
            {'descripcion': 'Anillo Oro 18K', 'precio': 1500.00, 'cantidad': 1},
            {'descripcion': 'Collar Plata 925', 'precio': 850.50, 'cantidad': 2},
            {'descripcion': 'Aretes Diamante', 'precio': 2200.75, 'cantidad': 1}
        ]
        
        if print_sale_receipt('SM-001', 'María García', test_items):
            print("   ✅ Recibo de venta impreso")
        else:
            print("   ❌ Error imprimiendo recibo de venta")
        
        # 6. Probar reporte de inventario
        print("\n6. Imprimiendo reporte de inventario...")
        inventory_data = [
            {'codigo': 'AN001', 'descripcion': 'Anillo Pandora', 'stock': 5, 'precio': 1250.00},
            {'codigo': 'CO002', 'descripcion': 'Collar Tiffany', 'stock': 2, 'precio': 3500.00},
            {'codigo': 'PU003', 'descripcion': 'Pulsera Cartier', 'stock': 3, 'precio': 2800.00}
        ]
        
        if printer_plugin.print_inventory_report(inventory_data):
            print("   ✅ Reporte de inventario impreso")
        else:
            print("   ❌ Error imprimiendo reporte de inventario")
        
        # 7. Desconectar
        print("\n7. Desconectando...")
        if printer_plugin.disconnect():
            print("   ✅ Desconectado correctamente")
        else:
            print("   ❌ Error desconectando")
    
    else:
        print("   ❌ Error conectando a archivo de prueba")
    
    print("\n🔄 Prueba completada")
    
    # Información adicional
    print("\n📋 INFORMACIÓN DEL PLUGIN:")
    print("   - Soporta conexiones USB, Red, Serial y Archivo")
    print("   - Compatible con impresoras ESC/POS (Epson, Star, ZJ, etc.)")
    print("   - Funciones: recibos, reportes, páginas de prueba")
    print("   - Configuración personalizable de ancho y opciones")
    
    print("\n📦 INSTALACIÓN DE DEPENDENCIAS:")
    print("   pip install python-escpos pyusb pyserial Pillow")
    print("   o usar: pip install -r Controller/plugins/requirements_printer.txt")
    
    print("\n🔧 USO BÁSICO:")
    print("   from Controller.plugins import printer_plugin, setup_printer")
    print("   setup_printer('usb', vendor_id=0x04b8, product_id=0x0202)")
    print("   printer_plugin.print_test()")

if __name__ == "__main__":
    test_printer_plugin()