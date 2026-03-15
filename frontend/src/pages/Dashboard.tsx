import axios from "axios";
import { useEffect, useState } from "react";

import ChatInterface from "../components/ChatInterface";
import DocumentTable from "../components/DocumentTable";
import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import {
  fetchDocuments,
  sendChat,
  uploadDocument,
  type ChatResponse,
  type DocumentRecord
} from "../services/api";

function Dashboard() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [isDocumentsLoading, setIsDocumentsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  async function loadDocuments() {
    setIsDocumentsLoading(true);
    try {
      const nextDocuments = await fetchDocuments();
      setDocuments(nextDocuments);
    } catch (error) {
      setStatusMessage(extractApiError(error, "Failed to load documents."));
    } finally {
      setIsDocumentsLoading(false);
    }
  }

  useEffect(() => {
    void loadDocuments();
  }, []);

  async function handleUpload(file: File) {
    setIsUploading(true);
    setStatusMessage(null);

    try {
      const response = await uploadDocument(file);
      setStatusMessage(
        `${response.file_name} indexed successfully with ${response.chunks_indexed} chunks.`
      );
      await loadDocuments();
    } catch (error) {
      setStatusMessage(extractApiError(error, "Upload failed."));
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAsk(question: string): Promise<ChatResponse> {
    setIsChatLoading(true);
    try {
      return await sendChat(question);
    } catch (error) {
      throw new Error(extractApiError(error, "Chat request failed."));
    } finally {
      setIsChatLoading(false);
    }
  }

  return (
    <main className="min-h-screen px-4 py-6 md:px-8 md:py-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <Navbar />

        {statusMessage ? (
          <div className="rounded-2xl border border-brand/20 bg-white/80 px-5 py-4 text-sm text-slate-700 shadow-card">
            {statusMessage}
          </div>
        ) : null}

        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <div className="space-y-6">
            <UploadBox isUploading={isUploading} onUpload={handleUpload} />
            <DocumentTable documents={documents} loading={isDocumentsLoading} />
          </div>
          <ChatInterface isLoading={isChatLoading} onAsk={handleAsk} />
        </div>
      </div>
    </main>
  );
}

function extractApiError(error: unknown, fallbackMessage: string) {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string") {
      return detail;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return fallbackMessage;
}

export default Dashboard;
