# first-self-learning-ai

Mi primer agente de IA con memoria a largo plazo. Es un chat en la terminal que recuerda cosas sobre el usuario entre sesiones.

## Cómo funciona

En cada mensaje, el agente:

1. **Busca** recuerdos relevantes en una base de datos vectorial (Qdrant).
2. **Añade** esos recuerdos al prompt de sistema.
3. **Genera** la respuesta con Gemini.
4. **Guarda** lo importante de la conversación con mem0.

Es una versión sencilla del patrón RAG (Retrieval-Augmented Generation).

## Tecnologías

| Pieza | Función |
|---|---|
| [Gemini](https://ai.google.dev/) | LLM para responder y extraer recuerdos; embeddings para convertir texto en vectores |
| [mem0](https://github.com/mem0ai/mem0) | Capa de memoria: extrae, guarda y busca recuerdos |
| [Qdrant](https://qdrant.tech/) | Base de datos vectorial, ejecutada en Docker |
| Python 3.11 | Lenguaje del proyecto, con entorno virtual (`venv`) |

## Requisitos

- Python 3.11
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Una API key de Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd first-self-learning-ai

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar las variables de entorno
cp .env.example .env
# y poner tu API key en .env
```

## Uso

Con Docker Desktop abierto:

```bash
docker compose up -d          # arrancar Qdrant
source venv/bin/activate      # activar el entorno
python chat.py                # iniciar el chat
```

Escribe `salir` para terminar. Para parar Qdrant: `docker compose stop`.

## Estructura

```
first-self-learning-ai/
├── chat.py              # el agente: bucle de chat con memoria
├── app.py               # prueba de concepto de la memoria
├── docker-compose.yml   # configuración del contenedor de Qdrant
├── requirements.txt     # dependencias de Python
├── .env.example         # plantilla de variables de entorno
└── .gitignore
```

No se suben al repositorio: `.env` (secretos), `venv/` (se regenera), `qdrant_data/` y `.mem0/` (datos locales).

## Limitaciones conocidas

- El plan gratuito de Gemini tiene un límite diario de peticiones, y cada turno de chat consume varias (respuesta + extracción de recuerdos).
- El historial de la sesión se limita a los últimos 20 mensajes.
