from fastapi import FastAPI, HTTPException
from app.api.endpoints import pdf_routes  # Import the router with the PDF-related routes

# Initialize a FastAPI application instance
app = FastAPI(title="PDF Table Extractor")  # Set the application title for documentation and identification

# Include the router that contains PDF-related endpoints
app.include_router(pdf_routes.router)
