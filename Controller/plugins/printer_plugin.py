"""
Plugin para Impresoras Térmicas
Compatible con impresoras ESC/POS (Epson, Star, ZJ, etc.)
Autor: Sistema S&M
Version: 1.0
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from escpos.printer import Usb, Network, Serial, File
    from escpos.exceptions import *
    ESCPOS_AVAILABLE = True
    logger.info("[PRINTER] ESC/POS library disponible")
except ImportError:
    ESCPOS_AVAILABLE = False
    logger.warning("[PRINTER] ESC/POS library no disponible. Instale con: pip install python-escpos")

class ThermalPrinterPlugin:
    """
    Plugin para manejo de impresoras térmicas
    Soporta conexiones USB, Network, Serial y File
    """
    
    def __init__(self):
        self.printer = None
        self.printer_type = None
        self.is_connected = False
        self.config = {
            'width': 32,  # Ancho en caracteres (típico para recibos)
            'encoding': 'utf-8',
            'cut_paper': True,
            'open_drawer': False,
            'print_logo': False
        }
        
    def detect_usb_printers(self) -> List[Dict]:
        """
        Detectar impresoras USB disponibles
        """
        if not ESCPOS_AVAILABLE:
            return []
            
        try:
            import usb.core
            # IDs comunes de impresoras térmicas
            thermal_printers = [
                {'vendor': 0x04b8, 'product': 0x0202, 'name': 'Epson TM-T88'},
                {'vendor': 0x04b8, 'product': 0x0e15, 'name': 'Epson TM-T20'},
                {'vendor': 0x0fe6, 'product': 0x811e, 'name': 'ZJ-5890K'},
                {'vendor': 0x067b, 'product': 0x2305, 'name': 'Prolific PL2305'},
                {'vendor': 0x1a86, 'product': 0x7584, 'name': 'CH340 Serial'}
            ]
            
            detected = []
            for printer in thermal_printers:
                device = usb.core.find(idVendor=printer['vendor'], idProduct=printer['product'])
                if device:
                    detected.append({
                        'name': printer['name'],
                        'vendor_id': hex(printer['vendor']),
                        'product_id': hex(printer['product']),
                        'type': 'usb'
                    })
                    
            return detected
            
        except Exception as e:
            logger.error(f"[PRINTER] Error detectando impresoras USB: {e}")
            return []
    
    def connect_usb(self, vendor_id: int = 0x04b8, product_id: int = 0x0202) -> bool:
        """
        Conectar a impresora USB
        """
        if not ESCPOS_AVAILABLE:
            logger.error("[PRINTER] Librería ESC/POS no disponible")
            return False
            
        try:
            self.printer = Usb(vendor_id, product_id)
            self.printer_type = 'usb'
            self.is_connected = True
            logger.info(f"[PRINTER] Conectado a impresora USB {hex(vendor_id)}:{hex(product_id)}")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error conectando USB: {e}")
            self.is_connected = False
            return False
    
    def connect_network(self, ip: str, port: int = 9100) -> bool:
        """
        Conectar a impresora de red
        """
        if not ESCPOS_AVAILABLE:
            logger.error("[PRINTER] Librería ESC/POS no disponible")
            return False
            
        try:
            self.printer = Network(ip, port)
            self.printer_type = 'network'
            self.is_connected = True
            logger.info(f"[PRINTER] Conectado a impresora de red {ip}:{port}")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error conectando red: {e}")
            self.is_connected = False
            return False
    
    def connect_serial(self, port: str = '/dev/ttyUSB0', baudrate: int = 9600) -> bool:
        """
        Conectar a impresora serial
        """
        if not ESCPOS_AVAILABLE:
            logger.error("[PRINTER] Librería ESC/POS no disponible")
            return False
            
        try:
            self.printer = Serial(port, baudrate)
            self.printer_type = 'serial'
            self.is_connected = True
            logger.info(f"[PRINTER] Conectado a impresora serial {port}")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error conectando serial: {e}")
            self.is_connected = False
            return False
    
    def connect_file(self, filepath: str = 'printer_output.bin') -> bool:
        """
        Conectar a archivo (para pruebas)
        """
        if not ESCPOS_AVAILABLE:
            logger.error("[PRINTER] Librería ESC/POS no disponible")
            return False
            
        try:
            self.printer = File(filepath)
            self.printer_type = 'file'
            self.is_connected = True
            logger.info(f"[PRINTER] Conectado a archivo {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error conectando archivo: {e}")
            self.is_connected = False
            return False
    
    def print_receipt(self, data: Dict) -> bool:
        """
        Imprimir recibo de venta
        """
        if not self.is_connected or not self.printer:
            logger.error("[PRINTER] No hay impresora conectada")
            return False
            
        try:
            # Header del recibo
            self.printer.set(align='center', text_type='b', width=2, height=2)
            self.printer.text("SISTEMA S&M\n")
            self.printer.text("RECIBO DE VENTA\n")
            
            # Línea separadora
            self.printer.set(align='left', text_type='normal', width=1, height=1)
            self.printer.text("=" * self.config['width'] + "\n")
            
            # Información de la venta
            self.printer.text(f"Folio: {data.get('folio', 'N/A')}\n")
            self.printer.text(f"Fecha: {data.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M'))}\n")
            self.printer.text(f"Cliente: {data.get('cliente', 'Público General')}\n")
            self.printer.text("-" * self.config['width'] + "\n")
            
            # Items de la venta
            total = 0
            items = data.get('items', [])
            
            for item in items:
                desc = str(item.get('descripcion', 'Producto'))[:20]
                precio = float(item.get('precio', 0))
                cantidad = int(item.get('cantidad', 1))
                subtotal = precio * cantidad
                total += subtotal
                
                # Línea de producto
                self.printer.text(f"{desc}\n")
                self.printer.text(f"{cantidad} x ${precio:.2f}")
                self.printer.text(f"${subtotal:.2f}".rjust(self.config['width'] - len(f"{cantidad} x ${precio:.2f}")) + "\n")
            
            # Total
            self.printer.text("=" * self.config['width'] + "\n")
            self.printer.set(text_type='b', width=2, height=2)
            total_text = f"TOTAL: ${total:.2f}"
            self.printer.text(total_text.center(self.config['width']) + "\n")
            
            # Footer
            self.printer.set(text_type='normal', width=1, height=1, align='center')
            self.printer.text("\nGracias por su compra\n")
            self.printer.text(f"www.sistema-sm.com\n")
            
            # Código de barras si está disponible
            if 'codigo_barras' in data:
                self.printer.barcode(str(data['codigo_barras']), 'CODE128', width=2, height=50)
            
            # Cortar papel si está habilitado
            if self.config['cut_paper']:
                self.printer.cut()
                
            # Abrir cajón si está habilitado
            if self.config['open_drawer']:
                self.printer.cashdraw(2)
                
            logger.info(f"[PRINTER] Recibo impreso exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error imprimiendo recibo: {e}")
            return False
    
    def print_inventory_report(self, data: List[Dict]) -> bool:
        """
        Imprimir reporte de inventario
        """
        if not self.is_connected or not self.printer:
            logger.error("[PRINTER] No hay impresora conectada")
            return False
            
        try:
            # Header del reporte
            self.printer.set(align='center', text_type='b', width=2, height=2)
            self.printer.text("SISTEMA S&M\n")
            self.printer.text("REPORTE INVENTARIO\n")
            
            # Información del reporte
            self.printer.set(align='left', text_type='normal', width=1, height=1)
            self.printer.text("=" * self.config['width'] + "\n")
            self.printer.text(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            self.printer.text(f"Total productos: {len(data)}\n")
            self.printer.text("-" * self.config['width'] + "\n")
            
            # Productos
            for i, producto in enumerate(data, 1):
                codigo = str(producto.get('codigo', 'N/A'))[:8]
                desc = str(producto.get('descripcion', 'Sin descripción'))[:18]
                stock = producto.get('stock', 0)
                precio = producto.get('precio', 0.0)
                
                self.printer.text(f"{i:2d}. {codigo} - {desc}\n")
                self.printer.text(f"    Stock: {stock:3d} | ${precio:.2f}\n")
                
                if i % 20 == 0:  # Pausa cada 20 productos
                    self.printer.text("-" * self.config['width'] + "\n")
            
            # Footer
            self.printer.text("=" * self.config['width'] + "\n")
            self.printer.set(align='center')
            self.printer.text("Fin del reporte\n")
            
            if self.config['cut_paper']:
                self.printer.cut()
                
            logger.info(f"[PRINTER] Reporte de inventario impreso exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error imprimiendo reporte: {e}")
            return False
    
    def print_test(self) -> bool:
        """
        Imprimir página de prueba
        """
        if not self.is_connected or not self.printer:
            logger.error("[PRINTER] No hay impresora conectada")
            return False
            
        try:
            self.printer.set(align='center', text_type='b', width=2, height=2)
            self.printer.text("PRUEBA DE IMPRESION\n")
            
            self.printer.set(text_type='normal', width=1, height=1)
            self.printer.text("=" * self.config['width'] + "\n")
            
            # Información del sistema
            self.printer.text(f"Sistema: S&M v1.0\n")
            self.printer.text(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.printer.text(f"Tipo: {self.printer_type}\n")
            self.printer.text(f"Ancho: {self.config['width']} chars\n")
            
            # Prueba de caracteres
            self.printer.text("-" * self.config['width'] + "\n")
            self.printer.text("Prueba de caracteres:\n")
            self.printer.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ\n")
            self.printer.text("abcdefghijklmnopqrstuvwxyz\n")
            self.printer.text("0123456789 !@#$%^&*()\n")
            self.printer.text("áéíóú ñÑ üÜ ¿¡\n")
            
            # Prueba de códigos de barras
            self.printer.text("-" * self.config['width'] + "\n")
            try:
                self.printer.barcode('123456789012', 'CODE128', width=2, height=50)
                self.printer.text("Código de barras OK\n")
            except:
                self.printer.text("Código de barras no soportado\n")
            
            self.printer.text("=" * self.config['width'] + "\n")
            self.printer.set(align='center')
            self.printer.text("PRUEBA COMPLETADA\n")
            
            if self.config['cut_paper']:
                self.printer.cut()
                
            logger.info("[PRINTER] Página de prueba impresa exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error imprimiendo prueba: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Desconectar impresora
        """
        try:
            if self.printer and hasattr(self.printer, 'close'):
                self.printer.close()
                
            self.printer = None
            self.printer_type = None
            self.is_connected = False
            logger.info("[PRINTER] Impresora desconectada")
            return True
            
        except Exception as e:
            logger.error(f"[PRINTER] Error desconectando: {e}")
            return False
    
    def get_status(self) -> Dict:
        """
        Obtener estado de la impresora
        """
        return {
            'connected': self.is_connected,
            'type': self.printer_type,
            'config': self.config.copy(),
            'escpos_available': ESCPOS_AVAILABLE
        }
    
    def update_config(self, new_config: Dict) -> None:
        """
        Actualizar configuración
        """
        self.config.update(new_config)
        logger.info(f"[PRINTER] Configuración actualizada: {new_config}")

# Instancia global del plugin
printer_plugin = ThermalPrinterPlugin()

# Funciones de utilidad
def setup_printer(connection_type: str = 'usb', **kwargs) -> bool:
    """
    Configurar y conectar impresora
    """
    if connection_type == 'usb':
        vendor_id = kwargs.get('vendor_id', 0x04b8)
        product_id = kwargs.get('product_id', 0x0202)
        return printer_plugin.connect_usb(vendor_id, product_id)
        
    elif connection_type == 'network':
        ip = kwargs.get('ip', '192.168.1.100')
        port = kwargs.get('port', 9100)
        return printer_plugin.connect_network(ip, port)
        
    elif connection_type == 'serial':
        port = kwargs.get('port', '/dev/ttyUSB0')
        baudrate = kwargs.get('baudrate', 9600)
        return printer_plugin.connect_serial(port, baudrate)
        
    elif connection_type == 'file':
        filepath = kwargs.get('filepath', 'printer_output.bin')
        return printer_plugin.connect_file(filepath)
        
    else:
        logger.error(f"[PRINTER] Tipo de conexión no soportado: {connection_type}")
        return False

def print_sale_receipt(folio: str, cliente: str, items: List[Dict], fecha: str = None) -> bool:
    """
    Imprimir recibo de venta
    """
    if not fecha:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    receipt_data = {
        'folio': folio,
        'cliente': cliente,
        'fecha': fecha,
        'items': items
    }
    
    return printer_plugin.print_receipt(receipt_data)

def print_test_page() -> bool:
    """
    Imprimir página de prueba
    """
    return printer_plugin.print_test()

def get_printer_status() -> Dict:
    """
    Obtener estado de la impresora
    """
    return printer_plugin.get_status()

if __name__ == "__main__":
    # Prueba del plugin
    print("Probando plugin de impresora térmica...")
    
    # Detectar impresoras USB
    printers = printer_plugin.detect_usb_printers()
    print(f"Impresoras detectadas: {len(printers)}")
    for printer in printers:
        print(f"  - {printer['name']} ({printer['vendor_id']}:{printer['product_id']})")
    
    # Conectar a archivo para prueba
    if printer_plugin.connect_file('test_output.bin'):
        print("Conectado a archivo de prueba")
        
        # Imprimir página de prueba
        if printer_plugin.print_test():
            print("Página de prueba impresa")
        
        # Imprimir recibo de prueba
        test_items = [
            {'descripcion': 'Producto 1', 'precio': 100.50, 'cantidad': 2},
            {'descripcion': 'Producto 2', 'precio': 75.25, 'cantidad': 1}
        ]
        
        if print_sale_receipt('TEST-001', 'Cliente Test', test_items):
            print("Recibo de prueba impreso")
        
        printer_plugin.disconnect()
        print("Prueba completada")
    else:
        print("Error conectando a archivo de prueba")