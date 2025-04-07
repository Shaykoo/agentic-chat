from fastapi import APIRouter, UploadFile, File
from app.services.rag_service import handle_user_query, process_uploaded_files
from app.schemas.query_schema import QueryRequest

router = APIRouter()

@router.post("/query")
async def query_route(payload: QueryRequest):
    return await handle_user_query(payload.user_id, payload.query)

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    return await process_uploaded_files(files)
