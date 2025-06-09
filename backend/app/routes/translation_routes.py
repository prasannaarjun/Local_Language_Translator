from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.services.translation_service import translation_service

router = APIRouter(tags=["translation"])

class TranslationRequest(BaseModel):
    text: str
    target_language: Literal["tamil", "telugu", "hindi"]

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from English to the specified target language
    """
    try:
        result = translation_service.translate_text(
            text=request.text,
            target_language=request.target_language
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 