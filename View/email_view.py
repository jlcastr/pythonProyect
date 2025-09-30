import tkinter as tk
from tkinter import messagebox, ttk
from Controller.db_operations import consultar_email_config, obtener_email_config, guardar_email_config
from Controller.styles_mac import (es_macos, configurar_estilos_macos, crear_boton_email_macos,
                                 FuentesMac, ColoresMac)

def configurar_fondo_uniforme(widget, color="#f8f9fa"):
    """
    Configura el fondo de un widget y todos sus hijos de manera recursiva
    Elimina cualquier fondo negro o problemático
    
    Args:
        widget: Widget a configurar
        color: Color de fondo (por defecto blanco)
    """
    try:
        # Configurar el widget principal
        widget.configure(bg=color)
        
        # Si es un Toplevel, configurar también highlightcolor y bd
        if hasattr(widget, 'wm_title'):  # Es una ventana
            widget.configure(highlightcolor=color, highlightbackground=color)
            
    except:
        pass
    
    # Configurar todos los widgets hijos recursivamente
    for child in widget.winfo_children():
        try:
            # Solo configurar Frame, Label y widgets que no sean Entry o Button
            widget_class = child.winfo_class()
            if widget_class in ['Frame', 'Label', 'Toplevel', 'Canvas']:
                child.configure(bg=color)
            elif widget_class == 'Entry':
                # Configuración específica para Entry - fondo blanco, texto negro
                child.configure(bg="white", fg="black", insertbackground="black")
                
            # Llamada recursiva para hijos del hijo
            configurar_fondo_uniforme(child, color)
        except:
            pass

def crear_boton_email_optimizado(parent, text, command, tipo_boton="guardar", **kwargs):
    """
    Crear botones optimizados para email - detecta macOS automáticamente
    
    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        tipo_boton: Tipo de botón ("guardar", "cancelar", "volver")
        **kwargs: Argumentos adicionales
    
    Returns:
        Widget de botón optimizado para la plataforma
    """
    # Colores uniformes para todas las plataformas - optimizados para fondo blanco
    colores_tipo = {
        "guardar": {"bg": "#27ae60", "fg": "white", "active_bg": "#229954"},
        "cancelar": {"bg": "#95a5a6", "fg": "white", "active_bg": "#7f8c8d"},
        "volver": {"bg": "#2980b9", "fg": "white", "active_bg": "#1f618d"}  # Azul más oscuro y visible
    }
    
    color_config = colores_tipo.get(tipo_boton, colores_tipo["guardar"])
    fuente = FuentesMac.BOTON_NORMAL if es_macos() else ("Arial", 10, "bold")
    
    return tk.Button(parent, text=text, command=command,
                    bg=color_config["bg"], fg=color_config["fg"],
                    activebackground=color_config["active_bg"], 
                    activeforeground="white",
                    font=fuente, relief="flat",
                    borderwidth=0, cursor="hand2", 
                    highlightthickness=0,  # Sin recuadros problemáticos
                    **kwargs)

def abrir_config_email(parent_window=None):
    """
    Abre el popup de configuración de email
    
    Args:
        parent_window: Ventana padre (opcional)
    """
    popup = tk.Toplevel(parent_window) if parent_window else tk.Toplevel()
    popup.title("⚙️ Configuración de Email")
    popup.geometry("380x250")
    popup.resizable(False, False)
    popup.configure(bg="#f8f9fa")  # Fondo blanco para la ventana popup
    
    # Configurar ícono
    try:
        popup.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Frame principal con estilo - fondo blanco consistente
    frame_bg = "#f8f9fa"  # Fondo blanco consistente con otras pantallas
    main_frame = tk.Frame(popup, bg=frame_bg, relief="solid", bd=1)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título principal con fuente optimizada - colores consistentes
    fuente_titulo = FuentesMac.SECUNDARIA if es_macos() else ("Arial", 14, "bold")
    titulo = tk.Label(main_frame, text="📧 Configuración de Email", 
                     font=fuente_titulo, bg=frame_bg, fg="#2c3e50")
    titulo.pack(pady=(15, 20))
    
    # Obtener configuración existente
    email_registrado = consultar_email_config()
    _, pass_registrada = obtener_email_config()
    
    # Campo de email con imagen de comunicación - colores consistentes
    fuente_label = FuentesMac.BOTON_PEQUEÑO if es_macos() else ("Arial", 10, "bold")
    
    if img_comunicacion:
        lbl_email_popup = tk.Label(main_frame, text=" Correo remitente:", 
                                  font=fuente_label, bg=frame_bg, fg="#34495e",
                                  compound=tk.LEFT, image=img_comunicacion)
        lbl_email_popup.image = img_comunicacion
        lbl_email_popup.pack(pady=(0, 5))
    else:
        tk.Label(main_frame, text="📬 Correo remitente:", 
                font=fuente_label, bg=frame_bg, fg="#34495e").pack(pady=(0, 5))
    entry_email = tk.Entry(main_frame, width=40, font=("Arial", 10), relief="solid", bd=1,
                          bg="white", fg="black", insertbackground="black")  # Fondo blanco, texto negro
    if email_registrado:
        entry_email.insert(0, email_registrado)
    entry_email.pack(pady=(0, 15), padx=20)
    
    # Campo de contraseña con imagen de candado - colores consistentes
    if img_candado:
        lbl_password_popup = tk.Label(main_frame, text=" Contraseña:", 
                                     font=fuente_label, bg=frame_bg, fg="#34495e",
                                     compound=tk.LEFT, image=img_candado)
        lbl_password_popup.image = img_candado
        lbl_password_popup.pack(pady=(0, 5))
    else:
        tk.Label(main_frame, text="🔐 Contraseña:", 
                font=fuente_label, bg=frame_bg, fg="#34495e").pack(pady=(0, 5))
    
    # Frame para contraseña con botón de ojo - fondo blanco consistente
    frame_pass = tk.Frame(main_frame, bg=frame_bg)
    frame_pass.pack(pady=(0, 20), padx=20)
    
    entry_pass = tk.Entry(frame_pass, width=32, show="*", font=("Arial", 10), relief="solid", bd=1,
                         bg="white", fg="black", insertbackground="black")  # Fondo blanco, texto negro
    if pass_registrada:
        entry_pass.insert(0, pass_registrada)
    entry_pass.pack(side="left", padx=(0, 5))
    
    # Variable para controlar visibilidad de contraseña
    password_visible = [False]
    
    def toggle_password():
        """Alternar visibilidad de la contraseña"""
        password_visible[0] = not password_visible[0]
        if password_visible[0]:
            entry_pass.config(show="")
            btn_ojo.config(text="🙈")
        else:
            entry_pass.config(show="*")
            btn_ojo.config(text="👁️")
    
    def on_enter_ojo(e):
        """Efecto hover al entrar"""
        btn_ojo.config(relief="sunken")
    
    def on_leave_ojo(e):
        """Efecto hover al salir"""
        btn_ojo.config(relief="flat")
    
    # Botón de ojo con fondo blanco consistente
    btn_ojo = tk.Button(frame_pass, text="👁️", width=3, height=1, command=toggle_password, 
                       relief="flat", bd=0, bg=frame_bg, fg="black", 
                       font=("Arial", 12, "bold"), cursor="hand2",
                       activebackground=frame_bg, activeforeground="black",
                       highlightthickness=0)  # Sin recuadros
    btn_ojo.bind("<Enter>", on_enter_ojo)
    btn_ojo.bind("<Leave>", on_leave_ojo)
    btn_ojo.pack(side="left", padx=(5, 0), pady=2)
    
    # Cargar imagen del disquete para el botón guardar
    try:
        img_disquete = tk.PhotoImage(file="Img/disquete.png")
        img_disquete = img_disquete.subsample(3, 3)  # Redimensionar para el botón (aún más grande)
    except Exception:
        img_disquete = None
    
    # Cargar imagen del candado para el label de contraseña
    try:
        img_candado = tk.PhotoImage(file="Img/candado.png")
        img_candado = img_candado.subsample(2, 2)  # Medida 2
    except Exception:
        img_candado = None
    
    # Cargar imagen de comunicación para el label de correo
    try:
        img_comunicacion = tk.PhotoImage(file="Img/comunicacion.png")
        img_comunicacion = img_comunicacion.subsample(2, 2)  # Medida 2
    except Exception:
        img_comunicacion = None
    
    # Función para guardar configuración
    def guardar():
        """Guardar la configuración de email"""
        email = entry_email.get().strip()
        password = entry_pass.get().strip()
        
        # Validaciones
        if not email or not password:
            messagebox.showwarning("⚠️ Campos requeridos", 
                                 "Debes ingresar correo y contraseña.", 
                                 parent=popup)
            return
        
        # Validar formato de email básico
        if "@" not in email or "." not in email:
            messagebox.showwarning("⚠️ Email inválido", 
                                 "Ingresa un email con formato válido.", 
                                 parent=popup)
            return
        
        try:
            # Guardar configuración
            guardar_email_config(email, password)
            messagebox.showinfo("✅ Configuración guardada", 
                              "Correo y contraseña guardados correctamente.\n"
                              "La contraseña se almacena de forma segura.", 
                              parent=popup)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("❌ Error", 
                               f"Error al guardar la configuración:\n{str(e)}", 
                               parent=popup)
    
    # Botones de acción - fondo blanco consistente
    frame_botones = tk.Frame(main_frame, bg=frame_bg)
    frame_botones.pack(pady=(10, 15))
    
    btn_cancelar = crear_boton_email_optimizado(frame_botones, "❌ Cancelar", 
                                               popup.destroy, "cancelar", 
                                               padx=15, pady=5)
    btn_cancelar.pack(side="left", padx=(0, 10))
    
    if img_disquete:
        btn_guardar = crear_boton_email_optimizado(frame_botones, "Guardar", 
                                                  guardar, "guardar",
                                                  padx=15, pady=5)
        # Para tk.Button (no macOS), agregar imagen manualmente
        if not es_macos():
            try:
                btn_guardar.config(image=img_disquete, compound=tk.LEFT)
                btn_guardar.image = img_disquete
            except:
                pass
    else:
        btn_guardar = crear_boton_email_optimizado(frame_botones, "Guardar", 
                                                  guardar, "guardar",
                                                  padx=15, pady=5)
    btn_guardar.pack(side="left")
    
    # Configurar comportamiento del popup
    # Aplicar fondo blanco uniforme a todo el popup
    configurar_fondo_uniforme(popup, "#f8f9fa")
    
    if parent_window:
        popup.transient(parent_window)
        popup.grab_set()
        
        # Centrar el popup respecto a la ventana padre
        parent_window.update_idletasks()
        x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - 190
        y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - 125
        popup.geometry(f"380x250+{x}+{y}")
        
        parent_window.wait_window(popup)
    else:
        popup.grab_set()

def mostrar_config_email_en_frame(parent_frame, callback_volver):
    """
    Mostrar configuración de email dentro de un frame existente
    
    Args:
        parent_frame: Frame padre donde mostrar la configuración
        callback_volver: Función a llamar para volver al menú anterior
    """
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Cargar imágenes al principio
    try:
        img_candado_frame = tk.PhotoImage(file="Img/candado.png")
        img_candado_frame = img_candado_frame.subsample(2, 2)  # Medida 2
    except Exception:
        img_candado_frame = None
    
    try:
        img_disquete_frame = tk.PhotoImage(file="Img/disquete.png")
        img_disquete_frame = img_disquete_frame.subsample(3, 3)  # Redimensionar para el botón aún más grande
    except Exception:
        img_disquete_frame = None
    
    # Cargar imagen de comunicación para el label de correo
    try:
        img_comunicacion_frame = tk.PhotoImage(file="Img/comunicacion.png")
        img_comunicacion_frame = img_comunicacion_frame.subsample(2, 2)  # Medida 2
    except Exception:
        img_comunicacion_frame = None
    
    # Configurar fondo blanco uniforme para todo
    configurar_fondo_uniforme(parent_frame, "#f8f9fa")
    
    # Frame principal para la configuración - con fondo blanco
    main_frame = tk.Frame(parent_frame, bg="#f8f9fa")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver - con fondo blanco
    header_frame = tk.Frame(main_frame, bg="#f8f9fa")
    header_frame.pack(fill="x", pady=(0, 30))
    
    btn_volver = crear_boton_email_optimizado(header_frame, "← Volver", 
                                             callback_volver, "volver",
                                             padx=20, pady=8)  # Más padding para mejor visibilidad
    btn_volver.pack(side="left")
    
    fuente_titulo_grande = FuentesMac.PRINCIPAL if es_macos() else ("Arial", 16, "bold")
    titulo = tk.Label(header_frame, text="⚙️ CONFIGURACIÓN DE EMAIL", 
                     font=fuente_titulo_grande, fg="#2c3e50", bg="#f8f9fa")
    titulo.pack(side="right")
    
    # Frame de configuración con estilo - fondo blanco consistente
    config_bg = "#f8f9fa"  # Fondo blanco consistente con otras pantallas
    config_frame = tk.Frame(main_frame, bg=config_bg, relief="solid", bd=2)
    config_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Obtener configuración existente
    email_registrado = consultar_email_config()
    _, pass_registrada = obtener_email_config()
    
    # Información actual - fondo blanco consistente
    info_frame = tk.Frame(config_frame, bg=config_bg)
    info_frame.pack(fill="x", pady=20, padx=20)
    
    fuente_label_bold = FuentesMac.BOTON_NORMAL if es_macos() else ("Arial", 12, "bold")
    fuente_label_normal = FuentesMac.TEXTO_NORMAL if es_macos() else ("Arial", 10)
    
    tk.Label(info_frame, text="📋 Configuración Actual:", 
            font=fuente_label_bold, bg=config_bg, fg="#2c3e50").pack(anchor="w")
    
    email_actual = email_registrado if email_registrado else "No configurado"
    pass_actual = "••••••••" if pass_registrada else "No configurada"
    
    tk.Label(info_frame, text=f"📧 Email: {email_actual}", 
            font=fuente_label_normal, bg=config_bg, fg="#34495e").pack(anchor="w", pady=(5, 0))
    tk.Label(info_frame, text=f"🔐 Contraseña: {pass_actual}", 
            font=fuente_label_normal, bg=config_bg, fg="#34495e").pack(anchor="w")
    
    # Separador - fondo blanco consistente
    separator = tk.Frame(config_frame, height=2, bg="#bdc3c7")
    separator.pack(fill="x", padx=20, pady=10)
    
    # Formulario de configuración - fondo blanco consistente
    form_frame = tk.Frame(config_frame, bg=config_bg)
    form_frame.pack(fill="x", pady=20, padx=20)
    
    # Label de correo con imagen de comunicación - fondo blanco consistente
    form_font = FuentesMac.BOTON_NORMAL if es_macos() else ("Arial", 11, "bold")
    
    if img_comunicacion_frame:
        lbl_email_frame = tk.Label(form_frame, text=" Nuevo correo remitente:", 
                                  font=form_font, bg=config_bg, fg="#34495e",
                                  compound=tk.LEFT, image=img_comunicacion_frame)
        lbl_email_frame.image = img_comunicacion_frame
        lbl_email_frame.pack(anchor="w", pady=(0, 5))
    else:
        tk.Label(form_frame, text="📬 Nuevo correo remitente:", 
                font=form_font, bg=config_bg, fg="#34495e").pack(anchor="w", pady=(0, 5))
    entry_email = tk.Entry(form_frame, width=50, font=("Arial", 10), relief="solid", bd=1,
                          bg="white", fg="black", insertbackground="black")  # Fondo blanco, texto negro
    if email_registrado:
        entry_email.insert(0, email_registrado)
    entry_email.pack(pady=(0, 15), anchor="w")
    
    # Label de contraseña con imagen de candado - fondo blanco consistente
    if img_candado_frame:
        lbl_password = tk.Label(form_frame, text=" Nueva contraseña:", 
                               font=form_font, bg=config_bg, fg="#34495e",
                               compound=tk.LEFT, image=img_candado_frame)
        lbl_password.image = img_candado_frame
        lbl_password.pack(anchor="w", pady=(0, 5))
    else:
        tk.Label(form_frame, text="🔐 Nueva contraseña:", 
                font=form_font, bg=config_bg, fg="#34495e").pack(anchor="w", pady=(0, 5))
    
    pass_frame = tk.Frame(form_frame, bg=config_bg)
    pass_frame.pack(anchor="w", pady=(0, 20))
    
    entry_pass = tk.Entry(pass_frame, width=42, show="*", font=("Arial", 10), relief="solid", bd=1,
                         bg="white", fg="black", insertbackground="black")  # Fondo blanco, texto negro
    if pass_registrada:
        entry_pass.insert(0, pass_registrada)
    entry_pass.pack(side="left", padx=(0, 10))
    
    password_visible = [False]
    
    def toggle_password():
        password_visible[0] = not password_visible[0]
        if password_visible[0]:
            entry_pass.config(show="")
            btn_ojo.config(text="🙈")
        else:
            entry_pass.config(show="*")
            btn_ojo.config(text="👁️")
    
    def on_enter_ojo_frame(e):
        """Efecto hover al entrar"""
        btn_ojo.config(relief="sunken")
    
    def on_leave_ojo_frame(e):
        """Efecto hover al salir"""
        btn_ojo.config(relief="flat")
    
    # Botón de ojo en frame - fondo blanco consistente
    btn_ojo = tk.Button(pass_frame, text="👁️", width=4, height=1, command=toggle_password, 
                       relief="flat", bd=0, bg=config_bg, fg="black", 
                       font=("Arial", 12, "bold"), cursor="hand2",
                       activebackground=config_bg, activeforeground="black",
                       highlightthickness=0)  # Sin recuadros
    btn_ojo.bind("<Enter>", on_enter_ojo_frame)
    btn_ojo.bind("<Leave>", on_leave_ojo_frame)
    btn_ojo.pack(side="left", padx=(5, 0), pady=3)
    
    def guardar_config():
        email = entry_email.get().strip()
        password = entry_pass.get().strip()
        
        if not email or not password:
            messagebox.showwarning("⚠️ Campos requeridos", 
                                 "Debes ingresar correo y contraseña.")
            return
        
        if "@" not in email or "." not in email:
            messagebox.showwarning("⚠️ Email inválido", 
                                 "Ingresa un email con formato válido.")
            return
        
        try:
            guardar_email_config(email, password)
            messagebox.showinfo("✅ Configuración guardada", 
                              "Correo y contraseña guardados correctamente.\n"
                              "La contraseña se almacena de forma segura.")
            # Actualizar la vista
            mostrar_config_email_en_frame(parent_frame, callback_volver)
        except Exception as e:
            messagebox.showerror("❌ Error", 
                               f"Error al guardar la configuración:\n{str(e)}")
    
    # Frame para el botón guardar - más visible
    button_frame = tk.Frame(form_frame, bg=config_bg)
    button_frame.pack(fill="x", pady=(20, 0))
    
    # Botón guardar con imagen - más prominente
    btn_guardar = crear_boton_email_optimizado(button_frame, "💾 Guardar Configuración", 
                                              guardar_config, "guardar",
                                              padx=25, pady=12)
    
    # Para plataformas no-macOS, agregar imagen si está disponible
    if img_disquete_frame and not es_macos():
        try:
            btn_guardar.config(image=img_disquete_frame, compound=tk.LEFT)
            btn_guardar.image = img_disquete_frame
        except:
            pass
    
    btn_guardar.pack(anchor="w")
    
    # Aplicar fondo blanco uniforme a todos los elementos creados
    configurar_fondo_uniforme(main_frame, "#f8f9fa")
    configurar_fondo_uniforme(parent_frame, "#f8f9fa")
    
    # Forzar actualización visual
    try:
        parent_frame.update_idletasks()
        main_frame.update_idletasks()
    except:
        pass
