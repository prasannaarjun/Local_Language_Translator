from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
from app.services.tts_service import tts_service
import io

router = APIRouter(tags=["text-to-speech"])

class TextToSpeechRequest(BaseModel):
    text: str
    language: Literal["tamil", "telugu", "hindi"]

@router.post("/text-to-speech")
async def convert_text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech in the specified language
    Returns audio file as binary response
    """
    try:
        audio_data = await tts_service.text_to_speech(
            text=request.text,
            language=request.language
        )
        
        # Create a BytesIO object from the audio data
        audio_buffer = io.BytesIO(audio_data)
        
        # Return as streaming response
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 