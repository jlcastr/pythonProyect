"""
Launcher para el Sistema de Ventas con interfaz web
Este script permite elegir entre la interfaz tradicional de Tkinter o la nueva interfaz web
"""

import sys
import os
from pathlib import Path

# Añadir el directorio padre al path para importar módulos
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def check_web_dependencies():
    """Verificar si las dependencias web están instaladas"""
    try:
        import webview  # PyWebView para interfaz web nativa
        # Verificar que las funciones básicas estén disponibles
        webview.create_window
        return True
    except ImportError:
        return False
    except AttributeError:
        # PyWebView está instalado pero incompleto
        return False

def install_web_dependencies():
    """Instalar dependencias web"""
    print("Instalando dependencias para la interfaz web...")
    
    import subprocess
    
    requirements_file = current_dir / "requirements_web.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("[OK] Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error instalando dependencias: {e}")
        return False

def launch_web_interface():
    """Lanzar interfaz web"""
    try:
        from web_interface.main_web import main
        print("[START] Iniciando interfaz web nativa...")
        return main()
    except Exception as e:
        print(f"[ERROR] Error iniciando interfaz web: {e}")
        return 1

def launch_tkinter_interface():
    """Lanzar interfaz tradicional de Tkinter"""
    try:
        # Importar y ejecutar la interfaz Tkinter existente
        from MainPrint import main  # Asumiendo que MainPrint.py tiene una función main
        print("[START] Iniciando interfaz Tkinter...")
        return main()
    except ImportError:
        try:
            # Alternativa: ejecutar MainPrint.py directamente
            import subprocess
            result = subprocess.run([sys.executable, str(parent_dir / "MainPrint.py")])
            return result.returncode
        except Exception as e:
            print(f"[ERROR] Error iniciando interfaz Tkinter: {e}")
            return 1
    except Exception as e:
        print(f"[ERROR] Error iniciando interfaz Tkinter: {e}")
        return 1

def show_menu():
    """Mostrar menú de selección de interfaz"""
    print("\n" + "="*60)
    print("    SISTEMA DE VENTAS S&M - SELECTOR DE INTERFAZ")
    print("="*60)
    print("Seleccione la interfaz que desea usar:")
    print()
    print("1. [WEB] Interfaz Web (Moderna, responsiva)")
    print("2. [GUI] Interfaz Tkinter (Tradicional)")
    print("3. [CFG] Instalar dependencias web")
    print("4. [EXIT] Salir")
    print()
    
    while True:
        try:
            choice = input("Ingrese su opción (1-4): ").strip()
            
            if choice == "1":
                if not check_web_dependencies():
                    print("\n[WARN] Las dependencias web no estan instaladas.")
                    install_choice = input("Desea instalarlas ahora? (s/n): ").strip().lower()
                    
                    if install_choice in ['s', 'si', 'y', 'yes']:
                        if install_web_dependencies():
                            return launch_web_interface()
                        else:
                            print("[ERROR] No se pudieron instalar las dependencias")
                            return 1
                    else:
                        print("[WARN] No se puede usar la interfaz web sin las dependencias")
                        continue
                else:
                    return launch_web_interface()
            
            elif choice == "2":
                return launch_tkinter_interface()
            
            elif choice == "3":
                if install_web_dependencies():
                    print("[OK] Dependencias instaladas. Ya puede usar la interfaz web.")
                else:
                    print("[ERROR] Error instalando dependencias")
                continue
            
            elif choice == "4":
                print("[EXIT] Hasta luego!")
                return 0
            
            else:
                print("[ERROR] Opcion invalida. Por favor ingrese 1, 2, 3 o 4.")
        
        except KeyboardInterrupt:
            print("\n\n[EXIT] Hasta luego!")
            return 0
        except Exception as e:
            print(f"[ERROR] Error: {e}")

def main():
    """Función principal del launcher"""
    try:
        return show_menu()
    except Exception as e:
        print(f"[ERROR] Error fatal: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)