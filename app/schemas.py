from pydantic import BaseModel
from typing import List

class PDFUpload(BaseModel):
    """
    PDFUpload represents the data structure for uploading a PDF file.

    Attributes:
        file_path (str): The file path of the PDF to be uploaded.
    """
    file_path: str

class TableContent(BaseModel):
    """
    TableContent represents the content of a table extracted from a PDF.

    Attributes:
        table_index (int): The index of the table within the PDF.
        content (str): The textual content of the table.
        summary (str): A summary of the table's content.
    """
    table_index: int
    content: str
    summary: str

class ExtractTablesResponse(BaseModel):
    """
    ExtractTablesResponse represents the response structure for table extraction from a PDF.

    Attributes:
        message (str): A message indicating the status of the table extraction.
        num_tables (int): The number of tables extracted from the PDF.
        tables (List[TableContent]): A list of extracted table contents.
    """
    message: str
    num_tables: int
    tables: List[TableContent]
