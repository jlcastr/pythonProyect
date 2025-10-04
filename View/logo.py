import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
from PIL import Image, ImageTk
import shutil

# Agregar el directorio padre al path para importar estilos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.styles import configurar_estilos_aplicacion, crear_recuadro_estandarizado
from Controller.SQL.db_operations import (
    crear_tabla_logos_config, guardar_logo_config, consultar_logo_config, 
    obtener_historial_logos, eliminar_logo_config,
    crear_tabla_titles, guardar_titulo_config, consultar_titulo_config, obtener_historial_titulos
)

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
    
    # Inicializar tablas en BD si no existen
    try:
        crear_tabla_logos_config()
        crear_tabla_titles()
    except Exception as e:
        print(f"Error al crear tablas: {e}")
    
    # Crear la interfaz con recuadro negro estándar usando función reutilizable
    main_frame, frame_principal = crear_recuadro_estandarizado(
        parent_frame, 
        "🖼️ CONFIGURACIÓN DE LOGO", 
        callback_volver
    )
    
    # Crear canvas y scrollbar para contenido scrolleable
    canvas = tk.Canvas(frame_principal, bg='#f8f9fa', highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    frame_centrado = tk.Frame(canvas, bg='#f8f9fa')
    
    # Configurar scrolling
    frame_centrado.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=frame_centrado, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Configurar el frame_centrado para centrar todo el contenido
    frame_centrado.columnconfigure(0, weight=1)  # Columnas laterales con peso
    frame_centrado.columnconfigure(1, weight=0)  # Columna central sin peso
    frame_centrado.columnconfigure(2, weight=1)  # Columnas laterales con peso
    
    # Función para hacer scroll con la rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # Función para bind recursivo del scroll a todos los widgets
    def bind_mousewheel_recursive(widget):
        widget.bind("<MouseWheel>", _on_mousewheel)
        for child in widget.winfo_children():
            bind_mousewheel_recursive(child)
    
    # Bind del scroll del mouse al canvas y todos sus hijos
    canvas.bind("<MouseWheel>", _on_mousewheel)
    frame_centrado.bind("<MouseWheel>", _on_mousewheel)
    
    # Función para aplicar bind a nuevos widgets que se agreguen
    def aplicar_scroll_a_widget(widget):
        bind_mousewheel_recursive(widget)

    # Variables para los logos de cada sección
    logos = {
        'ventanas': {'archivo': None, 'preview': None, 'info': tk.StringVar()},
        'reportes': {'archivo': None, 'preview': None, 'info': tk.StringVar()},
        'facturas': {'archivo': None, 'preview': None, 'info': tk.StringVar()}
    }
    
    # Variable para aplicar a todas las secciones
    aplicar_a_todas = tk.BooleanVar(value=False)
    
    # Función para obtener información de logo desde BD y archivos
    def obtener_info_logo(seccion, archivo_path):
        try:
            config_bd = consultar_logo_config(seccion)
            if config_bd and os.path.exists(archivo_path):
                fecha = config_bd['fecha_aplicado'][:10]  # Solo fecha, sin hora
                return f"{config_bd['archivo_original']} - Aplicado {fecha}"
            elif os.path.exists(archivo_path):
                return f"{os.path.basename(archivo_path)} - Logo actual"
            else:
                return 'Sin logo configurado'
        except Exception:
            return 'Sin logo configurado' if not os.path.exists(archivo_path) else f"{os.path.basename(archivo_path)} - Logo actual"
    
    # Obtener logos actuales si existen
    logos['ventanas']['info'].set(obtener_info_logo('ventanas', 'Img/SM2.ico'))
    logos['reportes']['info'].set(obtener_info_logo('reportes', 'Img/logo_reportes.png'))
    logos['facturas']['info'].set(obtener_info_logo('facturas', 'Img/logo_facturas.png'))

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
        
        # Aplicar scroll a todos los widgets de esta sección
        aplicar_scroll_a_widget(seccion_frame)
        
        return seccion_frame

    # Crear las tres secciones de logos
    crear_seccion_logo(frame_centrado, "Icono de Ventanas", "🖥️", "ventanas", 1)
    crear_seccion_logo(frame_centrado, "Reportes PDF", "📊", "reportes", 2)
    crear_seccion_logo(frame_centrado, "Facturas y Documentos", "🧾", "facturas", 3)

    # ==================== SECCIÓN DE CONFIGURACIÓN DE TÍTULOS ====================
    
    # Sección de títulos (centrada)
    titulos_frame = tk.LabelFrame(frame_centrado, text="📝 Configuración de Títulos", 
                                 font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                 relief='groove', bd=2)
    titulos_frame.grid(row=4, column=1, sticky='ew', pady=(0, 15), padx=10)
    titulos_frame.columnconfigure(1, weight=1)

    # Variables para los títulos
    titulo_sistema = tk.StringVar()
    titulo_reporte = tk.StringVar()
    titulo_ventana = tk.StringVar()
    
    # Cargar títulos actuales desde BD
    def cargar_titulos_actuales():
        try:
            titulos_config = consultar_titulo_config()
            titulo_sistema.set(titulos_config.get('sistema', 'Sistema de Manejo de Ventas'))
            titulo_reporte.set(titulos_config.get('reporte', 'Reporte de Ventas'))
            titulo_ventana.set(titulos_config.get('ventana', 'Sistema de Gestión'))
        except Exception as e:
            print(f"Error al cargar títulos: {e}")
            titulo_sistema.set("Sistema de Manejo de Ventas")
            titulo_reporte.set("Reporte de Ventas")
            titulo_ventana.set("Sistema de Gestión")
    
    cargar_titulos_actuales()
    
    # Campo: Título del Sistema
    tk.Label(titulos_frame, text="🏢 Título del Sistema:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=0, column=0, sticky='w', padx=15, pady=(15, 5))
    
    entry_sistema = tk.Entry(titulos_frame, textvariable=titulo_sistema, font=("Arial", 10), 
                            width=40, relief='solid', bd=1)
    entry_sistema.grid(row=0, column=1, sticky='ew', padx=15, pady=(15, 5))
    
    tk.Label(titulos_frame, text="Se mostrará como título principal de la aplicación", 
             font=("Arial", 8), bg='#f8f9fa', fg='#7f8c8d').grid(row=1, column=1, sticky='w', padx=15, pady=(0, 10))
    
    # Campo: Título de Reportes
    tk.Label(titulos_frame, text="📊 Título de Reportes:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=2, column=0, sticky='w', padx=15, pady=(5, 5))
    
    entry_reporte = tk.Entry(titulos_frame, textvariable=titulo_reporte, font=("Arial", 10), 
                            width=40, relief='solid', bd=1)
    entry_reporte.grid(row=2, column=1, sticky='ew', padx=15, pady=(5, 5))
    
    tk.Label(titulos_frame, text="Se mostrará en PDFs de reportes y documentos", 
             font=("Arial", 8), bg='#f8f9fa', fg='#7f8c8d').grid(row=3, column=1, sticky='w', padx=15, pady=(0, 10))
    
    # Campo: Título de Ventana
    tk.Label(titulos_frame, text="🖥️ Título de Ventana:", font=("Arial", 10, "bold"), 
             bg='#f8f9fa', fg='#2c3e50').grid(row=4, column=0, sticky='w', padx=15, pady=(5, 5))
    
    entry_ventana = tk.Entry(titulos_frame, textvariable=titulo_ventana, font=("Arial", 10), 
                            width=40, relief='solid', bd=1)
    entry_ventana.grid(row=4, column=1, sticky='ew', padx=15, pady=(5, 5))
    
    tk.Label(titulos_frame, text="Se mostrará en la barra de título de las ventanas", 
             font=("Arial", 8), bg='#f8f9fa', fg='#7f8c8d').grid(row=5, column=1, sticky='w', padx=15, pady=(0, 10))

    # Función para guardar solo los títulos
    def guardar_titulos():
        """Guardar únicamente los títulos en la base de datos"""
        try:
            # Obtener valores sin valores por defecto
            sistema = titulo_sistema.get().strip()
            reporte = titulo_reporte.get().strip()
            ventana = titulo_ventana.get().strip()
            
            # Verificar que al menos uno tenga contenido
            if not any([sistema, reporte, ventana]):
                messagebox.showwarning("Campos vacíos", "Debe completar al menos un campo de título antes de guardar.")
                return
            
            # Guardar solo los valores que no estén vacíos
            resultado = guardar_titulo_config(sistema, reporte, ventana)
            
            if resultado:
                messagebox.showinfo("Éxito", "Títulos guardados correctamente.\n\nLos cambios se verán al reiniciar la aplicación.")
            else:
                messagebox.showwarning("Sin cambios", "No se guardaron títulos porque todos los campos estaban vacíos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar títulos:\n{str(e)}")
    
    # Botón para guardar títulos (dentro de la sección de títulos)
    btn_guardar_titulos = tk.Button(titulos_frame, text="💾 Guardar Títulos", command=guardar_titulos,
                                   bg='#2ecc71', fg='white', font=("Arial", 9, "bold"),
                                   relief='raised', bd=1, cursor='hand2', padx=15)
    btn_guardar_titulos.grid(row=6, column=1, sticky='w', padx=15, pady=(10, 15))

    # Aplicar scroll a la sección de títulos
    aplicar_scroll_a_widget(titulos_frame)

    # Sección de opciones globales (centrada)
    opciones_frame = tk.LabelFrame(frame_centrado, text="⚙️ Opciones Globales", 
                                  font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                  relief='groove', bd=2)
    opciones_frame.grid(row=5, column=1, sticky='ew', pady=(0, 15), padx=10)

    # Checkbox para aplicar a todas las secciones
    tk.Checkbutton(opciones_frame, text="✅ Aplicar logo seleccionado a todas las secciones", 
                   variable=aplicar_a_todas, font=("Arial", 10, "bold"), 
                   bg='#f8f9fa', fg='#2c3e50').pack(anchor='w', padx=15, pady=15)
    
    # Información sobre la opción
    info_global = tk.Label(opciones_frame, 
                          text="Cuando esta opción esté activada, al seleccionar un logo en cualquier sección\nse aplicará automáticamente a todas las demás secciones.", 
                          font=("Arial", 9), bg='#f8f9fa', fg='#7f8c8d', justify='left')
    info_global.pack(anchor='w', padx=15, pady=(0, 15))

    # Aplicar scroll a la sección de opciones globales
    aplicar_scroll_a_widget(opciones_frame)

    # Botones de acción (centrados)
    botones_frame = tk.Frame(frame_centrado, bg='#f8f9fa')
    botones_frame.grid(row=6, column=1, pady=15)

    def aplicar_logos():
        """Aplicar los logos de cada sección y guardar títulos"""
        aplicados = []
        errores = []
        
        # Guardar títulos en BD solo si tienen contenido
        try:
            sistema = titulo_sistema.get().strip()
            reporte = titulo_reporte.get().strip()
            ventana = titulo_ventana.get().strip()
            
            if any([sistema, reporte, ventana]):
                resultado = guardar_titulo_config(sistema, reporte, ventana)
                if resultado:
                    print("✅ Títulos guardados correctamente en BD")
                else:
                    print("⚠️ No se guardaron títulos: campos vacíos")
            else:
                print("ℹ️ Títulos omitidos: todos los campos están vacíos")
        except Exception as e:
            print(f"❌ Error al guardar títulos: {e}")
        
        try:
            # Crear directorios necesarios si no existen
            backup_dir = "Img/backup"
            logos_dir = "Logos"
            os.makedirs(backup_dir, exist_ok=True)
            os.makedirs(logos_dir, exist_ok=True)
            
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
                        archivo_original = os.path.basename(logos[seccion]['archivo'])
                        
                        # 1. Guardar imagen original en carpeta Logos con timestamp para evitar sobreescritura
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        nombre_base, extension = os.path.splitext(archivo_original)
                        nombre_con_timestamp = f"{nombre_base}_{timestamp}_{seccion}{extension}"
                        ruta_logos_original = os.path.join(logos_dir, nombre_con_timestamp)
                        
                        # Copiar imagen original a carpeta Logos
                        shutil.copy2(logos[seccion]['archivo'], ruta_logos_original)
                        
                        # 2. Procesar imagen para su uso específico
                        img_procesada = img.copy()
                        img_procesada = img_procesada.resize(config['tamaño'], Image.Resampling.LANCZOS)
                        
                        # 3. Guardar en el formato correspondiente en Img/
                        if config['formato'] == 'ICO':
                            img_procesada.save(config['destino'], format='ICO')
                        else:
                            img_procesada.save(config['destino'], format='PNG')
                        
                        # 4. Guardar información en base de datos
                        try:
                            size_kb_original = os.path.getsize(ruta_logos_original) / 1024
                            dimensiones_originales = f"{img.size[0]}x{img.size[1]}"
                            
                            guardar_logo_config(
                                seccion=seccion,
                                archivo_path=ruta_logos_original,  # Ruta de la imagen original en Logos/
                                archivo_original=archivo_original,
                                tamaño_kb=size_kb_original,
                                dimensiones=dimensiones_originales,
                                aplicado_por="Usuario"
                            )
                        except Exception as db_error:
                            print(f"Error al guardar en BD para {seccion}: {db_error}")
                        
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
    
    def restablecer_titulos():
        """Restablecer títulos a valores por defecto"""
        resultado = messagebox.askyesno("Confirmar", "¿Restablecer todos los títulos a valores por defecto?")
        if resultado:
            titulo_sistema.set("Sistema de Manejo de Ventas")
            titulo_reporte.set("Reporte de Ventas")
            titulo_ventana.set("Sistema de Gestión")
            messagebox.showinfo("Listo", "Títulos restablecidos a valores por defecto.")

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
    
    def mostrar_historial():
        """Mostrar historial de cambios de logos"""
        try:
            historial = obtener_historial_logos(limit=20)
            if not historial:
                messagebox.showinfo("Historial", "No hay historial de cambios de logos disponible.")
                return
            
            # Crear ventana de historial
            historial_window = tk.Toplevel(parent_frame.winfo_toplevel())
            historial_window.title("📊 Historial de Logos")
            historial_window.geometry("600x400")
            historial_window.configure(bg='#f8f9fa')
            
            # Frame principal
            main_hist_frame = tk.Frame(historial_window, bg='#f8f9fa')
            main_hist_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_hist_frame, text="📊 Historial de Cambios de Logos", 
                    font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(pady=(0, 20))
            
            # Frame con scrollbar
            canvas = tk.Canvas(main_hist_frame, bg='#ffffff')
            scrollbar = tk.Scrollbar(main_hist_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ffffff')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Mostrar historial
            for i, cambio in enumerate(historial):
                cambio_frame = tk.Frame(scrollable_frame, bg='#ffffff', relief='solid', bd=1)
                cambio_frame.pack(fill='x', padx=10, pady=5)
                
                # Información del cambio
                seccion_emoji = {'ventanas': '🖥️', 'reportes': '📊', 'facturas': '🧾'}
                emoji = seccion_emoji.get(cambio['seccion'], '📄')
                
                tk.Label(cambio_frame, text=f"{emoji} {cambio['seccion'].title()}", 
                        font=("Arial", 10, "bold"), bg='#ffffff', fg='#2c3e50').pack(anchor='w', padx=10, pady=(5, 0))
                
                tk.Label(cambio_frame, text=f"Archivo: {cambio['archivo_original']}", 
                        font=("Arial", 9), bg='#ffffff', fg='#34495e').pack(anchor='w', padx=10)
                
                info_text = f"Fecha: {cambio['fecha_aplicado'][:16]} | Por: {cambio['aplicado_por']}"
                if cambio['dimensiones'] and cambio['tamaño_kb']:
                    info_text += f" | {cambio['dimensiones']} | {cambio['tamaño_kb']:.1f} KB"
                
                tk.Label(cambio_frame, text=info_text, 
                        font=("Arial", 8), bg='#ffffff', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 5))
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar historial:\n{str(e)}")
    
    # Botón historial
    btn_historial = tk.Button(botones_frame, text="📊 Historial", command=mostrar_historial,
                             bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                             relief='raised', bd=2, cursor='hand2', padx=15)
    btn_historial.pack(side="left", padx=5)
    
    def mostrar_galeria_logos():
        """Mostrar galería de todas las imágenes guardadas en carpeta Logos"""
        try:
            from Controller.SQL.db_operations import listar_imagenes_logos
            imagenes = listar_imagenes_logos()
            
            if not imagenes:
                messagebox.showinfo("Galería", "No hay imágenes guardadas en la carpeta Logos.")
                return
            
            # Crear ventana de galería
            galeria_window = tk.Toplevel(parent_frame.winfo_toplevel())
            galeria_window.title("🖼️ Galería de Logos")
            galeria_window.geometry("800x600")
            galeria_window.configure(bg='#f8f9fa')
            
            # Frame principal
            main_gal_frame = tk.Frame(galeria_window, bg='#f8f9fa')
            main_gal_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Título
            tk.Label(main_gal_frame, text="🖼️ Galería de Logos Guardados", 
                    font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(pady=(0, 20))
            
            # Frame con scrollbar para la galería
            canvas = tk.Canvas(main_gal_frame, bg='#ffffff')
            scrollbar = tk.Scrollbar(main_gal_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ffffff')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Mostrar imágenes en grid
            row, col = 0, 0
            max_cols = 3
            
            for i, imagen in enumerate(imagenes):
                try:
                    # Frame para cada imagen
                    img_frame = tk.Frame(scrollable_frame, bg='#ffffff', relief='solid', bd=1)
                    img_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                    
                    # Cargar y mostrar imagen
                    img_pil = Image.open(imagen['ruta'])
                    img_pil.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_pil)
                    
                    img_label = tk.Label(img_frame, image=photo, bg='#ffffff')
                    img_label.image = photo  # Mantener referencia
                    img_label.pack(pady=5)
                    
                    # Información de la imagen
                    tk.Label(img_frame, text=imagen['nombre'][:20] + ("..." if len(imagen['nombre']) > 20 else ""), 
                            font=("Arial", 9, "bold"), bg='#ffffff', fg='#2c3e50').pack()
                    
                    tk.Label(img_frame, text=f"{imagen['tamaño_kb']:.1f} KB", 
                            font=("Arial", 8), bg='#ffffff', fg='#7f8c8d').pack()
                    
                    # Actualizar posición en grid
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                        
                except Exception as e:
                    print(f"Error al cargar imagen {imagen['nombre']}: {e}")
                    continue
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Información total
            info_frame = tk.Frame(galeria_window, bg='#f8f9fa')
            info_frame.pack(fill='x', padx=20, pady=(0, 20))
            
            tk.Label(info_frame, text=f"Total de imágenes: {len(imagenes)}", 
                    font=("Arial", 10), bg='#f8f9fa', fg='#34495e').pack()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar galería:\n{str(e)}")
    
    # Botón galería
    btn_galeria = tk.Button(botones_frame, text="🖼️ Galería", command=mostrar_galeria_logos,
                           bg='#9b59b6', fg='white', font=("Arial", 10, "bold"),
                           relief='raised', bd=2, cursor='hand2', padx=15)
    btn_galeria.pack(side="left", padx=5)
    
    # Botón restablecer títulos
    btn_reset_titulos = tk.Button(botones_frame, text="📝 Reset Títulos", command=restablecer_titulos,
                                 bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                                 relief='raised', bd=2, cursor='hand2', padx=15)
    btn_reset_titulos.pack(side="left", padx=5)
    
    # Aplicar scroll a todos los botones
    aplicar_scroll_a_widget(botones_frame)
    
    # Aplicar scroll a todo el frame centrado después de que todos los widgets estén creados
    parent_frame.after(100, lambda: bind_mousewheel_recursive(frame_centrado))


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
