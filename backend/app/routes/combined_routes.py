from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal
from app.services.translation_service import translation_service
from app.services.tts_service import tts_service
import base64

router = APIRouter(tags=["combined"])

class TranslationAndSpeechRequest(BaseModel):
    text: str
    target_language: Literal["tamil", "telugu", "hindi"]

@router.post("/translate-and-speak")
async def translate_and_speak(request: TranslationAndSpeechRequest):
    """
    Complete workflow: Translate text and convert to speech
    Returns both translation and audio data
    """
    try:
        # Step 1: Translate the text
        translation_result = translation_service.translate_text(
            text=request.text,
            target_language=request.target_language
        )
        translated_text = translation_result["translated_text"]

        # Step 2: Convert translated text to speech
        audio_data = await tts_service.text_to_speech(
            text=translated_text,
            language=request.target_language
        )

        # Convert audio data to base64 for JSON response
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return JSONResponse({
            "original_text": request.text,
            "translated_text": translated_text,
            "audio_data": audio_base64
        })

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 