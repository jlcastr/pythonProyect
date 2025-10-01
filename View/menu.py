# menu.py

def menubar(root):
    import tkinter as tk
    from View.ReportHistorySales import mostrar_historial_ventas
    from View.ReportSales import mostrar_reporte_ventas
    menubar = tk.Menu(root)
    # Menú principal
    menu_archivo = tk.Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Historial de ventas", command=lambda: mostrar_historial_ventas(root))
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Reporte de ventas", command=lambda: mostrar_reporte_ventas(root))
    menubar.add_cascade(label="Historial", menu=menu_archivo)

    # Menú de configuraciones
    from View.email_view import abrir_config_email
    
    menu_config = tk.Menu(menubar, tearoff=0)
    menu_config.add_command(label="Email", command=lambda: abrir_config_email(root))
    menubar.add_cascade(label="Configuraciones", menu=menu_config)
    return menubar