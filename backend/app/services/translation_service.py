from googletrans import Translator
from typing import Literal

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            "tamil": "ta",
            "telugu": "te",
            "hindi": "hi"
        }

    def translate_text(
        self,
        text: str,
        target_language: Literal["tamil", "telugu", "hindi"]
    ) -> dict:
        """
        Translate text from English to the specified target language
        """
        if not text:
            raise ValueError("Text cannot be empty")

        if target_language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {target_language}")

        try:
            # Translate from English to target language
            result = self.translator.translate(
                text,
                src="en",
                dest=self.supported_languages[target_language]
            )

            return {
                "original_text": text,
                "translated_text": result.text,
                "source_language": "en",
                "target_language": target_language
            }
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

# Create a singleton instance
translation_service = TranslationService() 