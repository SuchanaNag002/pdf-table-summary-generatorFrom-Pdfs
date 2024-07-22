from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.pdf_service import PDFService
from app.services.table_service import TableService
from app.services.embedding_service import EmbeddingService
from app.services.ocr_service import OCRService
from app.schemas import ExtractTablesResponse, TableContent
from app.config import Settings, settings
import tempfile
import os
import logging

# Create a new APIRouter instance for handling routes
router = APIRouter()
# Initialize logger for logging errors and information
logger = logging.getLogger(__name__)

@router.post("/upload-pdf/", response_model=ExtractTablesResponse)
async def upload_pdf(file: UploadFile = File(...), settings: Settings = Depends(lambda: settings)):
    """
    Endpoint to upload a PDF file, process it to extract tables, and generate summaries for the table contents.

    Args:
        file (UploadFile): The uploaded PDF file.
        settings (Settings): Application settings.

    Returns:
        ExtractTablesResponse: A response containing a message, number of tables, and the table contents with summaries.
    """
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        # Write the uploaded file's content to the temporary file
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Step 1: Extract text from PDF 
        pdf_text = PDFService.upload_pdf(temp_file_path)

        # Step 2: Convert PDF to images
        try:
            images = PDFService.pdf_to_images(temp_file_path)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

        # Step 3: Perform OCR
        ocr_results = [OCRService.perform_ocr(image) for image in images]

        # Step 4: Extract tables
        tables = TableService.extract_tables(temp_file_path)

        # Step 5: Clean tables
        cleaned_tables = [TableService.clean_table(table) for table in tables]

        # Initialize an empty list to store table contents with summaries
        table_contents = []
        for i, cleaned_table in enumerate(cleaned_tables):
            if isinstance(cleaned_table, str):
                # Generate a summary for the table content using EmbeddingService
                summary = EmbeddingService.summarize_table_content(cleaned_table)
                # Create a TableContent instance and append it to the table_contents list
                table_contents.append(
                    TableContent(
                        table_index=i + 1,
                        content=cleaned_table,
                        summary=summary
                    )
                )
            else:
                logger.error(f"Invalid table format: {cleaned_table}")
                raise HTTPException(status_code=500, detail="Invalid table format encountered.")

        # Return a response with the extracted table information
        return ExtractTablesResponse(
            message="PDF processed successfully",
            num_tables=len(table_contents),
            tables=table_contents
        )
    except Exception as e:
        # Log any errors that occur during PDF processing
        logger.error(f"Error processing PDF: {str(e)}")
        # Raise an HTTPException with status code 500 if an error occurs
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    finally:
        # Ensure the temporary file is deleted after processing
        os.unlink(temp_file_path)
