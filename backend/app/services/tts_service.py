from gtts import gTTS
import io
from typing import Literal

class TTSService:
    def __init__(self):
        self.supported_languages = {
            "tamil": "ta",
            "telugu": "te",
            "hindi": "hi"
        }

    async def text_to_speech(self, text: str, language: Literal["tamil", "telugu", "hindi"]) -> bytes:
        """
        Convert text to speech using gTTS
        Returns audio data as bytes
        """
        if not text:
            raise ValueError("Text cannot be empty")

        if language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {language}")

        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=self.supported_languages[language], slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.getvalue()
        except Exception as e:
            raise Exception(f"Failed to generate speech: {str(e)}")

# Create a singleton instance
tts_service = TTSService() 