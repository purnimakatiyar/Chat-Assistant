import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_response
from app.services.insight_service import extract_insights

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    logger.info("Received message (history_len=%d)", len(request.history))

    ai_response = generate_response(request.message, request.history)
    insights = extract_insights(request.message)

    return ChatResponse(response=ai_response, insights=insights)
