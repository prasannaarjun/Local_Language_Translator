from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.services.tts_service import tts_service

router = APIRouter(tags=["text-to-speech"])

class TextToSpeechRequest(BaseModel):
    text: str
    language: Literal["tamil", "telugu", "hindi"]

@router.post("/text-to-speech")
async def convert_text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech in the specified language
    """
    try:
        return await tts_service.text_to_speech(
            text=request.text,
            language=request.language
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 