# aws-llama-rag-document-chatbot

Production-ready starter for a document RAG platform that uploads PDFs through a React dashboard, stores them in AWS S3, indexes chunks in Qdrant, and answers questions with a locally hosted Ollama Llama model.

## Architecture

1. User uploads a PDF in the React dashboard.
2. FastAPI validates the file and stores it in `s3://rag-documents-bucket/documents/`.
3. The backend extracts PDF text with `pypdf`, chunks the content, and creates embeddings with `BAAI/bge-small-en`.
4. Chunk vectors and metadata are stored in Qdrant.
5. User questions are embedded and matched against the top five stored chunks.
6. Retrieved context is sent to Ollama at `http://localhost:11434/api/generate`.
7. The grounded answer is returned to the chat UI with cited source chunks.

## Project structure

```text
aws-llama-rag-document-chatbot/
  frontend/
  backend/
  docker/
  scripts/
  requirements.txt
  .env
  README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- AWS account with an S3 bucket
- Ollama installed locally

## Environment setup

Edit `.env` with your values:

```env
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=rag-documents-bucket
S3_DOCUMENT_PREFIX=documents/
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=documents
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
EMBEDDING_MODEL=BAAI/bge-small-en
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_ORIGIN=http://localhost:5173
```

## AWS S3 setup

1. Create an S3 bucket, for example `rag-documents-bucket`.
2. Ensure your IAM user has `s3:PutObject`, `s3:GetObject`, and `s3:ListBucket` permissions.
3. Use the `documents/` prefix or adjust `S3_DOCUMENT_PREFIX` in `.env`.
4. Keep the bucket private; the backend reads files directly through boto3.

## Run supporting services

Start Qdrant and Redis:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Or use the helper script:

```bash
bash scripts/start_services.sh
```

## Run Ollama

Start the local Ollama server:

```bash
ollama serve
```

Pull a model:

```bash
ollama pull llama3
```

You can switch to `mistral` later by changing `OLLAMA_MODEL` in `.env`.

## Run the backend

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

Start FastAPI:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Available endpoints:

- `POST /upload`
- `GET /files`
- `POST /chat`
- `GET /health`

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://localhost:5173`.

If your backend is on a different URL, add a `frontend/.env.local` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Testing the flow

1. Start Docker services.
2. Start Ollama and ensure `ollama run llama3` works locally.
3. Start the FastAPI backend.
4. Start the React frontend.
5. Upload a PDF from the dashboard.
6. Confirm the file appears in the document list.
7. Ask a question in the chat panel and verify the answer cites the relevant source pages.

## Scalability notes

- The service boundaries in `backend/app/services` are designed so you can swap local Ollama for GPU inference later.
- Qdrant can move from local Docker to a managed cluster with configuration changes only.
- Upload, ingestion, and chat routes can be split into separate workers or Kubernetes deployments as traffic grows.
- Redis is included so you can add background queues or caching without redesigning the base layout.

## Operational notes

- The first backend start may be slower because `sentence-transformers` downloads the embedding model.
- The upload route currently processes PDFs inline for clarity; move ingestion to a queue worker for higher throughput.
- If a PDF contains only scanned images, OCR should be added before chunking.
