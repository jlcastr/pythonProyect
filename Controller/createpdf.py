from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generar_nota_venta(nombre_archivo, datos_venta, productos, total, abrir_pdf=True):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "NOTA DE VENTA")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Fecha: {datos_venta['fecha']}")
    c.drawString(50, height - 85, f"Cliente: {datos_venta['cliente']}")
    c.drawString(50, height - 100, f"Folio: {datos_venta['folio']}")

    # Tabla de productos
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 130, "Descripción")
    c.drawString(250, height - 130, "Cantidad")
    c.drawString(350, height - 130, "Precio")
    c.drawString(450, height - 130, "Importe")

    y = height - 145
    c.setFont("Helvetica", 10)
    for prod in productos:
        c.drawString(50, y, prod['descripcion'])
        c.drawString(250, y, str(prod['cantidad']))
        c.drawString(350, y, f"${prod['precio']:.2f}")
        c.drawString(450, y, f"${prod['importe']:.2f}")
        y -= 15

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y - 20, "Total:")
    c.drawString(450, y - 20, f"${total:.2f}")

    c.save()

    # Abrir el PDF generado automáticamente (solo en Windows)
    if abrir_pdf:
        import os
        try:
            os.startfile(nombre_archivo)
        except Exception:
            pass

