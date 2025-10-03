import tkinter as tk
from tkinter import messagebox, ttk
from Controller.SQL.db_operations import consultar_email_config, obtener_email_config, guardar_email_config
from Controller.styles_mac import (es_macos, configurar_estilos_macos, crear_boton_email_macos,
                                 FuentesMac, ColoresMac)

# Función comentada - solo usar para macOS si es necesario
# def configurar_fondo_uniforme(widget, color="#f8f9fa"):
#     """Solo aplicar en macOS si es necesario"""
#     if not es_macos():
#         return
#     # Resto del código solo para macOS...

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
    if es_macos():
        # Para macOS usar optimizaciones específicas
        return crear_boton_email_macos(parent, text, command, tipo_boton, **kwargs)
    else:
        # Para Windows/Linux usar colores originales
        colores_tipo = {
            "guardar": {"bg": "#27ae60", "fg": "white", "active_bg": "#229954"},
            "cancelar": {"bg": "#95a5a6", "fg": "white", "active_bg": "#7f8c8d"},
            "volver": {"bg": "#2980b9", "fg": "white", "active_bg": "#1f618d"}
        }
        
        color_config = colores_tipo.get(tipo_boton, colores_tipo["guardar"])
        
        return tk.Button(parent, text=text, command=command,
                        bg=color_config["bg"], fg=color_config["fg"],
                        activebackground=color_config["active_bg"], 
                        activeforeground="white",
                        font=("Arial", 10, "bold"), relief="raised", bd=2,
                        cursor="hand2", **kwargs)

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
    popup.configure(bg="#ecf0f1")
    
    # Configurar ícono
    try:
        popup.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Frame principal con estilo profesional
    main_frame = tk.Frame(popup, bg="#ffffff", relief="solid", bd=2)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Título principal
    fuente_titulo = FuentesMac.SECUNDARIA if es_macos() else ("Arial", 14, "bold")
    titulo = tk.Label(main_frame, text="📧 Configuración de Email", 
                     font=fuente_titulo, bg="#ffffff", fg="#2c3e50")
    titulo.pack(pady=(15, 20))
    
    # Obtener configuración existente
    email_registrado = consultar_email_config()
    _, pass_registrada = obtener_email_config()
    
    # Cargar imágenes al principio
    try:
        img_comunicacion = tk.PhotoImage(file="Img/comunicacion.png")
        img_comunicacion = img_comunicacion.subsample(2, 2)
    except Exception:
        img_comunicacion = None
        
    try:
        img_candado = tk.PhotoImage(file="Img/candado.png")
        img_candado = img_candado.subsample(2, 2)
    except Exception:
        img_candado = None
    
    # Campo de email con imagen de comunicación
    fuente_label = FuentesMac.BOTON_PEQUEÑO if es_macos() else ("Arial", 10, "bold")
    
    if img_comunicacion:
        lbl_email_popup = tk.Label(main_frame, text=" Correo remitente:", 
                                  font=fuente_label, bg="#ffffff", fg="#34495e",
                                  compound=tk.LEFT, image=img_comunicacion)
        lbl_email_popup.image = img_comunicacion
        lbl_email_popup.pack(pady=(0, 5))
    else:
        tk.Label(main_frame, text="📬 Correo remitente:", 
                font=fuente_label, bg="#ffffff", fg="#34495e").pack(pady=(0, 5))
    entry_email = tk.Entry(main_frame, width=40, font=("Arial", 10), relief="solid", bd=1)
    if email_registrado:
        entry_email.insert(0, email_registrado)
    entry_email.pack(pady=(0, 15), padx=20)
    
    # Campo de contraseña con imagen de candado
    if img_candado:
        lbl_password_popup = tk.Label(main_frame, text=" Contraseña:", 
                                     font=fuente_label, bg="#ffffff", fg="#34495e",
                                     compound=tk.LEFT, image=img_candado)
        lbl_password_popup.image = img_candado
        lbl_password_popup.pack(pady=(0, 5))
    else:
        tk.Label(main_frame, text="🔐 Contraseña:", 
                font=fuente_label, bg="#ffffff", fg="#34495e").pack(pady=(0, 5))
    
    # Frame para contraseña con botón de ojo
    frame_pass = tk.Frame(main_frame, bg="#ffffff")
    frame_pass.pack(pady=(0, 20), padx=20)
    
    entry_pass = tk.Entry(frame_pass, width=32, show="*", font=("Arial", 10), relief="solid", bd=1)
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
    
    # Botón de ojo con colores originales
    btn_ojo = tk.Button(frame_pass, text="👁️", width=3, height=1, command=toggle_password, 
                       relief="raised", bd=1, bg="#ecf0f1", fg="#2c3e50", 
                       font=("Arial", 12, "bold"), cursor="hand2",
                       activebackground="#bdc3c7", activeforeground="#2c3e50")
    btn_ojo.bind("<Enter>", on_enter_ojo)
    btn_ojo.bind("<Leave>", on_leave_ojo)
    btn_ojo.pack(side="left", padx=(5, 0), pady=2)
    
    # Cargar imagen del disquete para el botón guardar
    try:
        img_disquete = tk.PhotoImage(file="Img/disquete.png")
        img_disquete = img_disquete.subsample(3, 3)
    except Exception:
        img_disquete = None
    
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
    
    # Botones de acción
    frame_botones = tk.Frame(main_frame, bg="#ffffff")
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
    
    # Frame principal para la configuración
    main_frame = tk.Frame(parent_frame, bg="#ecf0f1")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título y botón volver
    header_frame = tk.Frame(main_frame, bg="#ecf0f1")
    header_frame.pack(fill="x", pady=(0, 30))
    
    btn_volver = crear_boton_email_optimizado(header_frame, "← Volver", 
                                             callback_volver, "volver",
                                             padx=15, pady=5)
    btn_volver.pack(side="left")
    
    fuente_titulo_grande = FuentesMac.PRINCIPAL if es_macos() else ("Arial", 16, "bold")
    titulo = tk.Label(header_frame, text="⚙️ CONFIGURACIÓN DE EMAIL", 
                     font=fuente_titulo_grande, fg="#2c3e50", bg="#ecf0f1")
    titulo.pack(side="right")
    
    # Frame de configuración con estilo profesional
    config_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=2)
    config_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Obtener configuración existente
    email_registrado = consultar_email_config()
    _, pass_registrada = obtener_email_config()
    
    # Información actual
    info_frame = tk.Frame(config_frame, bg="#ffffff")
    info_frame.pack(fill="x", pady=20, padx=20)
    
    fuente_label_bold = FuentesMac.BOTON_NORMAL if es_macos() else ("Arial", 12, "bold")
    fuente_label_normal = FuentesMac.TEXTO_NORMAL if es_macos() else ("Arial", 10)
    
    tk.Label(info_frame, text="📋 Configuración Actual:", 
            font=fuente_label_bold, bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    
    email_actual = email_registrado if email_registrado else "No configurado"
    pass_actual = "••••••••" if pass_registrada else "No configurada"
    
    tk.Label(info_frame, text=f"📧 Email: {email_actual}", 
            font=fuente_label_normal, bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(5, 0))
    tk.Label(info_frame, text=f"🔐 Contraseña: {pass_actual}", 
            font=fuente_label_normal, bg="#ffffff", fg="#34495e").pack(anchor="w")
    
    # Separador - fondo blanco consistente
    separator = tk.Frame(config_frame, height=2, bg="#bdc3c7")
    separator.pack(fill="x", padx=20, pady=10)
    
    # Formulario de configuración
    form_frame = tk.Frame(config_frame, bg="#ffffff")
    form_frame.pack(fill="x", pady=20, padx=20)
    
    # Label de correo con imagen de comunicación
    form_font = FuentesMac.BOTON_NORMAL if es_macos() else ("Arial", 11, "bold")
    
    if img_comunicacion_frame:
        lbl_email_frame = tk.Label(form_frame, text=" Nuevo correo remitente:", 
                                  font=form_font, bg="#ffffff", fg="#34495e",
                                  compound=tk.LEFT, image=img_comunicacion_frame)
        lbl_email_frame.image = img_comunicacion_frame
        lbl_email_frame.pack(anchor="w", pady=(0, 5))
    else:
        tk.Label(form_frame, text="📬 Nuevo correo remitente:", 
                font=form_font, bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(0, 5))
    entry_email = tk.Entry(form_frame, width=50, font=("Arial", 10), relief="solid", bd=1)
    if email_registrado:
        entry_email.insert(0, email_registrado)
    entry_email.pack(pady=(0, 15), anchor="w")
    
    # Label de contraseña con imagen de candado
    if img_candado_frame:
        lbl_password = tk.Label(form_frame, text=" Nueva contraseña:", 
                               font=form_font, bg="#ffffff", fg="#34495e",
                               compound=tk.LEFT, image=img_candado_frame)
        lbl_password.image = img_candado_frame
        lbl_password.pack(anchor="w", pady=(0, 5))
    else:
        tk.Label(form_frame, text="🔐 Nueva contraseña:", 
                font=form_font, bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(0, 5))
    
    pass_frame = tk.Frame(form_frame, bg="#ffffff")
    pass_frame.pack(anchor="w", pady=(0, 20))
    
    entry_pass = tk.Entry(pass_frame, width=42, show="*", font=("Arial", 10), relief="solid", bd=1)
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
    
    # Botón de ojo en frame con colores originales
    btn_ojo = tk.Button(pass_frame, text="👁️", width=4, height=1, command=toggle_password, 
                       relief="raised", bd=1, bg="#ecf0f1", fg="#2c3e50", 
                       font=("Arial", 12, "bold"), cursor="hand2",
                       activebackground="#bdc3c7", activeforeground="#2c3e50")
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
    
    # Frame para el botón guardar
    button_frame = tk.Frame(form_frame, bg="#ffffff")
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
    

