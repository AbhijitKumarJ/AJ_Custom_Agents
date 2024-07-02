from ..base_tool import BaseTool
from aj_mas.utils import logger
from PIL import Image
from PIL.ExifTags import TAGS

class ImageMetadataExtractorTool(BaseTool):
    def __init__(self):
        super().__init__("Image Metadata Extractor", "Extract metadata from an image")

    def execute(self, image_path: str):
        logger.log(f"Executing Image Metadata Extractor Tool")
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    metadata = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        metadata[tag] = value
                    return metadata
                else:
                    return "No metadata found in the image"
        except Exception as e:
            return f"Error extracting metadata: {str(e)}"