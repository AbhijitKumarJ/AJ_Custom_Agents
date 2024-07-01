from ..base_tool import BaseTool
from utils.logger import logger
from pydub import AudioSegment

class AudioFormatConverterTool(BaseTool):

    def __init__(self):
        super().__init__("Audio Format Converter", "Convert audio files between different formats")
    
    def execute(self, input_path: str, output_path: str):
        logger.log(f"Executing Audio Format Converter Tool")
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=output_path.split('.')[-1])
            return f"Audio successfully converted and saved to {output_path}"
        except Exception as e:
            return f"Error converting audio: {str(e)}"
