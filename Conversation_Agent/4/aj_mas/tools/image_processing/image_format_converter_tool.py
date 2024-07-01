from ..base_tool import BaseTool
from utils.logger import logger
from PIL import Image

class ImageFormatConverterTool(BaseTool):
    def __init__(self):
        super().__init__("Image Format Converter", "Convert image from one format to another")

    def execute(self, input_path: str, output_path: str):
        logger.log(f"Executing Image Format Converter Tool")
        try:
            with Image.open(input_path) as img:
                img.save(output_path)
            return f"Image successfully converted and saved to {output_path}"
        except Exception as e:
            return f"Error converting image: {str(e)}"