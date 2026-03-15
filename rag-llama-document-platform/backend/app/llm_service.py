import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://34.204.89.228:11434/api/generate")


def ask_llm(question: str, context: list[str]) -> str:
    prompt = f"""
You are an AI assistant.

Context:
{context}

Question:
{question}

Answer based only on the context.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    response.raise_for_status()

    return response.json()["response"]
