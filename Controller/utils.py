def enviar_por_correo(cursor, mostrar_popup_sin_productos):
    import tkinter as tk
    from tkinter import messagebox
    def enviar():
        destinatario = entry_email.get().strip()
        if not destinatario:
            messagebox.showwarning("Correo requerido", "Por favor, ingresa un correo destinatario.", parent=popup)
            return
        try:
            # Obtener datos de la última venta FINALIZADA (la más reciente)
            cursor.execute("SELECT MAX(id) FROM VentaMaster")
            venta_id = cursor.fetchone()[0]
            # Validar que hay una venta finalizada
            if venta_id is None:
                messagebox.showerror("Error", "No hay venta finalizada para adjuntar.", parent=popup)
                popup.destroy()
                return
            # Obtener datos de la venta
            cursor.execute("SELECT folio, fecha_venta FROM VentaMaster WHERE id = ?", (venta_id,))
            venta_row = cursor.fetchone()
            folio = venta_row[0]
            fecha = venta_row[1]
            cursor.execute("SELECT descripcion, precio FROM ventas_items WHERE venta_master_id = ?", (venta_id,))
            productos_db = cursor.fetchall()
            if not productos_db:
                messagebox.showerror("Error", "No hay productos en la venta finalizada.", parent=popup)
                popup.destroy()
                return
            else:
                    productos = []
                    total = 0
                    for prod in productos_db:
                        descripcion, precio = prod
                        productos.append({
                            'descripcion': descripcion,
                            'cantidad': 1,
                            'precio': float(precio),
                            'importe': float(precio)
                        })
                        total += float(precio)
                    datos_venta = {
                        'fecha': fecha,
                        'cliente': 'Consumidor Final',
                        'folio': folio
                    }
                    from Controller.createpdf import generar_nota_venta
                    import shutil, os, tempfile
                    nombre_archivo = f"nota_venta_{folio}.pdf"
                    generar_nota_venta(nombre_archivo, datos_venta, productos, total, abrir_pdf=False)
                    # Copiar el PDF a un archivo temporal para evitar problemas de permisos
                    try:
                        temp_dir = tempfile.gettempdir()
                        temp_pdf = os.path.join(temp_dir, f"temp_{nombre_archivo}")
                        shutil.copy2(nombre_archivo, temp_pdf)
                        adjunto_path = temp_pdf
                    except Exception as copy_err:
                        adjunto_path = nombre_archivo  # Si falla, intentar con el original
                    from Controller.email import enviar_correo_desde_db
                    cuerpo = "Adjunto su ticket de compra."
                    try:
                        enviar_correo_desde_db(destinatario, cuerpo, adjunto_path=adjunto_path)
                        messagebox.showinfo("Correo enviado", f"Correo enviado a {destinatario}", parent=popup)
                        # Cerrar el popup de correo y volver a mostrar el popup de los 3 botones
                        popup.destroy()
                        # Volver a mostrar el popup de opciones
                        from Controller.utils import mostrar_popup_finalizar_venta
                        mostrar_popup_finalizar_venta(root, lambda: None, cursor)
                    except Exception as send_err:
                        messagebox.showerror("Error", f"No se pudo enviar el correo: {send_err}", parent=popup)
                    finally:
                        # Intentar borrar el archivo temporal si se creó
                        if 'temp_pdf' in locals() and os.path.exists(temp_pdf):
                            try:
                                os.remove(temp_pdf)
                            except Exception:
                                pass
                    return
            messagebox.showerror("Error", "No hay venta para adjuntar.", parent=popup)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {e}", parent=popup)
        # Ya no se cierra el popup aquí

    root = None
    try:
        # Buscar la ventana principal
        import tkinter as tk
        root = tk._default_root
    except Exception:
        pass
    popup = tk.Toplevel(root)
    popup.title("Enviar por correo")
    popup.geometry("350x150")
    popup.resizable(False, False)
    label = tk.Label(popup, text="Ingresa el correo destinatario:", pady=10)
    label.pack()
    entry_email = tk.Entry(popup, width=35)
    entry_email.pack(pady=5)
    btn_enviar = tk.Button(popup, text="Enviar", command=enviar)
    btn_enviar.pack(pady=10)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)
"""Funciones utilitarias para la lógica de interfaz y validaciones."""
import re
from tkinter import messagebox
from datetime import datetime
from .db_operations import obtener_siguiente_folio, finalizar_venta

def validar_decimal(texto):
    if texto == "":
        return True
    patron = r"^\d{0,6}(\.\d{0,2})?$"
    return re.match(patron, texto) is not None

def agregar_producto(entry_descripcion, entry_precio, entry_folio, tree, folio_actual, cursor):
    import tkinter as tk
    descripcion = entry_descripcion.get()
    precio = entry_precio.get()
    if not descripcion or not precio:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.", parent=entry_descripcion.winfo_toplevel())
        return folio_actual
    try:
        precio_decimal = float(precio)
        if precio_decimal < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Precio inválido", "El precio debe ser un número decimal positivo.", parent=entry_precio.winfo_toplevel())
        return folio_actual
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Si no hay folio actual, generar uno
    if folio_actual is None:
        folio_actual = obtener_siguiente_folio(cursor)
        entry_folio.config(state="normal")
        entry_folio.delete(0, tk.END)
        entry_folio.insert(0, str(folio_actual))
        entry_folio.config(state="readonly")
    # Insertar en Treeview (solo en memoria)
    tree.insert("", tk.END, values=(descripcion, f"${precio_decimal:.2f}", fecha_venta, folio_actual))
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    return folio_actual

## finalizar_venta ahora se importa desde db_operations

def popup_imprimir_nota(imprimir):
    # No necesita tk
    imprimir()

def mostrar_popup_finalizar_venta(root, popup_imprimir_nota, cursor):
    import tkinter as tk
    popup = tk.Toplevel(root)
    popup.title("Finalizar venta")
    popup.geometry("540x180")  # Más ancho para 3 botones grandes
    popup.resizable(False, False)
    label = tk.Label(popup, text="¿Qué deseas hacer?", pady=20)
    label.pack()
    frame = tk.Frame(popup)
    frame.pack(pady=10)
    # Configurar estilo Blue.TButton y usar ttk.Button
    from tkinter import ttk
    style = ttk.Style()
    style.configure("Blue.TButton", background="#357ab8", foreground="white")
    style.configure("Red.TButton", background="#c0392b", foreground="white")
    btn_imprimir = ttk.Button(frame, text="Imprimir", width=13, style="Blue.TButton", command=lambda: [popup.destroy(), popup_imprimir_nota()])
    btn_imprimir.pack(side="left", padx=8)

    # Botón Enviar por correo (igual funcionalidad que el principal)
    import Controller.utils as utils_mod
    btn_enviar_correo = ttk.Button(
        frame,
        text="Enviar por correo",
        width=17,
        style="Blue.TButton",
        command=lambda: [popup.destroy(), utils_mod.enviar_por_correo(cursor, lambda: utils_mod.mostrar_popup_sin_productos(root))]
    )
    btn_enviar_correo.pack(side="left", padx=8)

    btn_no = ttk.Button(frame, text="Cerrar", width=10, style="Red.TButton", command=popup.destroy)
    btn_no.pack(side="left", padx=8, pady=5)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)

def cancelar(tree, entry_descripcion, entry_precio, entry_folio):
    import tkinter as tk
    tree.delete(*tree.get_children())
    entry_descripcion.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_folio.config(state="normal")
    import tkinter as tk
    entry_folio.delete(0, tk.END)
    entry_folio.config(state="readonly")
    return None, None

def imprimir(cursor, mostrar_popup_sin_productos):
    cursor.execute("SELECT MAX(id) FROM VentaMaster")
    venta_id = cursor.fetchone()[0]
    if venta_id:
        cursor.execute("SELECT folio, fecha_venta FROM VentaMaster WHERE id = ?", (venta_id,))
        venta_row = cursor.fetchone()
        folio = venta_row[0]
        fecha = venta_row[1]
        cursor.execute("""
            SELECT descripcion, precio FROM ventas_items WHERE venta_master_id = ?
        """, (venta_id,))
        productos_db = cursor.fetchall()
        if productos_db:
            productos = []
            total = 0
            for prod in productos_db:
                descripcion, precio = prod
                productos.append({
                    'descripcion': descripcion,
                    'cantidad': 1,
                    'precio': float(precio),
                    'importe': float(precio)
                })
                total += float(precio)
            datos_venta = {
                'fecha': fecha,
                'cliente': 'Consumidor Final',
                'folio': folio
            }
            from Controller.createpdf import generar_nota_venta
            nombre_archivo = f"nota_venta_{folio}.pdf"
            generar_nota_venta(nombre_archivo, datos_venta, productos, total, abrir_pdf=True)
            return
    mostrar_popup_sin_productos()

def limpiar_todo(tree):
    tree.delete(*tree.get_children())

def eliminar_seleccionado(tree):
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)
    else:
        parent = tree.winfo_toplevel()
        messagebox.showinfo("Selecciona un producto", "Debes seleccionar un producto para eliminar.", parent=parent)

def modificar_seleccionado(tree, entry_descripcion, entry_precio):
    import tkinter as tk
    selected = tree.selection()
    if selected:
        item = selected[0]
        values = tree.item(item, "values")
        descripcion, precio, fecha_venta, folio = values
        precio = precio.replace("$", "")
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, descripcion)
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, precio)
        tree.delete(item)
    else:
        messagebox.showinfo("Selecciona un producto", "Debes seleccionar un producto para modificar.", parent=entry_descripcion.winfo_toplevel())

def mostrar_popup_sin_productos(root):
    import tkinter as tk
    import tkinter as tk
    popup = tk.Toplevel(root)
    popup.title("Sin productos")
    popup.geometry("300x120")
    popup.resizable(False, False)
    label = tk.Label(popup, text="No hay productos para imprimir.", pady=20)
    label.pack()
    btn_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy)
    btn_cerrar.pack(pady=10)
    popup.transient(root)
    popup.grab_set()