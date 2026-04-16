# Sistema de Matching Cliente-Comercial con IA Local

Prototipo construido en menos de 24 horas como ejercicio práctico aplicado al sector legaltech, tras conocer la problemática real de la empresa.

## ¿Qué hace?

Recibe la descripción de un cliente potencial, asigna automáticamente el comercial más adecuado usando IA local, notifica al comercial por email y registra cada decisión con trazabilidad completa para cumplimiento RGPD.

## ¿Por qué IA local?

En el sector legal y de protección de datos, los datos de clientes son altamente sensibles. Este sistema usa LM Studio para ejecutar el modelo de IA completamente en local — los datos nunca salen de la infraestructura.

## Arquitectura
Cliente → POST /match → Anonimización (ID único) →
IA Local (LM Studio) → Matching → Email automático al comercial
→ Log de auditoría

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/match` | Asigna comercial y notifica por email |
| GET | `/historial_clientes` | Historial completo de asignaciones |
| GET | `/clientes_no_revisados` | Asignaciones pendientes de revisión humana |
| POST | `/revisar_cliente/{id}` | Marcar asignación como revisada |
| GET | `/estadisticas_comerciales` | Total de clientes por comercial |

## Stack

- **FastAPI** — API REST asíncrona
- **LM Studio** — IA local (datos nunca salen de la máquina)
- **pandas** — carga de comerciales y log desde CSV
- **smtplib** — notificación automática por email
- **python-dotenv** — gestión segura de credenciales
- **HTML/CSS/JS** — dashboard de control en tiempo real

## Cumplimiento RGPD

- La IA procesa IDs anónimos, nunca nombres reales
- Los datos de clientes no se envían a APIs externas
- Log de auditoría con timestamp en cada decisión
- Campo `revisado_por_humano` para cumplir el artículo 22 del RGPD
- Credenciales gestionadas con variables de entorno

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

API docs en `http://localhost:8000/docs`
Dashboard en `dashboard.html`

## Ejemplo de respuesta

```json
{
  "cliente_id": "CLIENTE_7BD38BCD",
  "cliente_nombre": "Clinica dental Málaga",
  "comercial_asignado": "Ana",
  "revisado_por_humano": false,
  "timestamp": "2026-04-16T10:37:44"
}
```

## Mejoras planificadas para producción

- Base de datos SQL en lugar de CSV
- Endpoints asíncronos completos
- Tests con pytest
- Notificaciones por Slack o WhatsApp
- Autenticación en los endpoints