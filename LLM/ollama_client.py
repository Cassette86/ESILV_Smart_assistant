"""
Client simple pour appeler un LLM via Ollama en local.

Pré-requis :
- Ollama installé et lancé
- un modèle téléchargé (ex: llama3.1, mistral, etc.)
- commande de test : ollama run llama3.1

Ce module expose une fonction generate(text_prompt) qui renvoie la réponse du modèle.
"""

import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


def generate(prompt: str) -> str:
    """
    Appelle Ollama /api/generate avec un prompt texte.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    return r.json().get("response", "").strip()
