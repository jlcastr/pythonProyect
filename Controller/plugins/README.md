# Plugin de Impresora Térmica para Sistema S&M

Plugin completo para manejo de impresoras térmicas compatible con el protocolo ESC/POS utilizado por marcas como Epson, Star Micronics, ZJ, y otras.

## 🚀 Características

- **Múltiples conexiones**: USB, Red (Ethernet), Serial, y archivo de prueba
- **Detección automática**: Busca impresoras USB conectadas
- **Recibos de venta**: Formato profesional con totales y códigos de barras
- **Reportes de inventario**: Listados completos de productos
- **Página de prueba**: Verificación de conectividad y caracteres
- **Configuración flexible**: Ancho, codificación, corte de papel, etc.

## 📦 Instalación

### Dependencias requeridas
```bash
pip install python-escpos pyusb pyserial Pillow
```

O instalar desde el archivo de requisitos:
```bash
pip install -r Controller/plugins/requirements_printer.txt
```

### Permisos USB (Linux/macOS)
```bash
# Agregar usuario al grupo dialout (Linux)
sudo usermod -a -G dialout $USER

# Permisos de dispositivos USB (puede requerir sudo)
sudo chmod 666 /dev/ttyUSB*
```

## 🖨️ Impresoras Compatibles

### USB (Pre-configuradas)
- **Epson TM-T88** (0x04b8:0x0202)
- **Epson TM-T20** (0x04b8:0x0e15)  
- **ZJ-5890K** (0x0fe6:0x811e)
- **Prolific PL2305** (0x067b:0x2305)
- **CH340 Serial** (0x1a86:0x7584)

### Red (Ethernet)
- Cualquier impresora con puerto Ethernet
- Puerto estándar: 9100

### Serial
- Conexión RS232/USB-Serial
- Baudrate configurable (9600 por defecto)

## 🔧 Uso Básico

### Importar el plugin
```python
from Controller.plugins import printer_plugin, setup_printer, print_sale_receipt
```

### Conectar a impresora USB
```python
# Conexión automática (Epson TM-T88)
setup_printer('usb')

# Conexión personalizada
setup_printer('usb', vendor_id=0x04b8, product_id=0x0202)
```

### Conectar a impresora de red
```python
setup_printer('network', ip='192.168.1.100', port=9100)
```

### Conectar via serial
```python
setup_printer('serial', port='/dev/ttyUSB0', baudrate=9600)
```

### Imprimir recibo de venta
```python
items = [
    {'descripcion': 'Anillo Oro 18K', 'precio': 1500.00, 'cantidad': 1},
    {'descripcion': 'Collar Plata 925', 'precio': 850.50, 'cantidad': 2}
]

print_sale_receipt('SM-001', 'Juan Pérez', items)
```

### Imprimir página de prueba
```python
printer_plugin.print_test()
```

## ⚙️ Configuración

```python
# Actualizar configuración
nueva_config = {
    'width': 32,           # Ancho en caracteres
    'encoding': 'utf-8',   # Codificación de texto
    'cut_paper': True,     # Cortar papel automáticamente
    'open_drawer': False,  # Abrir cajón de dinero
    'print_logo': False    # Imprimir logo (futuro)
}
printer_plugin.update_config(nueva_config)
```

## 🧪 Pruebas

### Ejecutar prueba completa
```bash
cd /path/to/proyecto
python Controller/plugins/test_printer.py
```

### Detectar impresoras USB
```python
printers = printer_plugin.detect_usb_printers()
for printer in printers:
    print(f\"{printer['name']} - {printer['vendor_id']}:{printer['product_id']}\")
```

### Verificar estado
```python
status = printer_plugin.get_status()
print(f\"Conectada: {status['connected']}\")
print(f\"Tipo: {status['type']}\")
```

## 📄 Formatos de Datos

### Recibo de Venta
```python
receipt_data = {
    'folio': 'SM-001',
    'cliente': 'María García', 
    'fecha': '2026-03-10 14:30:00',
    'items': [
        {
            'descripcion': 'Producto 1',
            'precio': 100.50,
            'cantidad': 2
        }
    ],
    'codigo_barras': '123456789012'  # Opcional
}
printer_plugin.print_receipt(receipt_data)
```

### Reporte de Inventario
```python
inventory_data = [
    {
        'codigo': 'AN001',
        'descripcion': 'Anillo Pandora',
        'stock': 5,
        'precio': 1250.00
    }
]
printer_plugin.print_inventory_report(inventory_data)
```

## 🔍 Solución de Problemas

### Error de conexión USB
1. Verificar que la impresora esté encendida
2. Comprobar IDs de vendor/product con `lsusb`
3. Verificar permisos de dispositivo
4. Instalar drivers específicos si es necesario

### Error de red
1. Verificar conectividad: `ping ip_impresora`
2. Comprobar puerto (generalmente 9100)
3. Revisar configuración de firewall

### Error de dependencias
```bash
# Reinstalar dependencias
pip uninstall python-escpos
pip install python-escpos==3.0a7

# Para macOS con libusb
brew install libusb
```

### Caracteres especiales incorrectos
```python
# Cambiar codificación
printer_plugin.update_config({'encoding': 'latin-1'})
```

## 📊 Ejemplo de Integración con Sistema

```python
# En el módulo de ventas
from Controller.plugins import print_sale_receipt

def finalizar_venta(folio, cliente, items_venta):
    # ... lógica de la venta ...
    
    # Imprimir recibo
    if print_sale_receipt(folio, cliente, items_venta):
        print(\"Recibo impreso correctamente\")
    else:
        print(\"Error imprimiendo recibo\")
```

## 📝 Registro de Actividad

El plugin utiliza el módulo `logging` de Python. Para habilitar logs detallados:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Los mensajes incluyen prefijo `[PRINTER]` para fácil identificación.

## 🔄 Desarrollo Futuro

- Soporte para imágenes/logos
- Plantillas de recibo personalizables
- Múltiples impresoras simultáneas
- Interfaz web de configuración
- Soporte para códigos QR

## 📞 Soporte

Para problemas específicos:
1. Revisar logs del sistema
2. Ejecutar `test_printer.py` para diagnóstico
3. Verificar compatibilidad de hardware
4. Consultar documentación de `python-escpos`

---
**Sistema S&M v1.0** | Plugin de Impresora Térmica v1.0