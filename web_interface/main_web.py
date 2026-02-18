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

    def get_sales_master(self, fecha_inicio='', fecha_fin=''):
        """API: Obtener datos de ventas maestras (VentaMaster)"""
        try:
            print(f"[API] Obteniendo ventas maestras - Desde: {fecha_inicio}, Hasta: {fecha_fin}")
            
            import sqlite3
            from datetime import datetime
            
            # Conectar a la base de datos
            db_path = Path(__file__).parent.parent / "config" / "sales_system.db"
            
            if not db_path.exists():
                print(f"[ERROR] Base de datos no encontrada en: {db_path}")
                return {"status": "error", "message": "Base de datos no encontrada"}
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Query para obtener ventas maestras con total calculado
            query = """
                SELECT vm.folio, vm.cliente, vm.fecha_venta, vm.id,
                       COALESCE(SUM(vi.precio), 0) as total
                FROM VentaMaster vm
                LEFT JOIN ventas_items vi ON vm.id = vi.venta_master_id
            """
            params = []
            
            # Aplicar filtros de fecha si se proporcionan
            if fecha_inicio and fecha_fin:
                query += " WHERE date(vm.fecha_venta) BETWEEN ? AND ?"
                params = [fecha_inicio, fecha_fin]
            elif fecha_inicio:
                query += " WHERE date(vm.fecha_venta) >= ?"
                params = [fecha_inicio]
            elif fecha_fin:
                query += " WHERE date(vm.fecha_venta) <= ?"
                params = [fecha_fin]
            
            query += " GROUP BY vm.id, vm.folio, vm.cliente, vm.fecha_venta ORDER BY vm.fecha_venta DESC"
            
            # Ejecutar query
            print(f"[API] Ejecutando query ventas maestras: {query}")
            print(f"[API] Con parámetros: {params}")
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convertir a formato que espera JavaScript
            ventas_data = []
            for row in rows:
                ventas_data.append({
                    'folio': row[0],
                    'cliente': row[1],
                    'fecha_venta': row[2],
                    'id': row[3],
                    'total': str(row[4])  # Convertir a string para JSON
                })
            
            conn.close()
            
            print(f"[API] Ventas maestras obtenidas: {len(ventas_data)} registros")
            
            return {"status": "success", "data": ventas_data}
            
        except Exception as e:
            print(f"[API] Error obteniendo ventas maestras: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}

    def get_sales_items(self, venta_master_id):
        """API: Obtener items de una venta específica"""
        try:
            print(f"[API] Obteniendo items para venta ID: {venta_master_id}")
            
            import sqlite3
            
            # Conectar a la base de datos
            db_path = Path(__file__).parent.parent / "config" / "sales_system.db"
            
            if not db_path.exists():
                print(f"[ERROR] Base de datos no encontrada en: {db_path}")
                return {"status": "error", "message": "Base de datos no encontrada"}
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Query para obtener items de la venta
            query = """
                SELECT descripcion, precio 
                FROM ventas_items 
                WHERE venta_master_id = ? 
                ORDER BY id
            """
            
            # Ejecutar query
            print(f"[API] Ejecutando query items: {query}")
            print(f"[API] Con parámetro: {venta_master_id}")
            cursor.execute(query, (venta_master_id,))
            rows = cursor.fetchall()
            
            # Convertir a formato que espera JavaScript
            items_data = []
            for row in rows:
                items_data.append({
                    'descripcion': row[0],
                    'precio': str(row[1])  # Convertir a string para JSON
                })
            
            conn.close()
            
            print(f"[API] Items obtenidos: {len(items_data)} registros")
            
            return {"status": "success", "data": items_data}
            
        except Exception as e:
            print(f"[API] Error obteniendo items: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}

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

    # Funciones de configuración del sistema
    def get_configuraciones(self):
        """Obtener las configuraciones del sistema"""
        try:
            if DEMO_MODE:
                return {
                    "status": "success",
                    "data": {
                        "id": 1,
                        "IsLocal": True,
                        "IsWeb": False,
                        "IsPremiun": False,
                        "IsGenerico": True,
                        "IsJoyeria": False
                    }
                }
            
            conn = obtener_conexion()
            if not conn:
                return {"status": "error", "message": "Error de conexión a la base de datos"}
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM configuraciones ORDER BY id LIMIT 1")
            result = cursor.fetchone()
            
            if result:
                data = {
                    "id": result[0],
                    "IsLocal": bool(result[1]),
                    "IsWeb": bool(result[2]),
                    "IsPremiun": bool(result[3]),
                    "IsGenerico": bool(result[4]),
                    "IsJoyeria": bool(result[5])
                }
                conn.close()
                return {"status": "success", "data": data}
            else:
                conn.close()
                return {"status": "error", "message": "No se encontró configuración"}
                
        except Exception as e:
            print(f"[ERROR] get_configuraciones: {e}")
            return {"status": "error", "message": f"Error al obtener configuraciones: {str(e)}"}

    def update_configuraciones(self, configuraciones):
        """Actualizar las configuraciones del sistema"""
        try:
            if DEMO_MODE:
                print(f"[DEMO] Actualizando configuraciones: {configuraciones}")
                return {"status": "success", "message": "Configuraciones actualizadas (modo demo)"}
            
            conn = obtener_conexion()
            if not conn:
                return {"status": "error", "message": "Error de conexión a la base de datos"}
            
            cursor = conn.cursor()
            
            # Verificar si existe al menos un registro
            cursor.execute("SELECT COUNT(*) FROM configuraciones")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insertar nuevo registro
                cursor.execute("""
                    INSERT INTO configuraciones (IsLocal, IsWeb, IsPremiun, IsGenerico, IsJoyeria) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    int(configuraciones.get('IsLocal', False)),
                    int(configuraciones.get('IsWeb', False)),
                    int(configuraciones.get('IsPremiun', False)),
                    int(configuraciones.get('IsGenerico', True)),
                    int(configuraciones.get('IsJoyeria', False))
                ))
                message = "Configuraciones creadas exitosamente"
            else:
                # Actualizar primer registro
                cursor.execute("""
                    UPDATE configuraciones 
                    SET IsLocal = ?, IsWeb = ?, IsPremiun = ?, IsGenerico = ?, IsJoyeria = ?
                    WHERE id = (SELECT MIN(id) FROM configuraciones)
                """, (
                    int(configuraciones.get('IsLocal', False)),
                    int(configuraciones.get('IsWeb', False)),
                    int(configuraciones.get('IsPremiun', False)),
                    int(configuraciones.get('IsGenerico', True)),
                    int(configuraciones.get('IsJoyeria', False))
                ))
                message = "Configuraciones actualizadas exitosamente"
            
            conn.commit()
            conn.close()
            
            print(f"[INFO] {message}")
            return {"status": "success", "message": message}
            
        except Exception as e:
            print(f"[ERROR] update_configuraciones: {e}")
            return {"status": "error", "message": f"Error al actualizar configuraciones: {str(e)}"}
    
    # Funciones de configuración de Email
    def obtener_config_email(self):
        """API: Obtener configuración de email actual"""
        try:
            print("[EMAIL] Obteniendo configuración de email...")
            
            if not DEMO_MODE:
                try:
                    # Importar funciones de email
                    from Controller.SQL.db_operations import consultar_email_config, obtener_email_config
                    
                    print("[EMAIL] Consultando tabla Emails...")
                    
                    # Consultar datos de la tabla Emails
                    email = consultar_email_config()
                    email_completo, password = obtener_email_config()
                    
                    print(f"[EMAIL] Email de BD (consultar_email_config): '{email}'")
                    print(f"[EMAIL] Email completo de BD (obtener_email_config): '{email_completo}'")
                    print(f"[EMAIL] Password existe: {bool(password)}")
                    print(f"[EMAIL] Email es None: {email is None}")
                    print(f"[EMAIL] Password es None: {password is None}")
                    
                    # Usar el email de la función más específica si está disponible
                    email_final = email_completo if email_completo else email
                    
                    # Manejar casos donde no hay configuración
                    if email_final is None or email_final == "":
                        email_display = "No configurado"
                        email_real = ""
                    else:
                        email_display = email_final
                        email_real = email_final
                    
                    if password is None or password == "":
                        password_display = "No configurada"
                        password_real = ""
                    else:
                        password_display = "••••••••"
                        password_real = password
                    
                    result = {
                        "status": "success",
                        "email": email_display,
                        "password": password_display,
                        "email_real": email_real,
                        "password_real": password_real,
                        "has_config": bool(email_real and password_real)
                    }
                    
                    print(f"[EMAIL] Resultado final: {result}")
                    return result
                    
                except ImportError as ie:
                    print(f"[EMAIL] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos de base de datos no disponibles: {str(ie)}"
                    }
                except Exception as db_error:
                    print(f"[EMAIL] Error accediendo a la base de datos: {db_error}")
                    import traceback
                    traceback.print_exc()
                    return {
                        "status": "error",
                        "message": f"Error de base de datos: {str(db_error)}"
                    }
            else:
                print("[EMAIL] Modo demostración activado")
                return {
                    "status": "success",
                    "email": "No configurado (modo demo)",
                    "password": "No configurada (modo demo)",
                    "email_real": "",
                    "password_real": "",
                    "has_config": False
                }
                
        except Exception as e:
            print(f"[EMAIL] Error obteniendo configuración: {e}")
            return {
                "status": "error",
                "message": f"Error al obtener configuración: {str(e)}"
            }
    
    def guardar_config_email(self, email, password):
        """API: Guardar configuración de email"""
        try:
            print(f"[EMAIL] Guardando configuración para: {email}")
            
            # Validaciones
            if not email or not password:
                return {
                    "status": "error",
                    "message": "Email y contraseña son obligatorios"
                }
            
            if "@" not in email or "." not in email:
                return {
                    "status": "error",
                    "message": "Formato de email inválido"
                }
            
            if len(password) < 6:
                return {
                    "status": "error",
                    "message": "La contraseña debe tener al menos 6 caracteres"
                }
            
            if not DEMO_MODE:
                # Importar y usar funciones de email
                from Controller.SQL.db_operations import guardar_email_config
                
                # Guardar en la base de datos
                guardar_email_config(email, password)
                
                print(f"[EMAIL] Configuración guardada exitosamente para: {email}")
                return {
                    "status": "success",
                    "message": "Configuración guardada correctamente"
                }
            else:
                print(f"[EMAIL] Modo demo - configuración simulada para: {email}")
                return {
                    "status": "success",
                    "message": "Configuración guardada (modo demostración)"
                }
                
        except Exception as e:
            print(f"[EMAIL] Error guardando configuración: {e}")
            return {
                "status": "error",
                "message": f"Error al guardar configuración: {str(e)}"
            }
    
    def probar_email_config(self, email, password):
        """API: Probar configuración de email enviando correo de prueba"""
        try:
            print(f"[EMAIL] Probando configuración para: {email}")
            
            if not email or not password:
                return {
                    "status": "error",
                    "message": "Email y contraseña son obligatorios para la prueba"
                }
            
            if not DEMO_MODE:
                # Importar módulo de email
                try:
                    from Controller.email import enviar_correo_prueba
                    
                    # Intentar enviar correo de prueba
                    resultado = enviar_correo_prueba(email, password, email)
                    
                    if resultado:
                        print(f"[EMAIL] Correo de prueba enviado exitosamente")
                        return {
                            "status": "success",
                            "message": "¡Correo de prueba enviado exitosamente!"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Error al enviar correo de prueba. Verifique la configuración."
                        }
                        
                except ImportError:
                    print("[EMAIL] Módulo de email no disponible")
                    return {
                        "status": "error",
                        "message": "Módulo de email no está configurado"
                    }
            else:
                # Simular envío en modo demo
                print(f"[EMAIL] Modo demo - simulando envío de prueba")
                return {
                    "status": "success",
                    "message": "Correo de prueba enviado exitosamente (modo demostración)"
                }
                
        except Exception as e:
            print(f"[EMAIL] Error probando configuración: {e}")
            return {
                "status": "error",
                "message": f"Error al probar configuración: {str(e)}"
            }
    
    def navegar_a(self, pagina):
        """API: Navegar a una página específica"""
        try:
            print(f"[NAV] Solicitud de navegación a: {pagina}")
            
            # Construir ruta completa
            if pagina.startswith('Settings/'):
                html_path = Path(__file__).parent / pagina
            else:
                html_path = Path(__file__).parent / "Settings" / pagina
            
            if html_path.exists():
                url = f"file://{html_path.absolute().as_posix()}"
                print(f"[NAV] Navegando a URL: {url}")
                
                # Usar threading para evitar problemas de callback
                def navegar():
                    try:
                        if hasattr(webview, 'windows') and webview.windows:
                            webview.windows[0].load_url(url)
                    except Exception as nav_error:
                        print(f"[NAV] Error en navegación: {nav_error}")
                
                # Ejecutar navegación en hilo separado
                threading.Thread(target=navegar, daemon=True).start()
                
                # Retornar inmediatamente
                return {
                    "status": "success",
                    "message": f"Navegando a {pagina}",
                    "url": url
                }
            else:
                print(f"[NAV] Archivo no encontrado: {html_path}")
                return {
                    "status": "error",
                    "message": f"Página no encontrada: {pagina}"
                }
                
        except Exception as e:
            print(f"[NAV] Error navegando: {e}")
            return {
                "status": "error",
                "message": f"Error de navegación: {str(e)}"
            }
    
    # Funciones de configuración de Logo y Títulos
    def obtener_titulos_config(self):
        """API: Obtener configuración de títulos actual"""
        try:
            print("[LOGO] Obteniendo configuración de títulos...")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import consultar_titulo_config
                    
                    titulos = consultar_titulo_config()
                    
                    return {
                        "status": "success",
                        "data": {
                            "sistema": titulos.get('sistema', ''),
                            "reporte": titulos.get('reporte', ''),
                            "ventana": titulos.get('ventana', '')
                        }
                    }
                    
                except ImportError as ie:
                    print(f"[LOGO] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos de base de datos no disponibles: {str(ie)}"
                    }
                except Exception as db_error:
                    print(f"[LOGO] Error accediendo a la base de datos: {db_error}")
                    return {
                        "status": "error",
                        "message": f"Error de base de datos: {str(db_error)}"
                    }
            else:
                print("[LOGO] Modo demostración - títulos por defecto")
                return {
                    "status": "success",
                    "data": {
                        "sistema": "Sistema de Manejo de Ventas",
                        "reporte": "Reporte de Ventas", 
                        "ventana": "Sistema de Gestión"
                    }
                }
                
        except Exception as e:
            print(f"[LOGO] Error general obteniendo títulos: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    def guardar_titulos_config(self, sistema, reporte, ventana):
        """API: Guardar configuración de títulos"""
        try:
            print(f"[LOGO] Guardando títulos: sistema='{sistema}', reporte='{reporte}', ventana='{ventana}'")
            
            if not DEMO_MODE:
                from Controller.SQL.db_operations import guardar_titulo_config
                
                # Guardar en la base de datos
                resultado = guardar_titulo_config(sistema, reporte, ventana)
                
                if resultado:
                    print("[LOGO] Títulos guardados exitosamente")
                    return {
                        "status": "success",
                        "message": "Títulos guardados correctamente"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "No se guardaron títulos porque todos los campos estaban vacíos"
                    }
            else:
                # Modo demostración
                print("[LOGO] Modo demo - títulos simulados")
                return {
                    "status": "success",
                    "message": "Títulos guardados correctamente (modo demostración)"
                }
                
        except Exception as e:
            print(f"[LOGO] Error guardando títulos: {e}")
            return {
                "status": "error",
                "message": f"Error al guardar títulos: {str(e)}"
            }
    
    def guardar_tipo_mercancia(self, tipo_mercancia, descripcion, categoria_general):
        """API: Guardar tipo de mercancía en la base de datos"""
        try:
            print(f"[INVENTORY] Guardando tipo de mercancía: '{tipo_mercancia}' - Categoría: '{categoria_general}'")
            
            # Validaciones
            if not tipo_mercancia or not tipo_mercancia.strip():
                return {
                    "status": "error",
                    "message": "El tipo de mercancía es obligatorio"
                }
            
            if not categoria_general or not categoria_general.strip():
                return {
                    "status": "error",
                    "message": "La categoría general es obligatoria"
                }
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import agregar_tipo_mercancia
                    
                    # Guardar en la base de datos
                    resultado = agregar_tipo_mercancia(
                        tipo_mercancia.strip(),
                        descripcion.strip() if descripcion else "",
                        categoria_general.strip()
                    )
                    
                    if resultado["status"] == "success":
                        print(f"[INVENTORY] Tipo de mercancía guardado exitosamente con ID: {resultado['id']}")
                        return {
                            "status": "success",
                            "message": "Tipo de mercancía registrado correctamente",
                            "id": resultado["id"]
                        }
                    else:
                        print(f"[INVENTORY] Error al guardar: {resultado['message']}")
                        return {
                            "status": "error",
                            "message": resultado["message"]
                        }
                        
                except ImportError as e:
                    print(f"[INVENTORY] Error importando módulo: {e}")
                    return {
                        "status": "error",
                        "message": "Módulo de base de datos no disponible"
                    }
            else:
                # Modo demostración
                print(f"[INVENTORY] Modo demo - tipo de mercancía simulado: {tipo_mercancia}")
                return {
                    "status": "success",
                    "message": "Tipo de mercancía registrado correctamente (modo demostración)",
                    "id": 999
                }
                
        except Exception as e:
            print(f"[INVENTORY] Error guardando tipo de mercancía: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"Error al registrar tipo de mercancía: {str(e)}"
            }
    
    def obtener_tipos_mercancia(self, categoria=None):
        """API: Obtener lista de tipos de mercancía"""
        try:
            print(f"[INVENTORY] Obteniendo tipos de mercancía - Categoría: {categoria}")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import obtener_tipos_mercancia as get_tipos
                    
                    # Obtener de la base de datos
                    tipos = get_tipos(categoria=categoria, activos_solo=True)
                    
                    print(f"[INVENTORY] Se encontraron {len(tipos)} tipos de mercancía")
                    return {
                        "status": "success",
                        "data": tipos,
                        "count": len(tipos)
                    }
                        
                except ImportError as e:
                    print(f"[INVENTORY] Error importando módulo: {e}")
                    return {
                        "status": "error",
                        "message": "Módulo de base de datos no disponible"
                    }
            else:
                # Modo demostración
                tipos_demo = [
                    {
                        "id": 1,
                        "tipo_mercancia": "Cadena de oro 18k",
                        "descripcion": "Cadena elegante para uso diario",
                        "categoria_general": "Cadenas"
                    },
                    {
                        "id": 2,
                        "tipo_mercancia": "Anillo de compromiso",
                        "descripcion": "Anillo con diamante solitario",
                        "categoria_general": "Anillos"
                    }
                ]
                
                if categoria:
                    tipos_demo = [t for t in tipos_demo if t["categoria_general"] == categoria]
                
                return {
                    "status": "success",
                    "data": tipos_demo,
                    "count": len(tipos_demo)
                }
                
        except Exception as e:
            print(f"[INVENTORY] Error obteniendo tipos de mercancía: {e}")
            return {
                "status": "error",
                "message": f"Error al obtener tipos de mercancía: {str(e)}"
            }
    
    def obtener_logo_info(self, seccion):
        """API: Obtener información de logo de una sección"""
        try:
            print(f"[LOGO] Obteniendo información de logo para: {seccion}")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import consultar_logo_config
                    import os
                    
                    # Archivos por defecto por sección
                    archivos_defecto = {
                        'ventanas': 'Img/SM2.ico',
                        'reportes': 'Img/logo_reportes.png',
                        'facturas': 'Img/logo_facturas.png'
                    }
                    
                    archivo_path = archivos_defecto.get(seccion, '')
                    config_bd = consultar_logo_config(seccion)
                    
                    if config_bd and os.path.exists(archivo_path):
                        fecha = config_bd['fecha_aplicado'][:10]
                        info_text = f"{config_bd['archivo_original']} - Aplicado {fecha}"
                    elif os.path.exists(archivo_path):
                        info_text = f"{os.path.basename(archivo_path)} - Logo actual"
                    else:
                        info_text = 'Sin logo configurado'
                    
                    return {
                        "status": "success",
                        "data": {
                            "info_text": info_text,
                            "preview_url": archivo_path if os.path.exists(archivo_path) else None
                        }
                    }
                    
                except ImportError as ie:
                    print(f"[LOGO] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos no disponibles: {str(ie)}"
                    }
                except Exception as db_error:
                    print(f"[LOGO] Error accediendo a datos de logo: {db_error}")
                    return {
                        "status": "error",
                        "message": f"Error de datos: {str(db_error)}"
                    }
            else:
                # Modo demo
                return {
                    "status": "success",
                    "data": {
                        "info_text": f"Logo {seccion} - Modo demostración",
                        "preview_url": None
                    }
                }
                
        except Exception as e:
            print(f"[LOGO] Error general obteniendo info de logo: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    def aplicar_logo(self, seccion, nombre_archivo, archivo_base64, tipo_archivo):
        """API: Aplicar logo a una sección específica"""
        try:
            print(f"[LOGO] Aplicando logo a {seccion}: {nombre_archivo}")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import guardar_logo_config
                    import base64
                    import os
                    from PIL import Image
                    from io import BytesIO
                    
                    # Decodificar imagen de base64
                    image_data = base64.b64decode(archivo_base64)
                    img = Image.open(BytesIO(image_data))
                    
                    # Configuración por sección
                    config_secciones = {
                        'ventanas': {'destino': 'Img/SM2.ico', 'formato': 'ICO', 'tamaño': (32, 32)},
                        'reportes': {'destino': 'Img/logo_reportes.png', 'formato': 'PNG', 'tamaño': (64, 64)},
                        'facturas': {'destino': 'Img/logo_facturas.png', 'formato': 'PNG', 'tamaño': (100, 100)}
                    }
                    
                    if seccion not in config_secciones:
                        return {
                            "status": "error", 
                            "message": f"Sección '{seccion}' no válida"
                        }
                    
                    config = config_secciones[seccion]
                    
                    # Crear backup si existe archivo actual
                    if os.path.exists(config['destino']):
                        backup_dir = "Img/backup"
                        os.makedirs(backup_dir, exist_ok=True)
                        backup_name = f"{os.path.splitext(os.path.basename(config['destino']))[0]}_backup{os.path.splitext(config['destino'])[1]}"
                        backup_path = os.path.join(backup_dir, backup_name)
                        
                        try:
                            import shutil
                            shutil.copy2(config['destino'], backup_path)
                            print(f"[LOGO] Backup creado: {backup_path}")
                        except Exception as backup_error:
                            print(f"[LOGO] Error creando backup: {backup_error}")
                    
                    # Redimensionar imagen
                    img_resized = img.resize(config['tamaño'], Image.Resampling.LANCZOS)
                    
                    # Guardar imagen
                    os.makedirs(os.path.dirname(config['destino']), exist_ok=True)
                    
                    if config['formato'] == 'ICO':
                        img_resized.save(config['destino'], format='ICO')
                    else:
                        img_resized.save(config['destino'], format=config['formato'])
                    
                    # Guardar en BD
                    size_kb = len(image_data) / 1024
                    guardar_logo_config(
                        seccion=seccion,
                        archivo_original=nombre_archivo,
                        archivo_destino=config['destino'],
                        dimensiones=f"{img.size[0]}x{img.size[1]}",
                        tamaño_kb=f"{size_kb:.1f}",
                        aplicado_por="Usuario Web"
                    )
                    
                    print(f"[LOGO] Logo aplicado exitosamente para {seccion}")
                    return {
                        "status": "success",
                        "message": f"Logo aplicado correctamente en {seccion}"
                    }
                    
                except ImportError as ie:
                    print(f"[LOGO] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos no disponibles: {str(ie)}"
                    }
                except Exception as apply_error:
                    print(f"[LOGO] Error aplicando logo: {apply_error}")
                    return {
                        "status": "error",
                        "message": f"Error aplicando logo: {str(apply_error)}"
                    }
            else:
                # Modo demo
                print(f"[LOGO] Modo demo - logo aplicado simulado para {seccion}")
                return {
                    "status": "success",
                    "message": f"Logo aplicado correctamente en {seccion} (modo demostración)"
                }
                
        except Exception as e:
            print(f"[LOGO] Error general aplicando logo: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    def restablecer_logos(self):
        """API: Restablecer logos desde respaldos"""
        try:
            print("[LOGO] Restableciendo logos desde respaldos...")
            
            if not DEMO_MODE:
                try:
                    import os
                    import shutil
                    
                    backup_dir = "Img/backup"
                    restaurados = []
                    
                    respaldos = {
                        'ventanas': {'backup': f"{backup_dir}/SM2_backup.ico", 'destino': 'Img/SM2.ico'},
                        'reportes': {'backup': f"{backup_dir}/logo_reportes_backup.png", 'destino': 'Img/logo_reportes.png'},
                        'facturas': {'backup': f"{backup_dir}/logo_facturas_backup.png", 'destino': 'Img/logo_facturas.png'}
                    }
                    
                    for seccion, config in respaldos.items():
                        if os.path.exists(config['backup']):
                            try:
                                shutil.copy2(config['backup'], config['destino'])
                                restaurados.append(seccion)
                                print(f"[LOGO] Restaurado {seccion} desde {config['backup']}")
                            except Exception as restore_error:
                                print(f"[LOGO] Error restaurando {seccion}: {restore_error}")
                    
                    if restaurados:
                        return {
                            "status": "success",
                            "message": f"Logos restaurados en: {', '.join(restaurados)}"
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "No se encontraron respaldos de logos"
                        }
                        
                except Exception as restore_error:
                    print(f"[LOGO] Error restableciendo logos: {restore_error}")
                    return {
                        "status": "error",
                        "message": f"Error restableciendo logos: {str(restore_error)}"
                    }
            else:
                # Modo demo
                return {
                    "status": "success",
                    "message": "Logos restablecidos correctamente (modo demostración)"
                }
                
        except Exception as e:
            print(f"[LOGO] Error general restableciendo logos: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    def obtener_historial_logos(self, limit=20):
        """API: Obtener historial de cambios de logos"""
        try:
            print(f"[LOGO] Obteniendo historial de logos (límite: {limit})")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import obtener_historial_logos
                    
                    historial = obtener_historial_logos(limit=limit)
                    
                    return {
                        "status": "success",
                        "data": historial if historial else []
                    }
                    
                except ImportError as ie:
                    print(f"[LOGO] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos no disponibles: {str(ie)}"
                    }
                except Exception as hist_error:
                    print(f"[LOGO] Error obteniendo historial: {hist_error}")
                    return {
                        "status": "error",
                        "message": f"Error obteniendo historial: {str(hist_error)}"
                    }
            else:
                # Historial demo  
                historial_demo = [
                    {
                        'seccion': 'ventanas',
                        'archivo_original': 'logo_ejemplo.ico',
                        'fecha_aplicado': '2025-10-15 14:30:00',
                        'aplicado_por': 'Usuario',
                        'dimensiones': '32x32',
                        'tamaño_kb': '15.2'
                    }
                ]
                
                return {
                    "status": "success",
                    "data": historial_demo
                }
                
        except Exception as e:
            print(f"[LOGO] Error general obteniendo historial: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
            }
    
    def listar_imagenes_galeria(self):
        """API: Listar imágenes en la galería (carpeta Logos)"""
        try:
            print("[LOGO] Listando imágenes de galería...")
            
            if not DEMO_MODE:
                try:
                    from Controller.SQL.db_operations import listar_imagenes_logos
                    
                    imagenes = listar_imagenes_logos()
                    
                    return {
                        "status": "success",
                        "data": imagenes if imagenes else []
                    }
                    
                except ImportError as ie:
                    print(f"[LOGO] Error importando módulos: {ie}")
                    return {
                        "status": "error",
                        "message": f"Módulos no disponibles: {str(ie)}"
                    }
                except Exception as gallery_error:
                    print(f"[LOGO] Error listando galería: {gallery_error}")
                    return {
                        "status": "error",
                        "message": f"Error listando galería: {str(gallery_error)}"
                    }
            else:
                # Galería demo
                galeria_demo = [
                    {
                        'nombre': 'logo_ejemplo1.png',
                        'ruta': 'Logos/logo_ejemplo1.png',
                        'tamaño_kb': '25.6',
                        'dimensiones': '64x64'
                    },
                    {
                        'nombre': 'logo_ejemplo2.ico',
                        'ruta': 'Logos/logo_ejemplo2.ico', 
                        'tamaño_kb': '12.3',
                        'dimensiones': '32x32'
                    }
                ]
                
                return {
                    "status": "success",
                    "data": galeria_demo
                }
                
        except Exception as e:
            print(f"[LOGO] Error general listando galería: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}"
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
                print("[DB] Verificando base de datos...")
                conn = obtener_conexion()
                if not conn:
                    print("[DB] Creando base de datos...")
                    crear_conexion_y_tablas()
                    conn = obtener_conexion()
                
                if conn:
                    cursor = conn.cursor()
                    
                    # Verificar que la tabla Emails exista
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Emails'")
                    table_exists = cursor.fetchone()
                    
                    if table_exists:
                        print("[DB] ✅ Tabla Emails encontrada")
                        
                        # Verificar contenido de la tabla Emails
                        cursor.execute("SELECT COUNT(*) FROM Emails")
                        count = cursor.fetchone()[0]
                        print(f"[DB] Registros en tabla Emails: {count}")
                        
                        if count > 0:
                            cursor.execute("SELECT email FROM Emails LIMIT 1")
                            sample_email = cursor.fetchone()
                            print(f"[DB] Email de muestra en BD: {sample_email[0] if sample_email else 'None'}")
                        
                    else:
                        print("[DB] ❌ Tabla Emails NO encontrada - creando...")
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Emails (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email TEXT NOT NULL,
                                pass TEXT NOT NULL,
                                createon TEXT NOT NULL,
                                updateon TEXT
                            )
                        """)
                        conn.commit()
                        print("[DB] ✅ Tabla Emails creada")
                    
                    conn.close()
                    
            except Exception as db_err:
                print(f"[DB] Error verificando base de datos: {db_err}")
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