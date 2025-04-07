# app/utils/mcp_context.py
from typing import List, Dict
from langchain_core.documents import Document

def build_mcp_context(
    system_prompt: str,
    user_query: str,
    retrieved_docs: List[Document],
    chat_history: List[Dict] = [],
    metadata: Dict = {}
) -> Dict:
    return {
        "system": system_prompt,
        "user_query": user_query,
        "context_documents": [doc.page_content for doc in retrieved_docs],
        "chat_history": chat_history,
        "metadata": metadata
    }
