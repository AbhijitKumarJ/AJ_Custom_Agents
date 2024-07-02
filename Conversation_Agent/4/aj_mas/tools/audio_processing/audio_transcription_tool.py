from ..base_tool import BaseTool
from aj_mas.utils import logger
import speech_recognition as sr

class AudioTranscriptionTool(BaseTool):
    def __init__(self):
        super().__init__("Audio Transcription", "Transcribe speech from audio files")
        self.recognizer = sr.Recognizer()

    def execute(self, audio_file_path: str, language: str = "en-US"):
        logger.log(f"Executing Audio Transcription Tool")
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"