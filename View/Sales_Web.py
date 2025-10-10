"""
Módulo de Ventas - Interfaz Web
Sistema de Ventas S&M
Versión: 2.0 - Interfaz Web Nativa
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import threading

# Importar módulos del sistema
try:
    import Controller.utils as utils
    import Controller.SQL.db_operations as db_operations
    from Controller.SQL.sqlite_utils import db_optimizer, guardar_venta_optimizada
    from config.db_setup import obtener_conexion
except ImportError as e:
    print(f"[WARN] Error importando módulos: {e}")

class SalesWebInterface:
    """Interfaz web para el módulo de ventas"""
    
    def __init__(self):
        self.venta_actual_id = None
        self.folio_actual = None
        self.productos_actuales = []
        self.cliente_actual = "Consumidor Final"
        self._db_lock = threading.Lock()  # Lock para operaciones de BD
        
        # Configurar conexión a base de datos
        try:
            from config.db_setup import obtener_conexion
            self.conn = obtener_conexion()
            if self.conn:
                self.cursor = self.conn.cursor()
                print("[INFO] Conexión a base de datos establecida")
            else:
                self.conn = None
                self.cursor = None
                print("[WARN] No se pudo establecer conexión a BD")
        except Exception as e:
            print(f"[WARN] Error conexión BD: {e}")
            self.conn = None
            self.cursor = None
    
    def generar_folio(self) -> str:
        """Generar nuevo folio de venta"""
        try:
            if self.cursor:
                # Obtener el último folio de VentaMaster
                self.cursor.execute("SELECT MAX(folio) FROM VentaMaster")
                resultado = self.cursor.fetchone()
                ultimo_folio = resultado[0] if resultado and resultado[0] else 0
                return str(ultimo_folio + 1).zfill(6)
            else:
                # Modo demostración
                return datetime.now().strftime("%Y%m%d%H%M%S")[-6:]
        except Exception as e:
            print(f"[ERROR] Error generando folio: {e}")
            return datetime.now().strftime("%Y%m%d%H%M%S")[-6:]
    
    def validar_producto(self, descripcion: str, precio: str) -> Dict[str, Any]:
        """Validar datos del producto"""
        if not descripcion.strip():
            return {"valido": False, "error": "La descripción no puede estar vacía"}
        
        try:
            precio_float = float(precio.replace(',', '.'))
            if precio_float <= 0:
                return {"valido": False, "error": "El precio debe ser mayor a cero"}
            return {"valido": True, "precio": precio_float}
        except ValueError:
            return {"valido": False, "error": "El precio debe ser un número válido"}
    
    def agregar_producto(self, descripcion: str, precio: str) -> Dict[str, Any]:
        """Agregar producto a la venta actual"""
        try:
            # Validar producto
            validacion = self.validar_producto(descripcion, precio)
            if not validacion["valido"]:
                return {"status": "error", "message": validacion["error"]}
            
            # Generar folio si no existe
            if not self.folio_actual:
                self.folio_actual = self.generar_folio()
            
            # Crear producto
            producto = {
                "descripcion": descripcion.strip(),
                "precio": validacion["precio"],
                "fecha_venta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "folio": self.folio_actual
            }
            
            # Agregar a la lista actual (solo en memoria hasta finalizar venta)
            self.productos_actuales.append(producto)
            
            print(f"[INFO] Producto agregado - Folio: {self.folio_actual}, Descripción: {producto['descripcion']}, Precio: ${producto['precio']}")
            
            return {
                "status": "success", 
                "message": "Producto agregado correctamente",
                "folio": self.folio_actual,
                "productos": self.productos_actuales,
                "total": sum(p["precio"] for p in self.productos_actuales)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error agregando producto: {str(e)}"}
    
    def eliminar_producto(self, indice: int) -> Dict[str, Any]:
        """Eliminar producto de la venta"""
        try:
            if 0 <= indice < len(self.productos_actuales):
                producto_eliminado = self.productos_actuales.pop(indice)
                
                print(f"[INFO] Producto eliminado - Descripción: {producto_eliminado['descripcion']}, Precio: ${producto_eliminado['precio']}")
                
                return {
                    "status": "success",
                    "message": "Producto eliminado correctamente",
                    "productos": self.productos_actuales,
                    "total": sum(p["precio"] for p in self.productos_actuales)
                }
            else:
                return {"status": "error", "message": "Índice de producto inválido"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error eliminando producto: {str(e)}"}
    
    def modificar_producto(self, indice: int, descripcion: str, precio: str) -> Dict[str, Any]:
        """Modificar producto existente"""
        try:
            if not (0 <= indice < len(self.productos_actuales)):
                return {"status": "error", "message": "Índice de producto inválido"}
            
            # Validar nuevos datos
            validacion = self.validar_producto(descripcion, precio)
            if not validacion["valido"]:
                return {"status": "error", "message": validacion["error"]}
            
            # Actualizar producto
            producto_anterior = self.productos_actuales[indice].copy()
            self.productos_actuales[indice].update({
                "descripcion": descripcion.strip(),
                "precio": validacion["precio"]
            })
            
            # Actualizar en base de datos si está disponible
            if self.cursor:
                try:
                    self.cursor.execute("""
                        UPDATE ventas_items 
                        SET descripcion = ?, precio = ?
                        WHERE descripcion = ? AND precio = ?
                        LIMIT 1
                    """, (descripcion.strip(), validacion["precio"],
                         producto_anterior["descripcion"], 
                         producto_anterior["precio"], 
                         producto_anterior["folio"]))
                    self.conn.commit()
                except Exception as e:
                    print(f"[WARN] Error actualizando BD: {e}")
            
            return {
                "status": "success",
                "message": "Producto modificado correctamente",
                "productos": self.productos_actuales,
                "total": sum(p["precio"] for p in self.productos_actuales)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error modificando producto: {str(e)}"}
    
    def limpiar_venta(self) -> Dict[str, Any]:
        """Limpiar la venta actual"""
        try:
            # Eliminar productos de base de datos si está disponible
            if self.cursor and self.folio_actual:
                try:
                    self.cursor.execute("DELETE FROM productos_venta WHERE folio = ?", 
                                      (self.folio_actual,))
                    self.conn.commit()
                except Exception as e:
                    print(f"[WARN] Error limpiando BD: {e}")
            
            # Resetear variables
            self.productos_actuales = []
            self.folio_actual = None
            self.venta_actual_id = None
            self.cliente_actual = "Consumidor Final"
            
            return {
                "status": "success",
                "message": "Venta limpiada correctamente",
                "productos": [],
                "total": 0
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error limpiando venta: {str(e)}"}
    
    def finalizar_venta(self, cliente: str = "Consumidor Final") -> Dict[str, Any]:
        """Finalizar la venta actual"""
        try:
            print(f"[DEBUG] finalizar_venta llamado con cliente: {cliente}")
            print(f"[DEBUG] productos_actuales count: {len(self.productos_actuales)}")
            print(f"[DEBUG] productos_actuales: {self.productos_actuales}")
            print(f"[DEBUG] folio_actual: {self.folio_actual}")
            
            if not self.productos_actuales:
                print("[ERROR] No hay productos en la venta - productos_actuales está vacío")
                return {"status": "error", "message": "No hay productos en la venta"}
            
            self.cliente_actual = cliente.strip() or "Consumidor Final"
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Calcular total  
            total = sum(p["precio"] for p in self.productos_actuales)
            print(f"[DEBUG] Total calculado: ${total}")
            
            # Guardar venta en base de datos usando la estructura correcta con lock
            if self.cursor and self.folio_actual:
                with self._db_lock:  # Usar lock para thread safety
                    try:
                        # 1. Insertar en VentaMaster
                        self.cursor.execute("""
                            INSERT INTO VentaMaster (folio, fecha_venta, cliente)
                            VALUES (?, ?, ?)
                        """, (self.folio_actual, fecha_actual, self.cliente_actual))
                        
                        venta_master_id = self.cursor.lastrowid
                        self.venta_actual_id = venta_master_id
                        
                        # 2. Insertar productos en ventas_items
                        for producto in self.productos_actuales:
                            self.cursor.execute("""
                                INSERT INTO ventas_items (descripcion, precio, fecha_venta, venta_master_id)
                                VALUES (?, ?, ?, ?)
                            """, (producto["descripcion"], producto["precio"], fecha_actual, venta_master_id))
                        
                        self.conn.commit()
                        print(f"[INFO] Venta guardada en BD - Folio: {self.folio_actual}, Master ID: {venta_master_id}, Productos: {len(self.productos_actuales)}")
                        
                    except Exception as e:
                        print(f"[ERROR] Error guardando venta en BD: {e}")
                        if self.conn:
                            self.conn.rollback()
                        return {"status": "error", "message": f"Error guardando en la base de datos: {str(e)}"}
            
            venta_finalizada = {
                "folio": self.folio_actual,
                "cliente": self.cliente_actual,
                "productos": self.productos_actuales.copy(),
                "total": total,
                "fecha": fecha_actual
            }
            
            # Limpiar para nueva venta
            self.productos_actuales = []
            self.folio_actual = None
            self.venta_actual_id = None
            
            return {
                "status": "success",
                "message": f"Venta {venta_finalizada['folio']} guardada exitosamente en la base de datos",
                "venta": venta_finalizada
            }
            
        except Exception as e:
            print(f"[ERROR] Error finalizando venta: {e}")
            return {"status": "error", "message": f"Error finalizando venta: {str(e)}"}
    
    def obtener_estado_venta(self) -> Dict[str, Any]:
        """Obtener el estado actual de la venta"""
        return {
            "folio": self.folio_actual,
            "cliente": self.cliente_actual,
            "productos": self.productos_actuales,
            "total": sum(p["precio"] for p in self.productos_actuales),
            "cantidad_productos": len(self.productos_actuales)
        }
    
    def imprimir_venta(self) -> Dict[str, Any]:
        """Generar impresión de la venta"""
        try:
            if not self.folio_actual:
                return {"status": "error", "message": "No hay venta para imprimir"}
            
            # Aquí iría la lógica de impresión
            # Por ahora, simulamos la impresión
            return {
                "status": "success",
                "message": "Venta enviada a impresión",
                "folio": self.folio_actual
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error imprimiendo: {str(e)}"}
    
    def enviar_por_correo(self, email: str) -> Dict[str, Any]:
        """Enviar venta por correo electrónico"""
        try:
            print(f"[DEBUG] Iniciando envío de correo. Folio actual: {self.folio_actual}")
            
            if not email or "@" not in email:
                return {"status": "error", "message": "Dirección de correo electrónico inválida"}
            
            # Validación más robusta del email
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return {"status": "error", "message": "Formato de correo electrónico inválido"}
            
            # Crear nueva conexión a la base de datos para evitar problemas de threading
            import sqlite3
            import os
            
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'sales_system.db')
            print(f"[DEBUG] Conectando a la base de datos: {db_path}")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Estrategia de búsqueda: primero por folio, luego la más reciente
            venta_row = None
            
            # 1. Intentar buscar por folio actual si existe
            if self.folio_actual:
                print(f"[DEBUG] Buscando venta con folio: {self.folio_actual}")
                cursor.execute("SELECT id, fecha_venta, cliente, folio FROM VentaMaster WHERE folio = ?", (self.folio_actual,))
                venta_row = cursor.fetchone()
                
            # 2. Si no se encuentra, buscar la venta más reciente
            if not venta_row:
                print("[DEBUG] No se encontró venta por folio, buscando la más reciente")
                cursor.execute("SELECT id, fecha_venta, cliente, folio FROM VentaMaster ORDER BY id DESC LIMIT 1")
                venta_row = cursor.fetchone()
                
                if venta_row:
                    # Actualizar el folio actual
                    self.folio_actual = venta_row[3]
                    print(f"[DEBUG] Usando venta más reciente - Folio: {self.folio_actual}")
                    
            # 3. Si aún no hay venta, mostrar mensaje con opción de demo
            if not venta_row:
                print("[DEBUG] No se encontraron ventas finalizadas")
                conn.close()
                return {
                    "status": "warning", 
                    "message": "No hay venta finalizada para enviar",
                    "details": "Debe agregar productos y finalizar una venta primero.",
                    "action": "show_demo_option"
                }
            
            venta_id = venta_row[0]
            fecha_venta = venta_row[1]
            cliente = venta_row[2] or "Consumidor Final"
            folio_venta = venta_row[3]
            
            print(f"[DEBUG] Datos de venta - ID: {venta_id}, Cliente: {cliente}, Folio: {folio_venta}")
            
            # Obtener productos de la venta (probar ambos nombres de columna por compatibilidad)
            cursor.execute("SELECT descripcion, precio FROM ventas_items WHERE venta_master_id = ?", (venta_id,))
            productos_db = cursor.fetchall()
            
            # Si no encuentra productos con venta_master_id, probar con venta_id
            if not productos_db:
                print("[DEBUG] Probando buscar productos con venta_id en lugar de venta_master_id")
                cursor.execute("SELECT descripcion, precio FROM ventas_items WHERE venta_id = ?", (venta_id,))
                productos_db = cursor.fetchall()
            
            print(f"[DEBUG] Productos encontrados: {len(productos_db) if productos_db else 0}")
            
            if not productos_db:
                conn.close()
                return {"status": "error", "message": "No se encontraron productos en la venta. Verifique que la venta tenga productos agregados."}
            
            # Preparar datos para el PDF
            productos = []
            total = 0
            for descripcion, precio in productos_db:
                producto = {
                    'descripcion': descripcion,
                    'cantidad': 1,
                    'precio': float(precio),
                    'importe': float(precio)
                }
                productos.append(producto)
                total += float(precio)
            
            # Usar el folio de la venta encontrada
            folio_a_usar = folio_venta or self.folio_actual
            
            datos_venta = {
                'fecha': fecha_venta,
                'cliente': cliente,
                'folio': folio_a_usar
            }
            
            print(f"[DEBUG] Generando PDF con folio: {folio_a_usar}")
            
            # Generar PDF
            try:
                from Controller.createpdf import generar_nota_venta
                import os, tempfile, shutil
                
                nombre_archivo = f"nota_venta_{folio_a_usar}.pdf"
                print(f"[DEBUG] Generando PDF: {nombre_archivo}")
                generar_nota_venta(nombre_archivo, datos_venta, productos, total, abrir_pdf=False)
                
                # Copiar a archivo temporal para evitar problemas de permisos
                temp_dir = tempfile.gettempdir()
                temp_pdf = os.path.join(temp_dir, f"temp_{nombre_archivo}")
                shutil.copy2(nombre_archivo, temp_pdf)
                print(f"[DEBUG] PDF copiado a: {temp_pdf}")
                
                # Enviar correo con PDF adjunto
                try:
                    from Controller.email import enviar_correo_desde_db
                    cuerpo = f"Estimado/a cliente,\n\nAdjunto encontrará su comprobante de compra.\n\nFolio: {folio_a_usar}\nCliente: {cliente}\nTotal: ${total:.2f}\n\nGracias por su compra.\n\nSistema de Ventas S&M"
                    print(f"[DEBUG] Enviando correo a: {email}")
                    
                    enviar_correo_desde_db(email, cuerpo, adjunto_path=temp_pdf)
                    
                    # Limpiar archivo temporal
                    try:
                        os.remove(temp_pdf)
                    except:
                        pass
                    
                    print("[DEBUG] Correo enviado exitosamente")
                    
                    # Cerrar conexión a la base de datos
                    conn.close()
                    
                    return {
                        "status": "success",
                        "message": f"Venta enviada exitosamente a {email}",
                        "folio": folio_a_usar,
                        "cliente": cliente,
                        "total": total
                    }
                    
                except Exception as email_error:
                    # Limpiar archivo temporal en caso de error
                    try:
                        if os.path.exists(temp_pdf):
                            os.remove(temp_pdf)
                    except:
                        pass
                    
                    # Cerrar conexión a la base de datos
                    conn.close()
                    
                    return {"status": "error", "message": f"Error enviando correo: {str(email_error)}"}
                    
            except Exception as pdf_error:
                # Cerrar conexión a la base de datos
                conn.close()
                return {"status": "error", "message": f"Error generando PDF: {str(pdf_error)}"}
            
        except Exception as e:
            # Cerrar conexión a la base de datos si existe
            try:
                conn.close()
            except:
                pass
            return {"status": "error", "message": f"Error inesperado: {str(e)}"}

# Clase principal para compatibilidad
class Sales:
    """Clase Sales adaptada para interfaz web"""
    
    def __init__(self):
        """Inicializar el módulo de ventas web"""
        self.sales_interface = SalesWebInterface()
        print("[INFO] Módulo de ventas inicializado con interfaz web")
    
    def obtener_api(self):
        """Obtener la interfaz API para comunicación con JavaScript"""
        return self.sales_interface
    
    def mostrar(self):
        """Método para compatibilidad - ya no se usa con interfaz web"""
        print("[INFO] Usando interfaz web nativa para ventas")
        return self.sales_interface

# Funciones API para JavaScript
def crear_api_ventas():
    """Crear API de ventas para uso en la interfaz web"""
    sales = Sales()
    return sales.obtener_api()

# Para compatibilidad con el sistema existente
def crear_pantalla_principal(conn, cursor, menubar):
    """Función de compatibilidad - redirige a interfaz web"""
    print("[INFO] Redirigiendo a interfaz web nativa...")
    sales = Sales()
    return sales.mostrar()

def crear_interfaz_ventas_en_frame(parent_frame, conn, cursor, callback_volver):
    """Función de compatibilidad - redirige a interfaz web"""
    print("[INFO] Redirigiendo a interfaz web nativa...")
    sales = Sales()
    return sales.mostrar()