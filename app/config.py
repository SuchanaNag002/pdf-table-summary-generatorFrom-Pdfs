import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings class holds the configuration settings for the application.

    Attributes:
        API_V1_STR (str): The base URL for version 1 of the API.
        PROJECT_NAME (str): The name of the project.
        GOOGLE_API_KEY (str): The Google API key, retrieved from environment variables.
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PDF Table Extractor"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

# Initialize the settings
settings = Settings()
