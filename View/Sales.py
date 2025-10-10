"""
Módulo de Ventas - Interfaz Web Nativa
Sistema de Ventas S&M
Versión: 2.0 - Transición a Web
"""

def Sales(root, usuario_actual):
    """
    Función principal del módulo de ventas - Redirección a interfaz web
    
    Args:
        root: Ventana principal de la aplicación (no utilizada en versión web)
        usuario_actual: Usuario logueado en el sistema
    """
    print("🔄 Módulo de Ventas - Iniciando interfaz web...")
    
    # Importar y lanzar la interfaz web
    try:
        import subprocess
        import sys
        from pathlib import Path
        
        # Obtener la ruta del launcher principal
        project_root = Path(__file__).parent.parent
        launcher_path = project_root / "launcher.py"
        
        if launcher_path.exists():
            # Lanzar la interfaz web directamente
            print("🚀 Lanzando interfaz web de ventas...")
            subprocess.Popen([sys.executable, str(launcher_path), "--web", "--module=sales"], 
                           cwd=str(project_root))
        else:
            # Fallback: usar la interfaz web local
            from View.Sales_Web import SalesWebInterface
            sales_interface = SalesWebInterface()
            print("✅ Interfaz web de ventas iniciada")
            
    except ImportError as e:
        print(f"❌ Error: Interfaz web no disponible - {e}")
        print("💡 Ejecuta 'python launcher.py' para instalar dependencias web")
        
        # Mostrar mensaje de error en la ventana principal si está disponible
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            if root:
                messagebox.showinfo(
                    "Actualización Requerida",
                    "El módulo de ventas ha sido actualizado a una interfaz web.\n\n"
                    "Para usar la nueva interfaz:\n"
                    "1. Cierra esta aplicación\n"
                    "2. Ejecuta 'python launcher.py'\n"
                    "3. Selecciona 'Interfaz Web'\n\n"
                    "La nueva interfaz es más moderna y se adapta automáticamente a diferentes resoluciones."
                )
                
                # Crear ventana de información temporal
                info_window = tk.Toplevel(root)
                info_window.title("Módulo Actualizado")
                info_window.geometry("500x300")
                info_window.resizable(False, False)
                
                # Centrar ventana
                info_window.transient(root)
                info_window.grab_set()
                
                frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
                frame.pack(fill=tk.BOTH, expand=True)
                
                title_label = tk.Label(frame, text="🎉 ¡Módulo Actualizado!", 
                                     font=("Arial", 16, "bold"), bg="white", fg="#2c3e50")
                title_label.pack(pady=(0, 20))
                
                message = """El módulo de Ventas ha sido actualizado con una interfaz web moderna que:

✅ Se adapta automáticamente a diferentes resoluciones
✅ Tiene un diseño más moderno y intuitivo  
✅ Ofrece mejor rendimiento
✅ Es compatible con todos los sistemas operativos

Para usar la nueva interfaz:
1. Cierra esta aplicación
2. Ejecuta 'python launcher.py'
3. Selecciona 'Interfaz Web'"""
                
                text_label = tk.Label(frame, text=message, font=("Arial", 11), 
                                    bg="white", fg="#34495e", justify=tk.LEFT, wraplength=450)
                text_label.pack(pady=(0, 20))
                
                button_frame = tk.Frame(frame, bg="white")
                button_frame.pack()
                
                def close_and_launch():
                    info_window.destroy()
                    root.quit()
                
                ok_button = tk.Button(button_frame, text="Entendido", 
                                    command=info_window.destroy,
                                    bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                                    padx=20, pady=8, relief=tk.FLAT)
                ok_button.pack(side=tk.LEFT, padx=(0, 10))
                
                launch_button = tk.Button(button_frame, text="Cerrar y Actualizar", 
                                        command=close_and_launch,
                                        bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                                        padx=20, pady=8, relief=tk.FLAT)
                launch_button.pack(side=tk.LEFT)
                
        except ImportError:
            print("No se puede mostrar interfaz gráfica de error")
            
    except Exception as e:
        print(f"❌ Error inesperado al lanzar interfaz web: {e}")


# Función de compatibilidad para llamadas directas
def crear_interfaz_ventas(root, usuario_actual):
    """Función de compatibilidad - redirige a Sales()"""
    Sales(root, usuario_actual)

def crear_interfaz_ventas_en_frame(parent_frame, conn, cursor, callback_volver):
    """Función de compatibilidad para frame - redirige a Sales()"""
    Sales(None, None)

def crear_pantalla_principal(conn, cursor, menubar):
    """Función de compatibilidad para pantalla principal - redirige a Sales()"""
    Sales(None, None)