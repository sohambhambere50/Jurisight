# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Flask settings
    # SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    DEBUG = True

    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

    # OpenAI / LLM settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")

    # Summarization settings
    SUMMARY_MAX_TOKENS = 300

    # RAG (if used later)
    VECTOR_DB_PATH = os.path.join(os.getcwd(), 'vector_store')

    # Other options
    LANGUAGE = "en"
