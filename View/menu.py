# menu.py

def menubar(root):
    import tkinter as tk
    from View.ReportView import mostrar_historial_ventas
    from View.ReportSales import mostrar_reporte_ventas
    menubar = tk.Menu(root)
    # Menú principal
    menu_archivo = tk.Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Historial de ventas", command=lambda: mostrar_historial_ventas(root))
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Reporte de ventas", command=lambda: mostrar_reporte_ventas(root))
    menubar.add_cascade(label="Historial", menu=menu_archivo)

    # Menú de configuraciones
    def abrir_config_email():
        popup = tk.Toplevel(root)
        popup.title("Configuración de Email")
        popup.geometry("350x200")
        popup.resizable(False, False)
        try:
            popup.iconbitmap('Img/SM2.ico')
        except Exception:
            pass
        tk.Label(popup, text="Correo remitente:").pack(pady=(15, 0))
        from Controller.db_operations import consultar_email_config, obtener_email_config
        email_registrado = consultar_email_config()
        _, pass_registrada = obtener_email_config()
        entry_email = tk.Entry(popup, width=35)
        if email_registrado:
            entry_email.insert(0, email_registrado)
        entry_email.pack(pady=5)
        tk.Label(popup, text="Contraseña:").pack(pady=(10, 0))
        frame_pass = tk.Frame(popup)
        entry_pass = tk.Entry(frame_pass, width=27, show="*")
        if pass_registrada:
            entry_pass.insert(0, pass_registrada)
        entry_pass.pack(side="left", pady=5, padx=(0, 5))
        password_visible = [False]
        def toggle_password():
            password_visible[0] = not password_visible[0]
            if password_visible[0]:
                entry_pass.config(show="")
                btn_ojo.config(text="👁")
            else:
                entry_pass.config(show="*")
                btn_ojo.config(text="👁")
        btn_ojo = tk.Button(frame_pass, text="👁", width=2, command=toggle_password, relief="flat", bd=0)
        btn_ojo.pack(side="left")
        frame_pass.pack(pady=5)
        def guardar():
            from tkinter import messagebox
            from Controller.db_operations import guardar_email_config
            email = entry_email.get().strip()
            password = entry_pass.get().strip()
            if not email or not password:
                messagebox.showwarning("Campos requeridos", "Debes ingresar correo y contraseña.", parent=popup)
                return
            guardar_email_config(email, password)
            messagebox.showinfo("Configuración guardada", "Correo y contraseña guardados correctamente.", parent=popup)
            popup.destroy()
        btn_guardar = tk.Button(popup, text="Guardar", command=guardar)
        btn_guardar.pack(pady=15)
        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup)

    menu_config = tk.Menu(menubar, tearoff=0)
    menu_config.add_command(label="Email", command=abrir_config_email)
    menubar.add_cascade(label="Configuraciones", menu=menu_config)
    return menubar