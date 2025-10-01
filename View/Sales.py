import tkinter as tk
from tkinter import ttk
import platform
import Controller.utils as utils
import Controller.db_operations as db_operations
from Controller.styles import configurar_estilos_aplicacion, Colores, Fuentes, EstilosVentas, EstilosTreeview
from Controller.styles_mac import configurar_estilos_macos, crear_boton_macos, es_macos

def crear_boton_optimizado(parent, text, command, tipo_boton):
    """
    Crear botón optimizado para la plataforma actual
    """
    is_macos = platform.system() == 'Darwin'
    
    if is_macos:
        # En macOS usar los estilos optimizados sin bordes
        from Controller.styles_mac import crear_boton_sales_macos
        return crear_boton_sales_macos(parent, text, command, tipo_boton)
    else:
        # En Windows/Linux usar tk.Button normal
        colores = {
            "agregar": ('#27ae60', 'white'),
            "cancelar": ('#e74c3c', 'white'),
            "eliminar": ('#e74c3c', 'white'),
            "modificar": ('#2980b9', 'white'),
            "limpiar": ('#95a5a6', 'white'),
            "finalizar": ('#27ae60', 'white')
        }
        color_bg, color_fg = colores.get(tipo_boton, ('#27ae60', 'white'))
        
        return tk.Button(parent, text=text, command=command,
                        bg=color_bg, fg=color_fg, font=("Arial", 10, "bold"),
                        relief='raised', bd=2, cursor='hand2')

def crear_pantalla_principal(conn, cursor, menubar):
    import tkinter as tk
    root = tk.Tk()
    try:
        root.iconbitmap('Img/SM2.ico')
    except Exception:
        pass
    
    # Configuración profesional de la ventana
    root.configure(bg='#ecf0f1')
    
    # Configurar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Configurar estilos específicos para macOS si es necesario
    if es_macos():
        configurar_estilos_macos()
    
    # Los estilos de botones ahora se manejan centralizadamente desde styles_mac.py
    
    # Los estilos de Treeview ya están configurados centralizadamente

    venta_actual_id = [None]
    folio_actual = [None]
    root.after(0, lambda: root.title("S&M - Sistema de Manejo de Ventas"))
    root.geometry("950x620")
    root.resizable(False, False)
    from View.menu import menubar as menu_fn
    root.config(menu=menu_fn(root))
    
    # Frame principal con estilo profesional
    main_container = EstilosVentas.crear_frame(root)
    main_container.configure(padx=20, pady=20)
    main_container.pack(fill='both', expand=True)
    
    # Título principal
    titulo_principal = EstilosVentas.crear_label_titulo(main_container, "📊 MÓDULO DE VENTAS")
    titulo_principal.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    # Sección de información de venta
    info_frame = EstilosVentas.crear_labelframe(main_container, "📋 Información de Venta")
    info_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    info_frame.columnconfigure(0, minsize=180)
    info_frame.columnconfigure(1, weight=1)

    # Etiqueta y campo para folio (readonly) con mejor estilo
    label_folio = tk.Label(info_frame, text="Folio de venta:", width=20, anchor="e",
                          font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_folio.grid(row=0, column=0, padx=15, pady=10, sticky="e")
    entry_folio = tk.Entry(info_frame, width=35, state="readonly", 
                          font=("Arial", 10), relief='solid', bd=1,
                          bg='#ffffff', fg='#000000', readonlybackground='#f0f0f0')
    entry_folio.grid(row=0, column=1, padx=15, pady=10, sticky='w')

    # Etiqueta y campo para nombre del cliente
    label_cliente = tk.Label(info_frame, text="Nombre del cliente:", width=20, anchor="e",
                            font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_cliente.grid(row=1, column=0, padx=15, pady=10, sticky="e")
    entry_cliente = tk.Entry(info_frame, width=35, font=("Arial", 10), 
                            relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_cliente.grid(row=1, column=1, padx=15, pady=10, sticky='w')

    # Sección de entrada de productos
    producto_frame = EstilosVentas.crear_labelframe(main_container, "🗺️ Agregar Producto")
    producto_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    producto_frame.columnconfigure(0, minsize=180)
    producto_frame.columnconfigure(1, weight=1)

    # Etiqueta y campo para descripción con mejor estilo
    label_descripcion = tk.Label(producto_frame, text="Descripción del producto:", width=20, anchor="e",
                                font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_descripcion.grid(row=0, column=0, padx=15, pady=8, sticky="e")
    entry_descripcion = tk.Entry(producto_frame, width=35, font=("Arial", 10), 
                               relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_descripcion.grid(row=0, column=1, padx=15, pady=8, sticky='w')

    # Etiqueta y campo para precio con mejor estilo
    label_precio = tk.Label(producto_frame, text="Precio ($):", width=20, anchor="e",
                           font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_precio.grid(row=1, column=0, padx=15, pady=8, sticky="e")
    vcmd = (root.register(lambda texto: utils.validar_decimal(texto)), '%P')
    entry_precio = tk.Entry(producto_frame, width=35, validate="key", validatecommand=vcmd, 
                          font=("Arial", 10), relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_precio.grid(row=1, column=1, padx=15, pady=8, sticky='w')

    # Frame para los botones con estilo profesional
    frame_input_btns = tk.Frame(producto_frame, bg='#f8f9fa')
    frame_input_btns.grid(row=2, column=0, columnspan=2, pady=15)

    def agregar_producto_wrapper():
        folio_actual[0] = utils.agregar_producto(
            entry_descripcion, entry_precio, entry_folio, tree, folio_actual[0], cursor
        )

    def finalizar_venta_wrapper():
        venta_actual_id[0], folio_actual[0] = utils.finalizar_venta(
            tree, entry_folio, conn, cursor,
            lambda: utils.mostrar_popup_finalizar_venta(
                root,
                lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
                cursor
            ),
            venta_actual_id[0], folio_actual[0]
        )

    # Botones optimizados sin bordes problemáticos
    btn_agregar = crear_boton_optimizado(
        frame_input_btns, "➕ Agregar", agregar_producto_wrapper, "agregar"
    )
    btn_agregar.pack(side="left", padx=15, pady=8)

    btn_cancelar = crear_boton_optimizado(
        frame_input_btns, "❌ Cancelar", 
        lambda: utils.cancelar(tree, entry_descripcion, entry_precio, entry_folio),
        "cancelar"
    )
    btn_cancelar.pack(side="left", padx=15, pady=8)

    # Sección de lista de productos
    lista_frame = EstilosVentas.crear_labelframe(main_container, "📋 Productos en la Venta")
    lista_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    lista_frame.columnconfigure(0, weight=1)

    tree = ttk.Treeview(lista_frame, columns=("descripcion", "precio", "fecha_venta", "folio"), 
                       show="headings", height=8, style="product.Treeview")
    EstilosVentas.configurar_filas_alternadas(tree)
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de venta")
    tree.heading("folio", text="Folio")
    tree.column("descripcion", width=250)
    tree.column("precio", width=120, anchor="center")
    tree.column("fecha_venta", width=180, anchor="center")
    tree.column("folio", width=100, anchor="center")
    tree.grid(row=0, column=0, padx=15, pady=15, sticky='ew')

    # Parche para insertar filas alternadas
    original_insert = tree.insert
    def striped_insert(parent, index, values):
        row_count = len(tree.get_children())
        tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        return original_insert(parent, index, values=values, tags=(tag,))
    tree.insert = striped_insert

    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns", pady=15)

    # Frame para botones de acción
    acciones_frame = tk.Frame(lista_frame, bg='#f8f9fa')
    acciones_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Botones de acción optimizados sin bordes problemáticos
    btn_eliminar = crear_boton_optimizado(acciones_frame, "🗑️ Eliminar", 
                                         lambda: utils.eliminar_seleccionado(tree), "eliminar")
    btn_eliminar.pack(side="left", padx=10)

    btn_modificar = crear_boton_optimizado(acciones_frame, "✏️ Modificar", 
                                          lambda: utils.modificar_seleccionado(tree, entry_descripcion, entry_precio), "modificar")
    btn_modificar.pack(side="left", padx=10)
    
    btn_limpiar = crear_boton_optimizado(acciones_frame, "🧹 Limpiar Todo", 
                                        lambda: utils.limpiar_todo(tree), "limpiar")
    btn_limpiar.pack(side="left", padx=10)

    # Sección de finalización
    finalizacion_frame = tk.Frame(main_container, bg='#f8f9fa')
    finalizacion_frame.grid(row=4, column=0, columnspan=3, pady=20)
    
    # Botón Finalizar venta con estilo destacado y sin bordes problemáticos
    btn_finalizar = crear_boton_optimizado(finalizacion_frame, "✅ Finalizar Venta", 
                                          finalizar_venta_wrapper, "finalizar")
    btn_finalizar.pack(pady=(0, 15))

    # Frame para botones de impresión y correo
    output_frame = tk.Frame(finalizacion_frame, bg='#f8f9fa')
    output_frame.pack()
    
    # Configurar estilo para botones ttk
    style.configure("Elegant.TButton", background="#2c3e50", foreground="white", 
                   font=("Arial", 11, "bold"), relief="raised")

    btn_imprimir = ttk.Button(
        output_frame,
        text="🖨️ Imprimir",
        command=lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
        style="Elegant.TButton"
    )
    btn_imprimir.pack(side='left', padx=15, pady=5)

    btn_email = ttk.Button(
        output_frame,
        text="📧 Enviar por Correo",
        command=lambda: utils.enviar_por_correo(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
        style="Elegant.TButton"
    )
    btn_email.pack(side='left', padx=15, pady=5)

    root.mainloop()

def crear_interfaz_ventas_en_frame(parent_frame, conn, cursor, callback_volver):
    """Crear la interfaz de ventas dentro de un frame existente"""
    # Limpiar el frame padre
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Crear un frame interno completamente centrado
    frame_centrado = EstilosVentas.crear_frame(parent_frame)
    frame_centrado.configure(padx=30, pady=20)
    frame_centrado.place(relx=0.5, rely=0.5, anchor='center')
    
    # Los estilos de Treeview ya están configurados centralizadamente

    venta_actual_id = [None]
    folio_actual = [None]

    # Header profesional centrado
    header_frame = tk.Frame(frame_centrado, bg='#f8f9fa')
    header_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 15))
    header_frame.columnconfigure(1, weight=1)
    
    # Configurar estilos centralizados
    style = configurar_estilos_aplicacion()
    
    # Configurar estilos específicos para macOS si es necesario
    if es_macos():
        configurar_estilos_macos()
    
    # Botón para volver al menú con estilo centralizado
    btn_volver = ttk.Button(header_frame, text="← Volver al Menú", 
                           command=callback_volver, 
                           style="VolverButton.TButton")
    btn_volver.pack(side='left')

    # Título centrado con mejor estilo
    titulo_ventas = EstilosVentas.crear_label_titulo(header_frame, "📊 MÓDULO DE VENTAS")
    titulo_ventas.pack(side='right')

    # Sección de información de venta
    info_frame = tk.LabelFrame(frame_centrado, text="📋 Información de Venta", 
                              font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                              relief='groove', bd=2)
    info_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    info_frame.columnconfigure(0, minsize=180)
    info_frame.columnconfigure(1, weight=1)

    # Etiqueta y campo para folio con mejor estilo
    label_folio = tk.Label(info_frame, text="Folio de venta:", width=20, anchor="e",
                          font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_folio.grid(row=0, column=0, padx=15, pady=10, sticky="e")
    entry_folio = tk.Entry(info_frame, width=35, state="readonly", 
                          font=("Arial", 10), relief='solid', bd=1,
                          bg='#ffffff', fg='#000000', readonlybackground='#f0f0f0')
    entry_folio.grid(row=0, column=1, padx=15, pady=10, sticky='w')
    
    # Etiqueta y campo para nombre del cliente
    label_cliente = tk.Label(info_frame, text="Nombre del cliente:", width=20, anchor="e",
                            font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_cliente.grid(row=1, column=0, padx=15, pady=10, sticky="e")
    entry_cliente = tk.Entry(info_frame, width=35, font=("Arial", 10), 
                            relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_cliente.grid(row=1, column=1, padx=15, pady=10, sticky='w')
    
    # Sección de entrada de productos
    producto_frame = tk.LabelFrame(frame_centrado, text="🗺️ Agregar Producto", 
                                  font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                                  relief='groove', bd=2)
    producto_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    producto_frame.columnconfigure(0, minsize=180)
    producto_frame.columnconfigure(1, weight=1)

    # Etiqueta y campo para descripción con mejor estilo
    label_descripcion = tk.Label(producto_frame, text="Descripción del producto:", width=20, anchor="e",
                                font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_descripcion.grid(row=0, column=0, padx=15, pady=8, sticky="e")
    entry_descripcion = tk.Entry(producto_frame, width=35, font=("Arial", 10), 
                               relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_descripcion.grid(row=0, column=1, padx=15, pady=8, sticky='w')

    # Etiqueta y campo para precio con mejor estilo
    label_precio = tk.Label(producto_frame, text="Precio ($):", width=20, anchor="e",
                           font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#2c3e50')
    label_precio.grid(row=1, column=0, padx=15, pady=8, sticky="e")
    root = parent_frame.winfo_toplevel()
    vcmd = (root.register(lambda texto: utils.validar_decimal(texto)), '%P')
    entry_precio = tk.Entry(producto_frame, width=35, validate="key", validatecommand=vcmd, 
                          font=("Arial", 10), relief='solid', bd=1, bg='#ffffff', fg='#000000')
    entry_precio.grid(row=1, column=1, padx=15, pady=8, sticky='w')

    # Frame para los botones con estilo profesional
    frame_input_btns = tk.Frame(producto_frame, bg='#f8f9fa')
    frame_input_btns.grid(row=2, column=0, columnspan=2, pady=15)

    def agregar_producto_wrapper():
        folio_actual[0] = utils.agregar_producto(
            entry_descripcion, entry_precio, entry_folio, tree, folio_actual[0], cursor
        )

    def finalizar_venta_wrapper():
        venta_actual_id[0], folio_actual[0] = utils.finalizar_venta(
            tree, entry_folio, conn, cursor,
            lambda: utils.mostrar_popup_finalizar_venta(
                root,
                lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
                cursor
            ),
            venta_actual_id[0], folio_actual[0]
        )

    # Botones optimizados sin bordes problemáticos
    btn_agregar = crear_boton_optimizado(frame_input_btns, "➕ Agregar", 
                                        agregar_producto_wrapper, "agregar")
    btn_agregar.pack(side="left", padx=15)

    btn_cancelar = crear_boton_optimizado(frame_input_btns, "❌ Cancelar", 
                                         lambda: utils.cancelar(tree, entry_descripcion, entry_precio, entry_folio), "cancelar")
    btn_cancelar.pack(side="left", padx=15)

    # Sección de lista de productos
    lista_frame = tk.LabelFrame(frame_centrado, text="📋 Productos en la Venta", 
                               font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e', 
                               relief='groove', bd=2)
    lista_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 15), padx=10)
    lista_frame.columnconfigure(0, weight=1)

    tree = ttk.Treeview(lista_frame, columns=("descripcion", "precio", "fecha_venta", "folio"), 
                       show="headings", height=8, style="minimal.Treeview")
    EstilosVentas.configurar_filas_alternadas(tree)
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de venta")
    tree.heading("folio", text="Folio")
    tree.column("descripcion", width=250)
    tree.column("precio", width=120, anchor="center")
    tree.column("fecha_venta", width=180, anchor="center")
    tree.column("folio", width=100, anchor="center")
    tree.grid(row=0, column=0, padx=15, pady=15, sticky='ew')

    # Parche para insertar filas alternadas
    original_insert = tree.insert
    def striped_insert(parent, index, values):
        row_count = len(tree.get_children())
        tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        return original_insert(parent, index, values=values, tags=(tag,))
    tree.insert = striped_insert

    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns", pady=15)

    # Frame para botones de acción
    acciones_frame = tk.Frame(lista_frame, bg='#f8f9fa')
    acciones_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Botones de acción optimizados sin bordes problemáticos
    btn_eliminar = crear_boton_optimizado(acciones_frame, "🗑️ Eliminar", 
                                         lambda: utils.eliminar_seleccionado(tree), "eliminar")
    btn_eliminar.pack(side="left", padx=10)

    btn_modificar = crear_boton_optimizado(acciones_frame, "✏️ Modificar", 
                                          lambda: utils.modificar_seleccionado(tree, entry_descripcion, entry_precio), "modificar")
    btn_modificar.pack(side="left", padx=10)
    
    btn_limpiar = crear_boton_optimizado(acciones_frame, "🧹 Limpiar Todo", 
                                        lambda: utils.limpiar_todo(tree), "limpiar")
    btn_limpiar.pack(side="left", padx=10)

    # Sección de finalización centrada
    finalizacion_frame = tk.Frame(frame_centrado, bg='#f8f9fa')
    finalizacion_frame.grid(row=4, column=0, columnspan=3, pady=15)
    
    # Botón Finalizar venta con estilo destacado y sin bordes problemáticos
    btn_finalizar = crear_boton_optimizado(finalizacion_frame, "✅ Finalizar Venta", 
                                          finalizar_venta_wrapper, "finalizar")
    btn_finalizar.pack(pady=(0, 15))

    # Frame para botones de impresión y correo
    output_frame = tk.Frame(finalizacion_frame, bg='#f8f9fa')
    output_frame.pack()
    
    # Configurar estilo para botones ttk
    style.configure("Elegant.TButton", background="#2c3e50", foreground="white", 
                   font=("Arial", 11, "bold"), relief="raised")

    btn_imprimir = ttk.Button(
        output_frame,
        text="🖨️ Imprimir",
        command=lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
        style="Elegant.TButton"
    )
    btn_imprimir.pack(side='left', padx=15, pady=5)

    btn_email = ttk.Button(
        output_frame,
        text="📧 Enviar por Correo",
        command=lambda: utils.enviar_por_correo(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
        style="Elegant.TButton"
    )
    btn_email.pack(side='left', padx=15, pady=5)