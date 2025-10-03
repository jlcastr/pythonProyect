import tkinter as tk
from tkinter import ttk
import sys
import os

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion, crear_recuadro_estandarizado

def mostrar_apariencia_en_frame(parent_frame, callback_volver):
    """
    Mostrar configuración de apariencia dentro de un frame existente usando el recuadro negro estándar
    
    Args:
        parent_frame: Frame padre donde mostrar la configuración de apariencia
        callback_volver: Función a llamar para volver al menú de configuraciones
    """
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Configurar estilos centralizados
    configurar_estilos_aplicacion()
    
    # Crear la interfaz con recuadro negro estándar usando función reutilizable
    main_frame, frame_centrado = crear_recuadro_estandarizado(
        parent_frame, 
        "🎨 CONFIGURACIÓN DE APARIENCIA", 
        callback_volver
    )
    
    # Configurar el frame_centrado para centrar todo el contenido
    frame_centrado.columnconfigure(0, weight=1)  # Columnas laterales con peso
    frame_centrado.columnconfigure(1, weight=0)  # Columna central sin peso
    frame_centrado.columnconfigure(2, weight=1)  # Columnas laterales con peso

    # Sección de temas (centrada)
    temas_frame = tk.LabelFrame(frame_centrado, text="🎨 Temas de Colores", 
                               font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                               relief='groove', bd=2)
    temas_frame.grid(row=1, column=1, sticky='ew', pady=(0, 15), padx=10)
    temas_frame.columnconfigure(0, weight=1)
    temas_frame.columnconfigure(1, weight=1)

    # Variables para temas
    tema_var = tk.StringVar(value="claro")
    
    # Radio buttons para temas
    tk.Label(temas_frame, text="Selecciona el tema:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky='w', padx=15)
    
    tk.Radiobutton(temas_frame, text="🌞 Tema Claro", variable=tema_var, value="claro",
                   font=("Arial", 10), bg='#f8f9fa', fg='#2c3e50').grid(row=1, column=0, sticky='w', padx=15, pady=5)
    
    tk.Radiobutton(temas_frame, text="🌙 Tema Oscuro", variable=tema_var, value="oscuro",
                   font=("Arial", 10), bg='#f8f9fa', fg='#2c3e50').grid(row=1, column=1, sticky='w', padx=15, pady=5)
    
    tk.Radiobutton(temas_frame, text="🌅 Tema Automático", variable=tema_var, value="auto",
                   font=("Arial", 10), bg='#f8f9fa', fg='#2c3e50').grid(row=2, column=0, columnspan=2, sticky='w', padx=15, pady=5)

    # Sección de colores personalizados (centrada)
    colores_frame = tk.LabelFrame(frame_centrado, text="🎨 Colores Personalizados", 
                                 font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                 relief='groove', bd=2)
    colores_frame.grid(row=2, column=1, sticky='ew', pady=(0, 15), padx=10)
    colores_frame.columnconfigure(1, weight=1)

    # Color principal
    tk.Label(colores_frame, text="Color principal:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, sticky='w', padx=15, pady=(10, 5))
    
    color_principal = tk.Button(colores_frame, text="  ", bg="#3498db", width=3, height=1,
                               relief="solid", bd=1, cursor="hand2")
    color_principal.grid(row=0, column=1, sticky='w', padx=15, pady=(10, 5))

    # Color secundario
    tk.Label(colores_frame, text="Color secundario:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=1, column=0, sticky='w', padx=15, pady=5)
    
    color_secundario = tk.Button(colores_frame, text="  ", bg="#2ecc71", width=3, height=1,
                                relief="solid", bd=1, cursor="hand2")
    color_secundario.grid(row=1, column=1, sticky='w', padx=15, pady=5)

    # Sección de preview (centrada)
    preview_frame = tk.LabelFrame(frame_centrado, text="👁️ Vista Previa", 
                                 font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                 relief='groove', bd=2)
    preview_frame.grid(row=3, column=1, sticky='ew', pady=(0, 15), padx=10)

    # Ejemplo de vista previa
    preview_text = tk.Label(preview_frame, text="Ejemplo de texto con la configuración actual", 
                           font=("Arial", 12), bg='#ffffff', fg='#2c3e50', 
                           relief="solid", bd=1, pady=10, padx=20)
    preview_text.pack(pady=15, padx=15, fill='x')

    # Botones de acción (centrados)
    botones_frame = tk.Frame(frame_centrado, bg='#f8f9fa')
    botones_frame.grid(row=4, column=1, pady=15)

    def aplicar_cambios():
        """Aplicar los cambios de apariencia"""
        from tkinter import messagebox
        messagebox.showinfo("Aplicar Cambios", 
                           f"Configuración aplicada:\n\n"
                           f"• Tema: {tema_var.get().title()}\n"
                           f"• Colores personalizados aplicados\n\n"
                           f"Los cambios se aplicarán al reiniciar la aplicación.")

    def restablecer_valores():
        """Restablecer valores por defecto"""
        tema_var.set("claro")
        color_principal.config(bg="#3498db")
        color_secundario.config(bg="#2ecc71")

    def seleccionar_color(boton_color):
        """Seleccionar color personalizado"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Seleccionar Color")
        if color[1]:  # Si se seleccionó un color
            boton_color.config(bg=color[1])

    # Configurar eventos de botones de color
    color_principal.config(command=lambda: seleccionar_color(color_principal))
    color_secundario.config(command=lambda: seleccionar_color(color_secundario))

    # Botón aplicar
    btn_aplicar = tk.Button(botones_frame, text="✅ Aplicar Cambios", command=aplicar_cambios,
                           bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                           relief='raised', bd=2, cursor='hand2', padx=20)
    btn_aplicar.pack(side="left", padx=10)

    # Botón restablecer
    btn_restablecer = tk.Button(botones_frame, text="🔄 Restablecer", command=restablecer_valores,
                               bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                               relief='raised', bd=2, cursor='hand2', padx=20)
    btn_restablecer.pack(side="left", padx=10)

    # Función para actualizar vista previa
    def actualizar_preview(*args):
        """La vista previa ahora solo muestra el tema seleccionado"""
        pass


def mostrar_apariencia(parent=None):
    """
    Función para mostrar configuración de apariencia en ventana separada
    
    Args:
        parent: Ventana padre (opcional)
    """
    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("🎨 Configuración de Apariencia")
    root.geometry("700x600")
    root.resizable(True, True)
    root.configure(bg='#ecf0f1')
    
    # Configurar ícono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Mostrar la configuración en el frame de la ventana
    mostrar_apariencia_en_frame(root, root.destroy)
    
    # Manejar cierre de ventana
    def on_close():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    # Prueba de la configuración de apariencia
    root = tk.Tk()
    root.title("Prueba - Configuración de Apariencia")
    root.geometry("800x700")
    
    def dummy_volver():
        print("Volver al menú de configuraciones")
    
    mostrar_apariencia_en_frame(root, dummy_volver)
    root.mainloop()
