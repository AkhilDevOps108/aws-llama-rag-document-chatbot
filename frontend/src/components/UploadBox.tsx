import { useRef, useState } from "react";

interface UploadBoxProps {
  isUploading: boolean;
  onUpload: (file: File) => Promise<void>;
}

function UploadBox({ isUploading, onUpload }: UploadBoxProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  async function handleSubmit() {
    if (!selectedFile) {
      return;
    }
    await onUpload(selectedFile);
    setSelectedFile(null);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  }

  return (
    <section className="rounded-[28px] border border-slate-200 bg-white px-6 py-6 shadow-card">
      <div className="mb-5">
        <h2 className="font-display text-2xl text-ink">Upload PDF</h2>
        <p className="mt-2 text-sm text-slate-600">
          Files are stored in S3, chunked, embedded with BGE, and indexed into
          Qdrant automatically.
        </p>
      </div>

      <label className="flex min-h-48 cursor-pointer flex-col items-center justify-center rounded-[24px] border-2 border-dashed border-brand/35 bg-mist/60 px-6 text-center transition hover:border-brand hover:bg-mist">
        <span className="mb-2 text-lg font-semibold text-ink">
          Drop a PDF here or click to browse
        </span>
        <span className="text-sm text-slate-500">
          Recommended for reports, policies, and internal documentation
        </span>
        <input
          ref={inputRef}
          className="hidden"
          type="file"
          accept="application/pdf"
          onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
        />
      </label>

      <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-h-6 text-sm text-slate-600">
          {selectedFile ? `Selected: ${selectedFile.name}` : "No file selected yet."}
        </div>
        <button
          className="rounded-full bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
          disabled={!selectedFile || isUploading}
          onClick={handleSubmit}
        >
          {isUploading ? "Uploading..." : "Upload and Index"}
        </button>
      </div>
    </section>
  );
}

export default UploadBox;

