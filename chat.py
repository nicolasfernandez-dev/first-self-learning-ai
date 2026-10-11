from dotenv import load_dotenv
load_dotenv()

import os
import time
from google import genai
from google.genai import errors
from mem0 import Memory




MODELO = "gemini-3.8-flash"
USER_ID = "nicolas_user"
MAX_HISTORIAL = 20  # mensajes de corto plazo que se conservan

config = {
    "llm": {
        "provider": "gemini",
        "config": {"model": MODELO},
    },
    "embedder": {
        "provider": "gemini",
        "config": {"model": "gemini-embedding-001", "embedding_dims": 768},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "memoria_gemini",
            "embedding_model_dims": 768,
        },
    },
}

memoria = Memory.from_config(config_dict=config)
cliente = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

historial = []  # memoria a corto plazo (solo esta sesión)


def generar(historial, sistema, intentos=4):
    """Llama a Gemini reintentando con espera creciente si está saturado."""
    for i in range(intentos):
        try:
            return cliente.models.generate_content(
                model=MODELO,
                contents=historial,
                config={"system_instruction": sistema},
            ).text
        except errors.ServerError:
            if i == intentos - 1:
                raise
            espera = 2 ** (i + 1)  # 2, 4, 8 segundos
            print(f"(Gemini saturado, reintentando en {espera}s...)")
            time.sleep(espera)


print("Escribe 'salir' para terminar.\n")

while True:
    entrada = input("Tú: ").strip()
    if entrada.lower() in ("salir", "exit"):
        break
    if not entrada:
        continue

    # 1. Recuperar recuerdos relevantes de la memoria a largo plazo
    try:
        encontrados = memoria.search(entrada, filters={"user_id": USER_ID}, top_k=5)
        recuerdos = "\n".join(f"- {r['memory']}" for r in encontrados["results"])
    except Exception as e:
        print(f"(No se pudo consultar la memoria: {e})")
        recuerdos = ""

    # 2. Construir el prompt de sistema con los recuerdos
    sistema = (
        "Eres un asistente personal con memoria a largo plazo. "
        "Usa estos recuerdos del usuario cuando sean relevantes, "
        "sin mencionarlos si no vienen al caso:\n"
        f"{recuerdos or '(sin recuerdos todavía)'}"
    )
    historial.append({"role": "user", "parts": [{"text": entrada}]})

    # 3. Generar la respuesta
    try:
        texto = generar(historial, sistema)
    except Exception as e:
        print(f"\nError al generar la respuesta: {e}\n")
        historial.pop()  # quitamos el mensaje que no obtuvo respuesta
        continue

    historial.append({"role": "model", "parts": [{"text": texto}]})
    historial[:] = historial[-MAX_HISTORIAL:]
    print(f"\nAgente: {texto}\n")

    # 4. Guardar el intercambio para que mem0 extraiga lo importante
    try:
        memoria.add(
            [
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": texto},
            ],
            user_id=USER_ID,
        )
    except Exception as e:
        print(f"(No se pudo guardar el recuerdo: {e})")