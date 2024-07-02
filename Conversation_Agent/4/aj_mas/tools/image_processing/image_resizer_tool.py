from ..base_tool import BaseTool
from aj_mas.utils import logger
from PIL import Image

class ImageResizerTool(BaseTool):
    def __init__(self):
        super().__init__("Image Resizer", "Resize an image to specified dimensions")

    def execute(self, image_path: str, width: int, height: int, output_path: str):
        logger.log(f"Executing Image Resizer Tool")
        try:
            with Image.open(image_path) as img:
                resized_img = img.resize((width, height))
                resized_img.save(output_path)
            return f"Image successfully resized and saved to {output_path}"
        except Exception as e:
            return f"Error resizing image: {str(e)}"