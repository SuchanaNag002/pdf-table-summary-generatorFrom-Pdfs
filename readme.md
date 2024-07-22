
---

# PDF Table Extractor

## Overview

The **PDF Table Extractor** is a tool designed to process PDF files, extract tables, and generate summaries for the extracted table contents. This project leverages advanced OCR and table extraction techniques to convert PDFs into structured data. It includes features such as table extraction, data cleaning, OCR processing, and summary generation.

## Tech Stack

- **Backend Framework**: FastAPI
- **PDF Processing**: `fitz` (PyMuPDF) for text extraction, `pdf2image` for converting PDF pages to images
- **Table Extraction**: `tabula` for reading tables from PDFs
- **OCR**: `pytesseract` for optical character recognition
- **Embeddings**: `GoogleGenerativeAIEmbeddings` for generating text embeddings and summaries
- **LLM**: `gemini-1.5-flash` for generating summaries of tabular data present in the PDF
- **Data Handling**: `pandas` for data manipulation and cleaning
- **Database**: Not used in this project
- **Deployment**: Not specified; can be deployed using any ASGI-compatible server

## Installation

### Prerequisites

Ensure you have the following software installed:

- **Python** (3.7 or higher)
- **Java** (for `tabula`)

### Setting Up the Environment

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/pdf-table-extractor.git
   cd pdf-table-extractor
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Installing Poppler

Poppler is required for PDF to image conversion. Follow the instructions for your operating system:

- **On Windows**:
  1. Download the latest Poppler release from [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases/)
  2. Extract the contents to a folder (e.g., `C:\poppler`)
  3. Add the `bin` folder to your system PATH (e.g., `C:\poppler\Library\bin`)

- **On macOS**:
  ```bash
  brew install poppler
  ```

- **On Linux**:
  ```bash
  sudo apt-get install poppler-utils
  ```

### Setting Up Tesseract

For `pytesseract`, you need to install Tesseract and configure its path:

1. **Install Tesseract**:
   - On Windows: Follow the instructions [here](https://github.com/tesseract-ocr/tesseract) for installation.
   - On macOS: `brew install tesseract`
   - On Linux: `sudo apt-get install tesseract-ocr`

2. **Configure Tesseract Path in Scripts**:
   - Follow the setup instructions in this [Stack Overflow link](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i) to ensure Tesseract is correctly set up in your environment.

## Running the Application

1. **Start the FastAPI Server**

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the FastAPI server, and you can access the API documentation at `http://127.0.0.1:8000/docs`.

2. **Upload a PDF File**

   Use the `/upload-pdf/` endpoint to upload a PDF file and receive extracted tables and their summaries.

## Static Files

For testing the application, you can use the static files provided in the project:

- **Sample PDF**: [table_pdf.pdf](app/static/table_pdf.pdf) - A sample PDF file used for testing the application's table extraction and processing capabilities.
- **FastAPI Screenshot**: [fastapi_ss_output.png](app/static/fastapi_ss_output.png) - A screenshot of the FastAPI output from processing `table_pdf.pdf`, demonstrating the application’s response.

## Usage

- **POST /upload-pdf/**: Upload a PDF file to extract tables and generate summaries.

### Example Request

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-pdf/' \
  -F 'file=@path/to/your/file.pdf'
```

### Example Response

```json
{
  "message": "PDF processed successfully",
  "num_tables": 2,
  "tables": [
    {
      "table_index": 1,
      "content": "Table content here...",
      "summary": "Summary of table 1..."
    },
    {
      "table_index": 2,
      "content": "Table content here...",
      "summary": "Summary of table 2..."
    }
  ]
}
```

## Troubleshooting

- **JPype Error**: If you encounter errors related to JPype, ensure Java is installed and properly configured.
- **Poppler Error**: Ensure Poppler is correctly installed and its binaries are added to the system PATH.

For additional support, check the project's [issue tracker](https://github.com/yourusername/pdf-table-extractor/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
