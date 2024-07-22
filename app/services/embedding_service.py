import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
from faiss import IndexFlatL2
import logging

# Initialize logger for logging errors and information
logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    EmbeddingService provides functionalities for generating embeddings and handling table content.

    Attributes:
        model (GoogleGenerativeAIEmbeddings): The embedding model initialized with the provided API key.

    Methods:
        __init__(api_key): Initializes the EmbeddingService with the given API key.
        create_embeddings(texts): Generates embeddings for a list of texts.
        create_embeddings_for_tables(tables, api_key): Generates embeddings for table contents and creates an FAISS index.
        summarize_table_content(table_text): Generates a summary for a given table's content.
    """
    
    def __init__(self, api_key):
        """
        Initializes the EmbeddingService with the given API key and configures the embedding model.

        Args:
            api_key (str): The API key for accessing Google Generative AI services.
        """
        # Configure the Google Generative AI with the provided API key
        genai.configure(api_key=api_key)
        # Initialize the embedding model using the API key
        self.model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

    def create_embeddings(self, texts):
        """
        Generates embeddings for a list of texts.

        Args:
            texts (list of str): A list of texts to generate embeddings for.

        Returns:
            list: A list of embeddings corresponding to the input texts.
        """
        embeddings = []
        for text in texts:
            try:
                # Generate embedding for the given text using the specified model
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document",
                )
                # Append the generated embedding to the embeddings list
                embeddings.append(result['embedding'])
            except Exception as e:
                # Log any errors that occur during embedding generation
                logger.error(f"Error generating embedding: {str(e)}")
                # Append a default embedding in case of an error
                embeddings.append([0.0] * 768)
        return embeddings

    @staticmethod
    def create_embeddings_for_tables(tables, api_key):
        """
        Generates embeddings for table contents and creates an FAISS index for similarity search.

        Args:
            tables (list): A list of table objects to generate embeddings for.
            api_key (str): The API key for accessing Google Generative AI services.

        Returns:
            tuple: A FAISS index for the table embeddings and a list of table texts.
        """
        # Initialize the EmbeddingService with the provided API key
        embedding_service = EmbeddingService(api_key)
        # Convert each table to its string representation
        table_texts = [table.to_string() for table in tables]
        # Generate embeddings for the table texts
        embeddings = embedding_service.create_embeddings(table_texts)
        
        # Determine the dimension of the embeddings (assumed from the first embedding)
        dimension = len(embeddings[0])
        # Create a FAISS index for L2 (Euclidean) distance
        index = IndexFlatL2(dimension)
        # Add the embeddings to the FAISS index
        index.add(np.array(embeddings, dtype=np.float32))
        
        return index, table_texts

    @staticmethod
    def summarize_table_content(table_text):
        """
        Generates a summary for a given table's content.

        Args:
            table_text (str): The text content of the table to summarize.

        Returns:
            str: A summary of the table's content.
        """
        try:
            # Check if the table text is empty or only contains whitespace
            if not table_text.strip():
                return "The table is empty."

            # Initialize the generative model for summarization
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            # Generate the summary for the table content
            response = model.generate_content(
                f"Summarize the following table content:\n\n{table_text}\n\nSummary:",
                generation_config=genai.GenerationConfig(
                    temperature=0.2,  # Controls the randomness of the output
                    max_output_tokens=1000  # Maximum number of tokens in the generated output
                )
            )
            return response.text
        except Exception as e:
            # Log any errors that occur during summary generation
            logger.error(f"Error generating summary: {str(e)}")
            return f"Unable to generate summary. Error: {str(e)}"
