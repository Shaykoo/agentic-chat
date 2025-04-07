from langchain_ollama import OllamaEmbeddings
from app.core.config import settings

embedding_model = OllamaEmbeddings(
    model=settings.EMBEDDING_MODEL,
    base_url=settings.BASE_URL
)

def get_embedding(text: str):
    return embedding_model.embed_query(text)
