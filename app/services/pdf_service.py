import fitz
from pdf2image import convert_from_path

class PDFService:
    """
    PDFService provides functionalities for handling PDF files.

    Methods:
        upload_pdf(pdf_path: str) -> str: Extracts text from a PDF file and returns it as a string.
        pdf_to_images(pdf_path: str): Converts each page of a PDF file into an image.
    """

    @staticmethod
    def upload_pdf(pdf_path: str) -> str:
        """
        Extracts text from a PDF file and returns it as a single string.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The text extracted from the PDF.
        """
        pdf_document = fitz.open(pdf_path)
        text = [page.get_text() for page in pdf_document]
        pdf_document.close()
        return "\n".join(text)

    @staticmethod
    def pdf_to_images(pdf_path: str):
        """
        Converts each page of a PDF file into an image.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            list: A list of images, each representing a page of the PDF.

        Raises:
            RuntimeError: If Poppler is not installed or not in PATH.
        """
        try:
            return convert_from_path(pdf_path)
        except Exception as e:
            if "poppler" in str(e).lower():
                raise RuntimeError("Poppler is not installed or not in PATH. Please install Poppler and try again.")
            raise e
