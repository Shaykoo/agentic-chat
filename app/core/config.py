import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vector_store")
    HISTORY_DB_URL = os.getenv("HISTORY_DB_URL", "sqlite:///./chat_history.db")

settings = Settings()
