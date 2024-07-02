from ..base_tool import BaseTool
from aj_mas.utils import logger
from gtts import gTTS

class TextToSpeechTool(BaseTool):
    def __init__(self):
        super().__init__("Text to Speech", "Convert text to speech")

    def execute(self, text: str, language: str = 'en', output_path: str = 'output.mp3'):
        logger.log(f"Executing Text to Speech Tool")
        try:
            tts = gTTS(text=text, lang=language)
            tts.save(output_path)
            return f"Text-to-speech conversion successful. Audio saved to {output_path}"
        except Exception as e:
            return f"Error in text-to-speech conversion: {str(e)}"