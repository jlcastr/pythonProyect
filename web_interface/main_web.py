"""
Sistema de Ventas S&M - Interfaz Web con PyWebView
Autor: Sistema de Gestión
Versión: 2.0 - Compatible con Python 3.13
Descripción: Interfaz web moderna para el sistema de ventas usando PyWebView
"""

import os
import sys
import threading
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Importar PyWebView
try:
    import webview
except ImportError:
    print("[ERROR] pywebview no está instalado. Instalar con: pip install pywebview")
    sys.exit(1)

# Importar módulos del sistema existente
DEMO_MODE = False
try:
    sys.path.append(str(Path(__file__).parent.parent))
    from View.Sales import Sales
    from View.Report_menu import crear_menu_reportes  
    from View.menu_settings_view import mostrar_configuraciones
    from Controller.styles import obtener_configuracion_adaptativa
    from config.db_setup import crear_conexion_y_tablas, obtener_conexion
    print("[INFO] Módulos del sistema cargados correctamente")
except ImportError as e:
    DEMO_MODE = True
    print(f"[INFO] Ejecutando en modo demostración")
    print(f"[DEBUG] Módulos no disponibles: {e}")
    
    # Funciones dummy para modo demostración
    def obtener_configuracion_adaptativa():
        return {'window_width': 1200, 'window_height': 800, 'screen_width': 1920, 'screen_height': 1080}
    
    def obtener_conexion():
        return None
    
    def crear_conexion_y_tablas():
        pass

class SalesSystemAPI:
    """API para comunicación entre JavaScript y Python"""
    
    def __init__(self):
        self.current_window = None
    
    def test_connection(self):
        """API: Prueba de conexión entre JavaScript y Python"""
        print("[TEST] ¡Conexión PyWebView funcionando correctamente!")
        return {"status": "success", "message": "Conexión establecida", "timestamp": "2025-10-09"}
        
    def open_sales(self):
        """Abrir módulo de ventas"""
        try:
            print("[INFO] Abriendo módulo de ventas web...")
            
            # Importar y crear instancia del módulo de ventas web
            try:
                sys.path.append(str(Path(__file__).parent.parent))
                from View.Sales_Web import SalesWebInterface
                self.sales_interface = SalesWebInterface()
                print("[INFO] Módulo de ventas inicializado correctamente")
                
            except ImportError as e:
                print(f"[WARN] Usando modo demostración para ventas: {e}")
                
            # Preparar información para JavaScript sin operaciones complejas
            sales_html = Path(__file__).parent / "Sales" / "sales.html"
            if sales_html.exists():
                sales_url = f"file://{sales_html.absolute().as_posix()}"
                print(f"[INFO] URL de ventas preparada: {sales_url}")
                
                # Retornar información simple para JavaScript
                return {
                    "status": "success",
                    "message": "Módulo de ventas iniciado",
                    "url": sales_url,
                    "redirect": True
                }
            else:
                print("[ERROR] Archivo sales.html no encontrado")
                return {
                    "status": "error", 
                    "message": "Archivo de ventas no encontrado"
                }
                
        except Exception as e:
            print(f"[ERROR] Error abriendo ventas: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    # Métodos API para el módulo de ventas
    def sales_agregar_producto(self, descripcion, precio):
        """API: Agregar producto a la venta"""
        try:
            print(f"\n[SALES] ===== INICIO sales_agregar_producto =====")
            print(f"[SALES] Descripción recibida: '{descripcion}' (tipo: {type(descripcion)})")
            print(f"[SALES] Precio recibido: '{precio}' (tipo: {type(precio)})")
            print(f"[SALES] Tiene sales_interface: {hasattr(self, 'sales_interface')}")
            
            if hasattr(self, 'sales_interface'):
                print(f"[SALES] sales_interface es: {type(self.sales_interface)}")
                print(f"[SALES] Llamando a sales_interface.agregar_producto...")
                resultado = self.sales_interface.agregar_producto(descripcion, precio)
                print(f"[SALES] Resultado del sales_interface: {resultado}")
                print(f"[SALES] ===== FIN sales_agregar_producto =====\n")
                return resultado
            else:
                print("[SALES] No hay sales_interface disponible - usando modo demo")
                return {"status": "info", "message": "Producto agregado (demo)"}
        except Exception as e:
            print(f"\n[SALES] ===== ERROR sales_agregar_producto =====")
            print(f"[SALES] Error en sales_agregar_producto: {e}")
            import traceback
            traceback.print_exc()
            print(f"[SALES] ===== FIN ERROR =====\n")
            return {"status": "error", "message": str(e)}
    
    def sales_eliminar_producto(self, indice):
        """API: Eliminar producto de la venta"""
        try:
            if hasattr(self, 'sales_interface'):
                resultado = self.sales_interface.eliminar_producto(int(indice))
                print(f"[SALES] Producto eliminado: {resultado}")
                return resultado
            return {"status": "info", "message": "Producto eliminado (demo)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sales_limpiar_venta(self):
        """API: Limpiar venta actual"""
        try:
            if hasattr(self, 'sales_interface'):
                resultado = self.sales_interface.limpiar_venta()
                print(f"[SALES] Venta limpiada: {resultado}")
                return resultado
            return {"status": "info", "message": "Venta limpiada (demo)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sales_finalizar_venta(self, cliente):
        """API: Finalizar venta actual"""
        try:
            print(f"[SALES] Intentando finalizar venta para cliente: {cliente}")
            print(f"[SALES] Tiene sales_interface: {hasattr(self, 'sales_interface')}")
            
            if hasattr(self, 'sales_interface'):
                print(f"[SALES] sales_interface tipo: {type(self.sales_interface)}")
                print(f"[SALES] Conexión BD en interface: {'Sí' if self.sales_interface.conn else 'No'}")
                
                resultado = self.sales_interface.finalizar_venta(cliente)
                print(f"[SALES] Resultado finalización: {resultado}")
                return resultado
            else:
                print("[SALES] No hay sales_interface disponible - usando modo demo")
                return {"status": "info", "message": "Venta finalizada (demo)"}
        except Exception as e:
            print(f"[SALES] Error en sales_finalizar_venta: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}
    
    def sales_imprimir_venta(self):
        """API: Imprimir venta"""
        try:
            if hasattr(self, 'sales_interface'):
                resultado = self.sales_interface.imprimir_venta()
                print(f"[SALES] Venta impresa: {resultado}")
                return resultado
            return {"status": "info", "message": "Venta impresa (demo)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sales_enviar_correo(self, email):
        """API: Enviar venta por correo"""
        try:
            if hasattr(self, 'sales_interface'):
                resultado = self.sales_interface.enviar_por_correo(email)
                print(f"[SALES] Venta enviada: {resultado}")
                return resultado
            return {"status": "info", "message": f"Venta enviada a {email} (demo)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Funciones de Reportes
    def reports_ventas(self):
        """API: Abrir reporte de ventas"""
        try:
            print("[REPORTS] Abriendo reporte de ventas...")
            
            if not DEMO_MODE:
                try:
                    from View.ReportSales import mostrar_reporte_ventas_en_frame
                    # En el contexto web, podríamos retornar los datos del reporte
                    return {
                        "status": "success", 
                        "message": "Reporte de ventas generado",
                        "redirect": "./Report/sales_report.html"  # Página futura
                    }
                except ImportError as e:
                    print(f"[REPORTS] Error importando ReportSales: {e}")
                    return {"status": "info", "message": "Reporte de ventas (modo demostración)"}
            else:
                return {"status": "info", "message": "Reporte de ventas (modo demostración)"}
                
        except Exception as e:
            print(f"[REPORTS] Error en reporte de ventas: {e}")
            return {"status": "error", "message": str(e)}
    
    def reports_historial(self):
        """API: Abrir historial de ventas"""
        try:
            print("[REPORTS] Abriendo historial de ventas...")
            
            if not DEMO_MODE:
                try:
                    from View.ReportHistorySales import mostrar_historial_ventas_en_frame
                    # En el contexto web, podríamos retornar los datos del historial
                    return {
                        "status": "success", 
                        "message": "Historial de ventas generado",
                        "redirect": "./Report/history_report.html"  # Página futura
                    }
                except ImportError as e:
                    print(f"[REPORTS] Error importando ReportHistorySales: {e}")
                    return {"status": "info", "message": "Historial de ventas (modo demostración)"}
            else:
                return {"status": "info", "message": "Historial de ventas (modo demostración)"}
                
        except Exception as e:
            print(f"[REPORTS] Error en historial de ventas: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_sales_data(self, fecha_inicio='', fecha_fin=''):
        """API: Obtener datos de ventas de la base de datos"""
        try:
            print(f"[API] Obteniendo datos de ventas - Desde: {fecha_inicio}, Hasta: {fecha_fin}")
            
            # Importar sqlite3 y conectar a la base de datos
            # Ignoramos DEMO_MODE para reportes porque la base de datos siempre debe estar disponible
            import sqlite3
            from datetime import datetime
            
            # Conectar a la base de datos
            db_path = Path(__file__).parent.parent / "config" / "sales_system.db"
            
            if not db_path.exists():
                print(f"[ERROR] Base de datos no encontrada en: {db_path}")
                return []
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Construir query SQL igual que en ReportSales.py
            query = """
                SELECT ventas_items.descripcion, ventas_items.precio, 
                       VentaMaster.fecha_venta, VentaMaster.folio 
                FROM ventas_items 
                INNER JOIN VentaMaster ON ventas_items.venta_master_id = VentaMaster.id
            """
            params = []
            
            # Aplicar filtros de fecha si se proporcionan
            if fecha_inicio and fecha_fin:
                query += " WHERE date(VentaMaster.fecha_venta) BETWEEN ? AND ?"
                params = [fecha_inicio, fecha_fin]
            elif fecha_inicio:
                query += " WHERE date(VentaMaster.fecha_venta) >= ?"
                params = [fecha_inicio]
            elif fecha_fin:
                query += " WHERE date(VentaMaster.fecha_venta) <= ?"
                params = [fecha_fin]
            
            query += " ORDER BY VentaMaster.fecha_venta DESC"
            
            # Ejecutar query
            print(f"[API] Ejecutando query: {query}")
            print(f"[API] Con parámetros: {params}")
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convertir a formato que espera JavaScript
            sales_data = []
            for row in rows:
                sales_data.append({
                    'descripcion': row[0],
                    'precio': str(row[1]),  # Convertir a string para JSON
                    'fecha_venta': row[2],
                    'folio': row[3]
                })
            
            conn.close()
            
            print(f"[API] Datos obtenidos exitosamente: {len(sales_data)} registros")
            if sales_data:
                print(f"[API] Primer registro: {sales_data[0]}")
                print(f"[API] Último registro: {sales_data[-1]}")
            
            return sales_data
            
        except Exception as e:
            print(f"[API] Error obteniendo datos de ventas: {e}")
            import traceback
            traceback.print_exc()
            return []

    def volver_menu_principal(self):
        """API: Volver al menú principal"""
        try:
            print("[NAV] Volviendo al menú principal...")
            return {
                "status": "success",
                "message": "Volviendo al menú principal",
                "redirect": "../index.html"
            }
        except Exception as e:
            print(f"[NAV] Error volviendo al menú: {e}")
            return {"status": "error", "message": str(e)}

    def volver_menu_reportes(self):
        """API: Volver al menú de reportes"""
        try:
            print("[NAV] Volviendo al menú de reportes...")
            return {
                "status": "success",
                "message": "Volviendo al menú de reportes",
                "redirect": "menu_report.html"
            }
        except Exception as e:
            print(f"[NAV] Error volviendo al menú de reportes: {e}")
            return {"status": "error", "message": str(e)}

    def open_reports(self):
        """Abrir módulo de reportes"""
        try:
            print("[INFO] Abriendo módulo de reportes...")
            
            # Esta función no es necesaria para la interfaz web
            # Los reportes se manejan directamente en HTML
            return {"status": "success", "message": "Módulo de reportes disponible en la interfaz web"}
                
        except Exception as e:
            print(f"[ERROR] Error abriendo reportes: {e}")
            return {"status": "error", "message": str(e)}
    
    def open_inventory(self):
        """Abrir módulo de inventario"""
        print("[INFO] Abriendo módulo de inventario...")
        return {"status": "info", "message": "Módulo de inventario en desarrollo"}
    
    def open_customers(self):
        """Abrir módulo de clientes"""
        print("[INFO] Abriendo módulo de clientes...")
        return {"status": "info", "message": "Módulo de clientes en desarrollo"}
    
    def open_settings(self):
        """Abrir configuraciones"""
        try:
            print("[INFO] Abriendo configuraciones...")
            
            # Esta función no es necesaria para la interfaz web
            # Las configuraciones se manejan directamente en HTML
            return {"status": "success", "message": "Configuraciones disponibles en la interfaz web"}
                
        except Exception as e:
            print(f"[ERROR] Error abriendo configuraciones: {e}")
            return {"status": "error", "message": str(e)}
    
    def open_prices(self):
        """Abrir gestión de precios"""
        print("[INFO] Abriendo gestión de precios...")
        return {"status": "info", "message": "Gestión de precios en desarrollo"}
    
    def exit_application(self):
        """Cerrar aplicación"""
        print("[INFO] Cerrando aplicación...")
        webview.windows[0].destroy()
        return {"status": "success", "message": "Aplicación cerrada"}
    
    def get_system_info(self):
        """Obtener información del sistema"""
        try:
            config = obtener_configuracion_adaptativa()
            return {
                "status": "success",
                "data": {
                    "resolution": f"{config.get('screen_width', 'N/A')}x{config.get('screen_height', 'N/A')}",
                    "config": config,
                    "python_version": sys.version,
                    "platform": sys.platform
                }
            }
        except Exception as e:
            return {
                "status": "success", 
                "data": {
                    "python_version": sys.version,
                    "platform": sys.platform,
                    "mode": "demostración"
                }
            }

class SalesSystemWebApp:
    """Aplicación principal con interfaz web usando PyWebView"""
    
    def __init__(self):
        self.api = SalesSystemAPI()
        self.base_path = Path(__file__).parent
        self.web_path = self.base_path / "web_interface"
        
    def get_html_path(self) -> str:
        """Obtener ruta del archivo HTML principal"""
        # Cargar index.html (menú principal) por defecto
        html_file = self.base_path / "index.html"
        if html_file.exists():
            print(f"[INFO] Cargando menú principal: {html_file}")
            return str(html_file.absolute())
        
        raise FileNotFoundError(f"Archivo HTML principal no encontrado: {html_file}")
    
    def get_window_config(self) -> Dict[str, Any]:
        """Obtener configuración de ventana"""
        try:
            config = obtener_configuracion_adaptativa()
            return {
                "width": config.get('window_width', 1200),
                "height": config.get('window_height', 800),
                "min_size": (800, 600)
            }
        except:
            return {
                "width": 1200,
                "height": 800,
                "min_size": (800, 600)
            }
    
    def run(self):
        """Ejecutar la aplicación"""
        try:
            print("=" * 60)
            print("SISTEMA DE VENTAS S&M - INTERFAZ WEB")
            print("Powered by PyWebView - Compatible con Python 3.13")
            print("=" * 60)
            
            # Verificar base de datos si está disponible
            try:
                conn = obtener_conexion()
                if not conn:
                    print("[INFO] Creando base de datos...")
                    crear_conexion_y_tablas()
                else:
                    conn.close()
            except:
                print("[INFO] Funcionando en modo demostración")
            
            # Obtener configuración de ventana
            window_config = self.get_window_config()
            html_path = self.get_html_path()
            
            print(f"[INFO] Cargando interfaz desde: {html_path}")
            print(f"[INFO] Tamaño de ventana: {window_config['width']}x{window_config['height']}")
            print(f"[INFO] Python: {sys.version}")
            print("[INFO] SIN servidor web - Acceso directo a archivos")
            
            # Crear ventana con PyWebView
            webview.create_window(
                title="Sistema de Ventas S&M - Interfaz Web",
                url=html_path,
                width=window_config['width'],
                height=window_config['height'],
                min_size=window_config['min_size'],
                resizable=True,
                shadow=True,
                js_api=self.api
            )
            
            # Iniciar la aplicación
            print("[INFO] Iniciando aplicación...")
            print("[INFO] Presione Ctrl+C para salir")
            
            webview.start(debug=False)
            
        except KeyboardInterrupt:
            print("\n[INFO] Interrupción por teclado recibida...")
        except Exception as e:
            print(f"[ERROR] Error en la aplicación: {e}")
        finally:
            print("[INFO] Aplicación cerrada")

def check_pywebview_compatibility():
    """Verificar compatibilidad con PyWebView"""
    try:
        # Verificar que webview esté disponible
        webview.create_window  # Test basic functionality
        print(f"[INFO] PyWebView está disponible")
        print(f"[INFO] Python versión: {sys.version}")
        return True
    except Exception as e:
        print(f"[ERROR] Error verificando PyWebView: {e}")
        return False

def main():
    """Función principal"""
    try:
        print("Verificando compatibilidad...")
        if not check_pywebview_compatibility():
            print("[ERROR] PyWebView no es compatible con este sistema")
            return 1
        
        # Crear y ejecutar aplicación
        app = SalesSystemWebApp()
        app.run()
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] Error fatal: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)