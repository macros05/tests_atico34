import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env
def enviar_email(comercial_nombre, comercial_email, cliente_nombre, descripcion):
    msg = MIMEMultipart()
    msg['Subject'] = f'🎯 Nuevo cliente asignado: {cliente_nombre}'
    msg['From'] = 'moralesgonzalezmarcos104@gmail.com'
    msg['To'] = comercial_email

    cuerpo = f"""
Hola {comercial_nombre},

Se te ha asignado un nuevo cliente automáticamente.

Cliente: {cliente_nombre}
Descripción: {descripcion}

Por favor, contacta con el cliente a la brevedad.

Sistema de Matching Automático - Atico34
    """

    msg.attach(MIMEText(cuerpo, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('moralesgonzalezmarcos104@gmail.com', os.getenv("GMAIL_APP_PASSWORD"))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"✅ Email enviado a {comercial_email}")

# Prueba mandándotelo a ti mismo
enviar_email(
    comercial_nombre="Juan",
    comercial_email="moralesgonzalezmarcos104@gmail.com",
    cliente_nombre="Empresa Test RGPD",
    descripcion="Empresa mediana que necesita cumplir con el RGPD urgentemente"
)