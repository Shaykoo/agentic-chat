from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.core.config import settings

def get_chat_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string=settings.HISTORY_DB_URL
    )
