from Controller.SQL.db_operations import obtener_email_config
# Enviar correo usando credenciales almacenadas en la base de datos
def enviar_correo_desde_db(destinatario, cuerpo, adjunto_path=None):
    remitente, password = obtener_email_config()
    if not remitente or not password:
        raise Exception("No hay configuración de correo guardada.")
    enviar_correo(destinatario, "Ticket de compra S&M", cuerpo, remitente, password, adjunto_path)
import smtplib
from email.message import EmailMessage

def enviar_correo(destinatario, asunto, cuerpo, remitente, password, adjunto_path=None):
    msg = EmailMessage()
    msg['Subject'] = "Ticket de compra S&M"
    msg['From'] = remitente
    msg['To'] = destinatario
    msg.set_content(cuerpo)

    # Adjuntar archivo si se proporciona
    if adjunto_path:
        with open(adjunto_path, 'rb') as f:
            file_data = f.read()
            file_name = adjunto_path.split('/')[-1]
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Configuración automática de servidor y puerto según el dominio del remitente
    dominio = remitente.split('@')[-1].lower()
    if 'gmail.com' in dominio:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
    elif 'outlook.com' in dominio or 'hotmail.com' in dominio or 'live.com' in dominio:
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
    elif 'yahoo.com' in dominio:
        smtp_server = 'smtp.mail.yahoo.com'
        smtp_port = 587
    else:
        smtp_server = 'smtp.' + dominio
        smtp_port = 587
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(remitente, password)
        smtp.send_message(msg)

def enviar_correo_prueba(remitente, password, destinatario):
    """
    Enviar correo de prueba para verificar configuración
    
    Args:
        remitente: Email del remitente
        password: Contraseña del remitente
        destinatario: Email de destino (puede ser el mismo remitente)
    
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    try:
        asunto = "🔧 Prueba de Configuración - Sistema S&M"
        cuerpo = """
¡Hola!

Este es un correo de prueba del Sistema de Ventas S&M.

Si estás recibiendo este mensaje, significa que la configuración de tu correo electrónico está funcionando correctamente.

✅ Configuración verificada exitosamente
📧 Remitente: {}
🕒 Fecha: {}

¡Ya puedes usar el sistema para enviar reportes y facturas!

---
Sistema de Ventas S&M
Configuración de Email
        """.format(remitente, __import__('datetime').datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        # Enviar el correo
        enviar_correo(destinatario, asunto, cuerpo, remitente, password)
        print(f"[EMAIL] Correo de prueba enviado exitosamente a: {destinatario}")
        return True
        
    except Exception as e:
        print(f"[EMAIL] Error enviando correo de prueba: {e}")
        return False

# Ejemplo de uso:
# enviar_correo(
#     destinatario='destino@email.com',
#     asunto='Prueba',
#     cuerpo='Este es un correo de prueba',
#     remitente='tucorreo@gmail.com',
#     password='tu_contraseña',
#     adjunto_path=None
# )
