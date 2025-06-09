from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.services.translation_service import translation_service
from app.services.tts_service import tts_service

router = APIRouter(tags=["combined"])

class TranslationAndSpeechRequest(BaseModel):
    text: str
    target_language: Literal["tamil", "telugu", "hindi"]

@router.post("/translate-and-speak")
async def translate_and_speak(request: TranslationAndSpeechRequest):
    """
    Complete workflow: Translate text and convert to speech
    """
    try:
        # Step 1: Translate the text
        translation_result = translation_service.translate_text(
            text=request.text,
            target_language=request.target_language
        )
        translated_text = translation_result["translated_text"]

        # Step 2: Convert translated text to speech
        audio_response = await tts_service.text_to_speech(
            text=translated_text,
            language=request.target_language
        )

        return {
            "original_text": request.text,
            "translated_text": translated_text,
            "audio_file": audio_response
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 