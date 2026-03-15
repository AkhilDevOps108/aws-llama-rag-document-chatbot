import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ingest_pipeline import process_document
from llm_service import ask_llm
from retriever import search
from s3_service import download_from_s3, list_s3_files, upload_bytes_to_s3

app = FastAPI()

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")

    file_bytes = await file.read()
    upload_bytes_to_s3(file_bytes, file.filename)

    local_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    download_from_s3(file.filename, local_file_path)
    process_document(local_file_path)

    return {"message": "uploaded to S3", "filename": file.filename}


@app.get("/files")
def list_files():
    return list_s3_files()


@app.post("/chat")
def chat(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    context = search(question)
    answer = ask_llm(question, context)

    return {"answer": answer, "context": context}
