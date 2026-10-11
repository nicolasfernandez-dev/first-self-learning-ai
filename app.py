from dotenv import load_dotenv
load_dotenv()

import os
from mem0 import Memory


config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-3.8-flash",  # cámbialo por uno de tu lista
        },
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "gemini-embedding-001",
            "embedding_dims": 768,
        },
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

m = Memory.from_config(config_dict=config)

print("🧠 Guardando recuerdos...")
m.add(
    "Me llamo Nicolás y prefiero programar la lógica en C++ o Java antes que en otros lenguajes.",
    user_id="nicolas_user",
)

print("🔍 Buscando en la memoria...")
resultados = m.search(
    "¿Cómo me llamo y qué lenguajes prefiero usar?",
    filters={"user_id": "nicolas_user"},
)

print("\n--- RECUERDOS EXTRAÍDOS POR LA IA ---")
for recuerdo in resultados["results"]:
    print(f"- {recuerdo['memory']}")