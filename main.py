from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
import os
import uuid
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# --- CONFIGURACIÓN ---
client_local = OpenAI(
    base_url="http://10.74.99.20:1234/v1",
    api_key="lm-studio"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CARGA CSV ---
try:
    df = pd.read_csv("comerciales.csv")
    comerciales = [{"nombre": str(row['nombre']), "perfil": f"{row['perfil']} (Especialidad: {row['especialidad']})"} for _, row in df.iterrows()]
    print(f"✅ {len(comerciales)} comerciales cargados")
except Exception as e:
    print(f"❌ Error: {e}")
    comerciales = []

# --- FUNCIÓN EMAIL ---
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

def guardar_datos_cliente_csv(cliente_id, cliente_nombre, comercial_asignado, revisado_por_humano, timestamp):
    df_cliente = pd.DataFrame([{
        "cliente_id": cliente_id,
        "cliente_nombre": cliente_nombre,
        "comercial_asignado": comercial_asignado,
        "revisado_por_humano": revisado_por_humano,
        "timestamp": timestamp
    }])
    if not os.path.isfile("clientes_log.csv"):
        df_cliente.to_csv("clientes_log.csv", index=False)
    else:
        df_cliente.to_csv("clientes_log.csv", mode='a', header=False, index=False)

# --- MODELOS ---
class Cliente(BaseModel):
    nombre: str
    descripcion: str

# --- ENDPOINTS ---
@app.post("/match")
async def match_cliente(cliente: Cliente):
    if not comerciales:
        return {"error": "No se pudieron cargar los comerciales."}

    cliente_id = f"CLIENTE_{uuid.uuid4().hex[:8].upper()}"
    perfiles = "\n".join([f"- {c['nombre']}: {c['perfil']}" for c in comerciales])

    prompt = f"""Comerciales disponibles:
{perfiles}

Cliente ID: {cliente_id}
Descripción: {cliente.descripcion}

¿Qué comercial es el más adecuado? Responde SOLO con el nombre."""

    response = client_local.chat.completions.create(
        model="local-model",
        messages=[{"role": "user", "content": prompt}]
    )

    if not response.choices or not response.choices[0].message.content:
        comercial_asignado = "NO ENCONTRADO, RESPUESTA VACÍA"
    else:
        comercial_asignado = response.choices[0].message.content.strip()

    log = {
        "cliente_id": cliente_id,
        "timestamp": datetime.now().isoformat(),
        "comercial_asignado": comercial_asignado,
        "revisado_por_humano": False
    }

    if comercial_asignado != "NO ENCONTRADO, RESPUESTA VACÍA" and comercial_asignado in [c['nombre'] for c in comerciales]:
        enviar_email(comercial_asignado, f"moralesgonzalezmarcos104@gmail.com", cliente.nombre, cliente.descripcion)
    
    guardar_datos_cliente_csv(cliente_id, cliente.nombre, comercial_asignado, log["revisado_por_humano"], log["timestamp"])

    return {
        "cliente_id": cliente_id,
        "cliente_nombre": cliente.nombre,
        "comercial_asignado": comercial_asignado,
        "revisado_por_humano": False,
        "timestamp": log["timestamp"]
    }

@app.get("/historial_clientes")
async def obtener_historial_clientes():
    if not os.path.isfile("clientes_log.csv"):
        return {"error": "No se han registrado clientes aún."}
    df_historial = pd.read_csv("clientes_log.csv")
    return df_historial.to_dict(orient="records")

@app.post("/revisar_cliente/{cliente_id}")
async def revisar_cliente(cliente_id: str):
    if not os.path.isfile("clientes_log.csv"):
        return {"error": "No se han registrado clientes aún."}
    df_historial = pd.read_csv("clientes_log.csv")
    if cliente_id not in df_historial["cliente_id"].values:
        return {"error": f"No se encontró el cliente con ID {cliente_id}."}
    df_historial.loc[df_historial["cliente_id"] == cliente_id, "revisado_por_humano"] = True
    df_historial.to_csv("clientes_log.csv", index=False)
    return {"message": f"Cliente {cliente_id} marcado como revisado por humano."}

@app.get("/clientes_no_revisados")
async def obtener_clientes_no_revisados():
    if not os.path.isfile("clientes_log.csv"):
        return {"error": "No se han registrado clientes aún."}
    df_historial = pd.read_csv("clientes_log.csv")
    no_revisados = df_historial[df_historial["revisado_por_humano"] == False]
    return no_revisados.to_dict(orient="records")