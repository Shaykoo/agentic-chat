from typing import List
import os
import tempfile
import logging
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from app.services.embedding_service import embedding_model
from app.core.config import settings
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from app.utils.mcp_context import build_mcp_context

logger = logging.getLogger(__name__)

def init_vector_store():
    vector_store_path = os.path.join(settings.VECTOR_DB_PATH, "index.faiss")
    if os.path.exists(vector_store_path):
        return FAISS.load_local(
            settings.VECTOR_DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    else:
        dummy_doc = Document(page_content="init", metadata={})
        vs = FAISS.from_documents([dummy_doc], embedding_model)
        # No need to delete any doc
        return vs


vector_store = init_vector_store()

def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])

def retrieve_context(query: str):
    results = vector_store.similarity_search(query, k=5)
    return format_docs(results)

# async def handle_user_query(user_id: str, query: str):
#     logger.info(f"Handling query for user {user_id}")
#     context = retrieve_context(query)
#     llm = ChatOllama(model="deepseek-r1:8b", base_url=settings.BASE_URL)
#     prompt = f"Context:\n{context}\n\nQuestion: {query}"
#     return {
#         "response": llm.invoke(prompt),
#         "used_prompt": prompt
#     }

async def handle_user_query(user_id: str, query: str):
    logger.info(f"Handling query for user {user_id}")
    
    # Retrieve context docs
    docs = vector_store.similarity_search(query, k=5)
    context = format_docs(docs)

    # Build MCP-style context
    mcp_context = build_mcp_context(
        system_prompt="You are a helpful assistant.",
        user_query=query,
        retrieved_docs=docs,
        chat_history=[],  # You could fill this with memory later
        metadata={"user_id": user_id}
    )

    # Use context to construct final prompt
    llm = ChatOllama(model="deepseek-r1:8b", base_url=settings.BASE_URL)
    prompt = f"""{mcp_context['system']}

Context:
{context}

User: {query}
"""
    return {
        "response": llm.invoke(prompt),
        "used_prompt": prompt,
        "debug_context": mcp_context 
    }

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(docs)

async def process_uploaded_files(files: List):
    docs = []
    for uploaded_file in files:
        logger.info(f"Processing {uploaded_file.filename}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await uploaded_file.read())
            temp_path = tmp.name

        loader = PyMuPDFLoader(temp_path)
        docs.extend(loader.load())
        os.remove(temp_path)

    chunks = split_documents(docs)
    vector_store.add_documents(chunks)
    vector_store.save_local(settings.VECTOR_DB_PATH)

    return {"message": "Files processed and indexed."}
