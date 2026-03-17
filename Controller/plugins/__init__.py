"""
Paquete de plugins para el Sistema S&M
"""

from .printer_plugin import ThermalPrinterPlugin, printer_plugin, setup_printer

__all__ = ['ThermalPrinterPlugin', 'printer_plugin', 'setup_printer']