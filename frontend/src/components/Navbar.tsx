function Navbar() {
  return (
    <header className="relative overflow-hidden rounded-[28px] border border-white/70 bg-white/70 px-6 py-6 shadow-card backdrop-blur md:px-10">
      <div className="absolute inset-y-0 right-0 w-40 bg-gradient-to-l from-brand/10 to-transparent" />
      <div className="relative flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-brand">
            Enterprise RAG Workspace
          </p>
          <h1 className="font-display text-3xl text-ink md:text-5xl">
            Document Knowledge AI
          </h1>
        </div>
        <p className="max-w-xl text-sm leading-6 text-slate-600 md:text-base">
          Upload company PDFs, index them in AWS S3 and Qdrant, then chat over the
          retrieved knowledge with a locally hosted Llama model.
        </p>
      </div>
    </header>
  );
}

export default Navbar;

