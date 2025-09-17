import tkinter as tk
from tkinter import ttk
import Controller.utils as utils
import Controller.db_operations as db_operations

def crear_pantalla_principal(conn, cursor, menubar):
    import tkinter as tk
    root = tk.Tk()
    # Estilo personalizado para Treeview de productos (igual que el reporte)
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use("default")
    style.configure("minimal.Treeview",
                    background="#fafafa",
                    foreground="#222",
                    rowheight=24,
                    fieldbackground="#fafafa",
                    font=("Segoe UI", 10),
                    borderwidth=0)
    style.configure("minimal.Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#eaeaea",
                    foreground="#222",
                    borderwidth=0)
    style.layout("minimal.Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'})
    ])
    style.map("minimal.Treeview",
              background=[('selected', '#e0e0e0')])
    style.map("minimal.Treeview.Heading",
              background=[('active', '#cccccc')])

    venta_actual_id = [None]
    folio_actual = [None]
    root.after(0, lambda: root.title("Agregar Producto"))
    root.geometry("900x570")
    root.resizable(False, False)
    from View.menu import menubar as menu_fn
    root.config(menu=menu_fn(root))

    # Etiqueta y campo para folio (readonly)
    label_folio = tk.Label(root, text="Folio de venta:")
    label_folio.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_folio = tk.Entry(root, width=30, state="readonly")
    entry_folio.grid(row=0, column=1, padx=10, pady=5)

    # Etiqueta y campo para descripción
    label_descripcion = tk.Label(root, text="Descripción del producto:")
    label_descripcion.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_descripcion = tk.Entry(root, width=30)
    entry_descripcion.grid(row=1, column=1, padx=10, pady=5)

    # Etiqueta y campo para precio
    label_precio = tk.Label(root, text="Precio (máx 6 enteros y 2 decimales):")
    label_precio.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    vcmd = (root.register(lambda texto: utils.validar_decimal(texto)), '%P')
    entry_precio = tk.Entry(root, width=30, validate="key", validatecommand=vcmd)
    entry_precio.grid(row=2, column=1, padx=10, pady=5)

    # Frame para los botones Agregar y Cancelar debajo de los inputs
    frame_input_btns = tk.Frame(root)
    frame_input_btns.grid(row=3, column=0, columnspan=2, pady=10)

    def agregar_producto_wrapper():
        folio_actual[0] = utils.agregar_producto(
            entry_descripcion, entry_precio, entry_folio, tree, folio_actual[0], cursor
        )

    def finalizar_venta_wrapper():
        venta_actual_id[0], folio_actual[0] = utils.finalizar_venta(
                tree, entry_folio, conn, cursor,
                lambda: utils.mostrar_popup_finalizar_venta(root, lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root))),
                venta_actual_id[0], folio_actual[0]
            )

    btn_agregar = tk.Button(frame_input_btns, text="Agregar", command=agregar_producto_wrapper)
    btn_agregar.pack(side="left", padx=10)

    btn_cancelar = tk.Button(frame_input_btns, text="Cancelar", command=lambda: utils.cancelar(tree, entry_descripcion, entry_precio, entry_folio), fg="black")
    btn_cancelar.pack(side="left", padx=10)

    # Treeview para mostrar productos con columnas
    label_lista = tk.Label(root, text="Productos agregados:")
    label_lista.grid(row=4, column=0, padx=10, pady=5, sticky="ne")

    tree = ttk.Treeview(root, columns=("descripcion", "precio", "fecha_venta", "folio"), show="headings", height=8, style="product.Treeview")
    tree.tag_configure('oddrow', background='#e6f2ff')
    tree.tag_configure('evenrow', background='#ffffff')
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("fecha_venta", text="Fecha de venta")
    tree.heading("folio", text="Folio")
    tree.column("descripcion", width=200)
    tree.column("precio", width=100, anchor="center")
    tree.column("fecha_venta", width=200, anchor="center")
    tree.column("folio", width=100, anchor="center")
    tree.grid(row=4, column=1, padx=10, pady=5)

    # Parche para insertar filas alternadas
    original_insert = tree.insert
    def striped_insert(parent, index, values):
        row_count = len(tree.get_children())
        tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        return original_insert(parent, index, values=values, tags=(tag,))
    tree.insert = striped_insert

    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=4, column=2, sticky="ns", pady=5)

    # Botones debajo de la lista
    btn_eliminar = tk.Button(root, text="Eliminar seleccionado", command=lambda: utils.eliminar_seleccionado(tree))
    btn_eliminar.grid(row=5, column=0, padx=10, pady=5, sticky="e")

    btn_limpiar = tk.Button(root, text="Limpiar todo", command=lambda: utils.limpiar_todo(tree), fg="black")
    btn_limpiar.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    btn_modificar = tk.Button(root, text="Modificar seleccionado", command=lambda: utils.modificar_seleccionado(tree, entry_descripcion, entry_precio))
    btn_modificar.grid(row=5, column=1, padx=10, pady=5, sticky="e")

    # Botón Finalizar venta (centrado arriba de imprimir)
    btn_finalizar = tk.Button(root, text="Finalizar venta", command=finalizar_venta_wrapper, fg="black", width=20)
    btn_finalizar.grid(row=6, column=1, padx=10, pady=(20, 5), sticky="n")

    # Botón Imprimir debajo de todos los demás, alineado a la derecha (usando ttk para color personalizado en macOS)
    style.configure("Blue.TButton", background="#357ab8", foreground="white")
    btn_imprimir = ttk.Button(
        root,
        text="Imprimir",
        command=lambda: utils.imprimir(cursor, lambda: utils.mostrar_popup_sin_productos(root)),
        style="Blue.TButton"
    )
    btn_imprimir.grid(row=7, column=1, padx=10, pady=20, sticky="e")

    root.mainloop()