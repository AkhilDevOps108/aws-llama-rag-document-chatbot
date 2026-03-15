from __future__ import annotations

import httpx

from app.config import get_settings


PROMPT_TEMPLATE = """You are a helpful assistant answering questions from company documents.

Context:
{retrieved_chunks}

Question:
{user_question}

Answer clearly using the provided context."""


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ollama_url.rstrip("/")
        self.model = settings.ollama_model

    async def generate_answer(self, retrieved_chunks: str, user_question: str) -> str:
        prompt = PROMPT_TEMPLATE.format(
            retrieved_chunks=retrieved_chunks,
            user_question=user_question,
        )

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()
