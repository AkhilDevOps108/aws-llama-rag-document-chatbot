from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models.document import ChatRequest, ChatResponse, ChatSource
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    settings = get_settings()
    embedding_service = EmbeddingService()
    vector_service = VectorService()
    llm_service = LLMService()

    query_embedding = embedding_service.embed_query(request.question)
    matches = vector_service.search(query_embedding, top_k=settings.top_k)
    if not matches:
        raise HTTPException(status_code=404, detail="No indexed document context found.")

    context = "\n\n".join(
        f"[{match['document_name']} - page {match.get('page_number') or 'n/a'}]\n{match['text']}"
        for match in matches
    )
    answer = await llm_service.generate_answer(context, request.question)

    return ChatResponse(
        answer=answer,
        sources=[
            ChatSource(
                document_name=str(match["document_name"]),
                page_number=match.get("page_number"),
                score=float(match["score"]),
                text=str(match["text"]),
            )
            for match in matches
        ],
    )
