import pytesseract
from PIL import Image

class OCRService:
    """
    OCRService provides Optical Character Recognition (OCR) functionalities using Tesseract.

    Attributes:
        pytesseract.pytesseract.tesseract_cmd (str): The path to the Tesseract executable.
    
    Methods:
        perform_ocr(image: Image.Image) -> str: Performs OCR on a given image and returns the extracted text.
    """

    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    @staticmethod
    def perform_ocr(image: Image.Image) -> str:
        """
        Performs OCR on a given image and returns the extracted text.

        Args:
            image (Image.Image): The image to perform OCR on.

        Returns:
            str: The text extracted from the image.
        """
        return pytesseract.image_to_string(image)
