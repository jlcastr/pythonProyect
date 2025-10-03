import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
from PIL import Image, ImageTk
import shutil

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion, crear_recuadro_estandarizado

def mostrar_logo_en_frame(parent_frame, callback_volver):
    """
    Mostrar configuración de logo dentro de un frame existente usando el recuadro negro estándar
    
    Args:
        parent_frame: Frame padre donde mostrar la configuración de logo
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
        "🖼️ CONFIGURACIÓN DE LOGO", 
        callback_volver
    )
    
    # Configurar el frame_centrado para centrar todo el contenido
    frame_centrado.columnconfigure(0, weight=1)  # Columnas laterales con peso
    frame_centrado.columnconfigure(1, weight=0)  # Columna central sin peso
    frame_centrado.columnconfigure(2, weight=1)  # Columnas laterales con peso

    # Variables para los logos de cada sección
    logos = {
        'ventanas': {'archivo': None, 'preview': None, 'info': tk.StringVar()},
        'reportes': {'archivo': None, 'preview': None, 'info': tk.StringVar()},
        'facturas': {'archivo': None, 'preview': None, 'info': tk.StringVar()}
    }
    
    # Variable para aplicar a todas las secciones
    aplicar_a_todas = tk.BooleanVar(value=False)
    
    # Obtener logos actuales si existen
    if os.path.exists('Img/SM2.ico'):
        logos['ventanas']['info'].set('Img/SM2.ico - Logo actual')
    else:
        logos['ventanas']['info'].set('Sin logo configurado')
        
    if os.path.exists('Img/logo_reportes.png'):
        logos['reportes']['info'].set('Img/logo_reportes.png - Logo actual')
    else:
        logos['reportes']['info'].set('Sin logo configurado')
        
    if os.path.exists('Img/logo_facturas.png'):
        logos['facturas']['info'].set('Img/logo_facturas.png - Logo actual')
    else:
        logos['facturas']['info'].set('Sin logo configurado')

    # Diccionario para almacenar referencias a los preview_labels
    preview_labels = {}
    
    # Función para aplicar a todas las secciones
    def aplicar_archivo_a_todas(archivo, size_kb, img_size, seccion_origen):
        """Aplicar el mismo archivo a todas las secciones"""
        try:
            img = Image.open(archivo)
            info_text = f"{os.path.basename(archivo)} ({size_kb:.1f} KB, {img_size[0]}x{img_size[1]}px)"
            
            for key in logos.keys():
                if key != seccion_origen:
                    # Actualizar archivo e información
                    logos[key]['archivo'] = archivo
                    logos[key]['info'].set(info_text)
                    
                    # Actualizar preview si existe la referencia
                    if key in preview_labels:
                        img_preview = img.copy()
                        img_preview.thumbnail((60, 60), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img_preview)
                        
                        preview_labels[key].config(image=photo, text="")
                        preview_labels[key].image = photo
                        logos[key]['preview'] = photo
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar a todas las secciones:\n{str(e)}")

    # Función para crear una sección de logo
    def crear_seccion_logo(parent, titulo, icono, seccion_key, fila):
        # Frame principal de la sección
        seccion_frame = tk.LabelFrame(parent, text=f"{icono} {titulo}", 
                                     font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                     relief='groove', bd=2)
        seccion_frame.grid(row=fila, column=1, sticky='ew', pady=(0, 15), padx=10)
        seccion_frame.columnconfigure(1, weight=1)
        
        # Preview del logo
        preview_frame = tk.Frame(seccion_frame, bg='#ffffff', relief='solid', bd=1, height=80, width=80)
        preview_frame.grid(row=0, column=0, rowspan=3, pady=15, padx=15, sticky='n')
        preview_frame.pack_propagate(False)
        
        preview_label = tk.Label(preview_frame, text="Sin logo", bg='#ffffff', fg='#7f8c8d', font=("Arial", 8))
        preview_label.pack(expand=True)
        
        # Guardar referencia al preview_label
        preview_labels[seccion_key] = preview_label
        
        # Cargar logo actual si existe
        archivos_actuales = {
            'ventanas': 'Img/SM2.ico',
            'reportes': 'Img/logo_reportes.png', 
            'facturas': 'Img/logo_facturas.png'
        }
        
        if os.path.exists(archivos_actuales[seccion_key]):
            try:
                img = Image.open(archivos_actuales[seccion_key])
                img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                preview_label.config(image=photo, text="")
                preview_label.image = photo
            except:
                pass
        
        # Información del archivo
        info_label = tk.Label(seccion_frame, textvariable=logos[seccion_key]['info'], 
                             font=("Arial", 9), bg='#f8f9fa', fg='#7f8c8d', wraplength=300)
        info_label.grid(row=0, column=1, sticky='w', padx=15, pady=(15, 5))
        
        # Función para seleccionar archivo específico
        def seleccionar_archivo_seccion():
            tipos_archivo = [
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.ico"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("ICO", "*.ico"),
                ("Todos los archivos", "*.*")
            ]
            
            archivo = filedialog.askopenfilename(
                title=f"Seleccionar Logo para {titulo}",
                filetypes=tipos_archivo,
                initialdir=os.getcwd()
            )
            
            if archivo:
                try:
                    # Verificar que es una imagen válida
                    img = Image.open(archivo)
                    
                    # Mostrar información del archivo
                    size = os.path.getsize(archivo)
                    size_kb = size / 1024
                    logos[seccion_key]['info'].set(f"{os.path.basename(archivo)} ({size_kb:.1f} KB, {img.size[0]}x{img.size[1]}px)")
                    
                    # Crear preview
                    img_preview = img.copy()
                    img_preview.thumbnail((60, 60), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_preview)
                    
                    preview_label.config(image=photo, text="")
                    preview_label.image = photo
                    logos[seccion_key]['preview'] = photo
                    
                    # Guardar referencia a la imagen
                    logos[seccion_key]['archivo'] = archivo
                    
                    # Si está marcado "aplicar a todas", aplicar a las otras secciones
                    if aplicar_a_todas.get():
                        aplicar_archivo_a_todas(archivo, size_kb, img.size, seccion_key)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
                    logos[seccion_key]['info'].set("Error al cargar archivo")
                    preview_label.config(image="", text="Error")
                    logos[seccion_key]['archivo'] = None
        
        # Botón para seleccionar archivo
        btn_seleccionar = tk.Button(seccion_frame, text="📁 Seleccionar", command=seleccionar_archivo_seccion,
                                   bg='#3498db', fg='white', font=("Arial", 9, "bold"),
                                   relief='raised', bd=1, cursor='hand2', padx=10)
        btn_seleccionar.grid(row=1, column=1, sticky='w', padx=15, pady=5)
        
        # Botón para limpiar
        def limpiar_seccion():
            logos[seccion_key]['archivo'] = None
            logos[seccion_key]['info'].set('Sin logo configurado')
            preview_label.config(image="", text="Sin logo")
            preview_label.image = None
        
        btn_limpiar = tk.Button(seccion_frame, text="🗑️ Limpiar", command=limpiar_seccion,
                               bg='#95a5a6', fg='white', font=("Arial", 9, "bold"),
                               relief='raised', bd=1, cursor='hand2', padx=10)
        btn_limpiar.grid(row=2, column=1, sticky='w', padx=15, pady=(0, 15))
        
        return seccion_frame

    # Crear las tres secciones
    crear_seccion_logo(frame_centrado, "Icono de Ventanas", "🖥️", "ventanas", 1)
    crear_seccion_logo(frame_centrado, "Reportes PDF", "📊", "reportes", 2)
    crear_seccion_logo(frame_centrado, "Facturas y Documentos", "🧾", "facturas", 3)

    # Sección de opciones globales (centrada)
    opciones_frame = tk.LabelFrame(frame_centrado, text="⚙️ Opciones Globales", 
                                  font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                  relief='groove', bd=2)
    opciones_frame.grid(row=4, column=1, sticky='ew', pady=(0, 15), padx=10)

    # Checkbox para aplicar a todas las secciones
    tk.Checkbutton(opciones_frame, text="✅ Aplicar logo seleccionado a todas las secciones", 
                   variable=aplicar_a_todas, font=("Arial", 10, "bold"), 
                   bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', padx=15, pady=15)
    
    # Información sobre la opción
    info_global = tk.Label(opciones_frame, 
                          text="Cuando esta opción esté activada, al seleccionar un logo en cualquier sección\nse aplicará automáticamente a todas las demás secciones.", 
                          font=("Arial", 9), bg='#f8f9fa', fg='#7f8c8d', justify='left')
    info_global.pack(anchor='w', padx=15, pady=(0, 15))

    # Botones de acción (centrados)
    botones_frame = tk.Frame(frame_centrado, bg='#f8f9fa')
    botones_frame.grid(row=5, column=1, pady=15)

    def aplicar_logos():
        """Aplicar los logos de cada sección"""
        aplicados = []
        errores = []
        
        try:
            # Crear directorio de respaldo si no existe
            backup_dir = "Img/backup"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Procesar cada sección
            secciones_config = {
                'ventanas': {'destino': 'Img/SM2.ico', 'formato': 'ICO', 'tamaño': (32, 32), 'backup': 'SM2_backup.ico'},
                'reportes': {'destino': 'Img/logo_reportes.png', 'formato': 'PNG', 'tamaño': (64, 64), 'backup': 'logo_reportes_backup.png'},
                'facturas': {'destino': 'Img/logo_facturas.png', 'formato': 'PNG', 'tamaño': (100, 100), 'backup': 'logo_facturas_backup.png'}
            }
            
            for seccion, config in secciones_config.items():
                if logos[seccion]['archivo']:
                    try:
                        # Respaldar archivo actual si existe
                        if os.path.exists(config['destino']):
                            shutil.copy2(config['destino'], f"{backup_dir}/{config['backup']}")
                        
                        # Procesar imagen
                        img = Image.open(logos[seccion]['archivo'])
                        img_procesada = img.copy()
                        img_procesada = img_procesada.resize(config['tamaño'], Image.Resampling.LANCZOS)
                        
                        # Guardar en el formato correspondiente
                        if config['formato'] == 'ICO':
                            img_procesada.save(config['destino'], format='ICO')
                        else:
                            img_procesada.save(config['destino'], format='PNG')
                        
                        aplicados.append(seccion.title())
                        
                        # Actualizar información de la sección
                        logos[seccion]['info'].set(f"{config['destino']} - Logo aplicado")
                        
                    except Exception as e:
                        errores.append(f"{seccion.title()}: {str(e)}")
            
            # Mostrar resultado
            if aplicados and not errores:
                messagebox.showinfo("Éxito", 
                                   f"Logos aplicados correctamente en:\n• " + "\n• ".join(aplicados) + 
                                   "\n\nLos cambios se verán al reiniciar la aplicación.")
            elif aplicados and errores:
                messagebox.showwarning("Parcialmente completado",
                                      f"Logos aplicados en:\n• " + "\n• ".join(aplicados) +
                                      f"\n\nErrores en:\n• " + "\n• ".join(errores))
            elif errores:
                messagebox.showerror("Error", f"Errores al aplicar logos:\n• " + "\n• ".join(errores))
            else:
                messagebox.showwarning("Sin cambios", "No hay logos seleccionados para aplicar.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error general al aplicar logos:\n{str(e)}")

    def restablecer_logos():
        """Restablecer logos desde respaldos"""
        resultado = messagebox.askyesno("Confirmar", 
                                       "¿Estás seguro de que quieres restablecer los logos desde los respaldos?\n"
                                       "Se perderán los logos actuales.")
        if resultado:
            try:
                backup_dir = "Img/backup"
                restaurados = []
                
                # Archivos de respaldo
                respaldos = {
                    'ventanas': {'backup': f"{backup_dir}/SM2_backup.ico", 'destino': 'Img/SM2.ico'},
                    'reportes': {'backup': f"{backup_dir}/logo_reportes_backup.png", 'destino': 'Img/logo_reportes.png'},
                    'facturas': {'backup': f"{backup_dir}/logo_facturas_backup.png", 'destino': 'Img/logo_facturas.png'}
                }
                
                for seccion, config in respaldos.items():
                    if os.path.exists(config['backup']):
                        shutil.copy2(config['backup'], config['destino'])
                        logos[seccion]['info'].set(f"{config['destino']} - Logo restaurado")
                        restaurados.append(seccion.title())
                
                if restaurados:
                    messagebox.showinfo("Éxito", f"Logos restaurados en:\n• " + "\n• ".join(restaurados))
                else:
                    messagebox.showinfo("Información", "No hay logos de respaldo disponibles.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al restablecer logos:\n{str(e)}")

    def limpiar_todas():
        """Limpiar todas las selecciones"""
        resultado = messagebox.askyesno("Confirmar", "¿Limpiar todas las selecciones actuales?")
        if resultado:
            for seccion in logos.keys():
                logos[seccion]['archivo'] = None
                logos[seccion]['info'].set('Sin logo configurado')
            messagebox.showinfo("Listo", "Todas las selecciones han sido limpiadas.")

    # Botón aplicar
    btn_aplicar = tk.Button(botones_frame, text="✅ Aplicar Logos", command=aplicar_logos,
                           bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                           relief='raised', bd=2, cursor='hand2', padx=20)
    btn_aplicar.pack(side="left", padx=5)

    # Botón restablecer
    btn_restablecer = tk.Button(botones_frame, text="🔄 Restablecer", command=restablecer_logos,
                               bg='#e74c3c', fg='white', font=("Arial", 10, "bold"),
                               relief='raised', bd=2, cursor='hand2', padx=15)
    btn_restablecer.pack(side="left", padx=5)
    
    # Botón limpiar todo
    btn_limpiar_todo = tk.Button(botones_frame, text="🗑️ Limpiar Todo", command=limpiar_todas,
                                bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                                relief='raised', bd=2, cursor='hand2', padx=15)
    btn_limpiar_todo.pack(side="left", padx=5)


def mostrar_logo(parent=None):
    """
    Función para mostrar configuración de logo en ventana separada
    
    Args:
        parent: Ventana padre (opcional)
    """
    root = tk.Toplevel(parent) if parent else tk.Toplevel()
    root.title("🖼️ Configuración de Logo")
    root.geometry("700x700")
    root.resizable(True, True)
    root.configure(bg='#ecf0f1')
    
    # Configurar ícono
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Mostrar la configuración en el frame de la ventana
    mostrar_logo_en_frame(root, root.destroy)
    
    # Manejar cierre de ventana
    def on_close():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    # Prueba de la configuración de logo
    root = tk.Tk()
    root.title("Prueba - Configuración de Logo")
    root.geometry("800x800")
    
    def dummy_volver():
        print("Volver al menú de configuraciones")
    
    mostrar_logo_en_frame(root, dummy_volver)
    root.mainloop()
