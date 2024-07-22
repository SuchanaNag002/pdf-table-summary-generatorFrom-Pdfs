import tabula
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TableService:
    @staticmethod
    def extract_tables(pdf_path: str):
        try:
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            logger.info(f"Extracted {len(tables)} tables from the PDF.")
            return tables
        except Exception as e:
            if "jpype" in str(e).lower():
                logger.error("JPype is not properly installed. Please ensure Java is installed and JPype is correctly configured.")
                raise RuntimeError("JPype is not properly installed. Please ensure Java is installed and JPype is correctly configured.")
            logger.error(f"Error extracting tables: {str(e)}")
            raise e

    @staticmethod
    def clean_table(table: pd.DataFrame) -> str:
        try:
            # Remove rows and columns that are entirely empty
            table = table.dropna(how='all').dropna(axis=1, how='all')
            
            # Clean column names
            table.columns = table.columns.str.strip().str.lower()
            table.columns = [col if not col.startswith('unnamed:') else f'column_{i}' for i, col in enumerate(table.columns)]
            
            # Replace NaN with empty string
            table = table.fillna('')
            
            # Convert all data to strings using DataFrame.map instead of applymap
            table = table.map(str)
            
            # Create a string representation of the table
            table_string = table.to_string(index=False)
            
            logger.info("Table cleaned successfully.")
            return table_string
        except Exception as e:
            logger.error(f"Error cleaning table: {str(e)}")
            return f"Error cleaning table: {str(e)}"

    @staticmethod
    def process_tables(pdf_path: str):
        tables = TableService.extract_tables(pdf_path)
        cleaned_tables = []
        for i, table in enumerate(tables):
            cleaned_table = TableService.clean_table(table)
            cleaned_tables.append({
                'table_index': i + 1,
                'content': cleaned_table
            })
        return cleaned_tables