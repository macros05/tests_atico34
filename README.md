# Sistema de Matching Cliente-Comercial con IA Local

Prototipo construido en menos de 12 horas como ejercicio práctico aplicado al sector legaltech.

## ¿Qué hace?

Recibe la descripción de un cliente potencial y asigna automáticamente el comercial más adecuado usando IA local. Una vez asignado, notifica al comercial por email de forma automática.

## ¿Por qué IA local?

En el sector legal y de protección de datos, los datos de clientes son altamente sensibles. Este sistema usa LM Studio para ejecutar el modelo de IA completamente en local — los datos nunca salen de la infraestructura.

## Arquitectura
Cliente → POST /match → Anonimización (ID único) →
IA Local (LM Studio) → Matching → Email automático al comercial

## Stack

- **FastAPI** — API REST
- **LM Studio** — IA local (datos nunca salen de la máquina)
- **pandas** — carga de comerciales desde CSV
- **smtplib** — notificación por email
- **python-dotenv** — gestión segura de credenciales

## Cumplimiento RGPD

- La IA procesa IDs anónimos, nunca nombres reales
- Los datos de clientes no se envían a APIs externas
- Log de auditoría con timestamp en cada decisión
- Campo `revisado_por_humano` para cumplir el artículo 22 del RGPD

## Instalación

```bash
pip install fastapi uvicorn pandas openai python-dotenv
```

Crea un archivo `.env`:
GMAIL_APP_PASSWORD=tu_app_password

## Uso

```bash
uvicorn main:app --reload
```

Prueba en `http://localhost:8000/docs`

## Ejemplo de respuesta

```json
{
  "cliente_id": "CLIENTE_7BD38BCD",
  "cliente_nombre": "Empresa Test",
  "comercial_asignado": "Juan",
  "revisado_por_humano": false,
  "timestamp": "2026-04-15T20:58:40"
}
```