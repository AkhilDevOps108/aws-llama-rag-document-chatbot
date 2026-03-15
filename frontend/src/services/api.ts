import axios from "axios";

export interface DocumentRecord {
  name: string;
  size: number;
  uploaded_at: string;
  s3_key: string;
}

export interface UploadResponse {
  message: string;
  file_name: string;
  s3_key: string;
  chunks_indexed: number;
}

export interface ChatSource {
  document_name: string;
  page_number?: number | null;
  score: number;
  text: string;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"
});

export async function fetchDocuments() {
  const response = await api.get<DocumentRecord[]>("/files");
  return response.data;
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post<UploadResponse>("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
  return response.data;
}

export async function sendChat(question: string) {
  const response = await api.post<ChatResponse>("/chat", { question });
  return response.data;
}
