import type { DocumentRecord } from "../services/api";

interface DocumentTableProps {
  documents: DocumentRecord[];
  loading: boolean;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function formatSize(size: number) {
  if (size < 1024) {
    return `${size} B`;
  }
  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`;
  }
  return `${(size / (1024 * 1024)).toFixed(2)} MB`;
}

function DocumentTable({ documents, loading }: DocumentTableProps) {
  return (
    <section className="rounded-[28px] border border-slate-200 bg-white px-6 py-6 shadow-card">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="font-display text-2xl text-ink">Document List</h2>
          <p className="mt-2 text-sm text-slate-600">
            S3-backed inventory of every uploaded document.
          </p>
        </div>
        <div className="rounded-full bg-sand px-4 py-2 text-sm font-semibold text-coral">
          {documents.length} indexed
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-y-3">
          <thead>
            <tr className="text-left text-xs uppercase tracking-[0.2em] text-slate-500">
              <th className="pb-2">Name</th>
              <th className="pb-2">Size</th>
              <th className="pb-2">Uploaded</th>
              <th className="pb-2">S3 Key</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td className="rounded-2xl bg-slate-50 px-4 py-6 text-sm text-slate-500" colSpan={4}>
                  Loading documents...
                </td>
              </tr>
            ) : documents.length === 0 ? (
              <tr>
                <td className="rounded-2xl bg-slate-50 px-4 py-6 text-sm text-slate-500" colSpan={4}>
                  No PDFs uploaded yet.
                </td>
              </tr>
            ) : (
              documents.map((document) => (
                <tr key={document.s3_key} className="rounded-2xl bg-slate-50 text-sm text-slate-700">
                  <td className="rounded-l-2xl px-4 py-4 font-medium text-ink">{document.name}</td>
                  <td className="px-4 py-4">{formatSize(document.size)}</td>
                  <td className="px-4 py-4">{formatDate(document.uploaded_at)}</td>
                  <td className="rounded-r-2xl px-4 py-4 text-xs text-slate-500">{document.s3_key}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default DocumentTable;

