from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, files

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload.router)
app.include_router(files.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Document Upload Platform API"}