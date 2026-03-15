import { useState } from "react";

import type { ChatResponse } from "../services/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatResponse["sources"];
}

interface ChatInterfaceProps {
  isLoading: boolean;
  onAsk: (question: string) => Promise<ChatResponse>;
}

function ChatInterface({ isLoading, onAsk }: ChatInterfaceProps) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Ask a question about your indexed documents. I’ll retrieve the best chunks from Qdrant and answer with Ollama."
    }
  ]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim()) {
      return;
    }

    const currentQuestion = question.trim();
    setQuestion("");
    setMessages((existing) => [...existing, { role: "user", content: currentQuestion }]);

    try {
      const response = await onAsk(currentQuestion);
      setMessages((existing) => [
        ...existing,
        { role: "assistant", content: response.answer, sources: response.sources }
      ]);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to get an answer right now.";
      setMessages((existing) => [...existing, { role: "assistant", content: message }]);
    }
  }

  return (
    <section className="rounded-[28px] border border-slate-200 bg-white px-6 py-6 shadow-card">
      <div className="mb-5">
        <h2 className="font-display text-2xl text-ink">Chat With Documents</h2>
        <p className="mt-2 text-sm text-slate-600">
          Questions are embedded, matched against the top five chunks, and sent to your
          local Llama runtime.
        </p>
      </div>

      <div className="flex h-[28rem] flex-col rounded-[24px] bg-slate-950 p-4 text-white">
        <div className="flex-1 space-y-4 overflow-y-auto pr-1">
          {messages.map((message, index) => (
            <article
              key={`${message.role}-${index}`}
              className={`max-w-[90%] rounded-3xl px-4 py-3 text-sm leading-6 ${
                message.role === "user"
                  ? "ml-auto bg-coral text-white"
                  : "bg-white/10 text-slate-100"
              }`}
            >
              <p>{message.content}</p>
              {message.sources && message.sources.length > 0 ? (
                <div className="mt-3 flex flex-wrap gap-2">
                  {message.sources.map((source, sourceIndex) => (
                    <span
                      key={`${source.document_name}-${sourceIndex}`}
                      className="rounded-full border border-white/15 bg-white/5 px-3 py-1 text-xs text-slate-200"
                    >
                      {source.document_name} · page {source.page_number ?? "n/a"}
                    </span>
                  ))}
                </div>
              ) : null}
            </article>
          ))}
        </div>

        <form className="mt-4 flex gap-3" onSubmit={handleSubmit}>
          <input
            className="flex-1 rounded-full border border-white/15 bg-white/10 px-5 py-3 text-sm text-white outline-none placeholder:text-slate-400"
            placeholder="Ask about policy clauses, pricing terms, or onboarding steps..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />
          <button
            className="rounded-full bg-brand px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-slate-500"
            disabled={isLoading}
            type="submit"
          >
            {isLoading ? "Thinking..." : "Send"}
          </button>
        </form>
      </div>
    </section>
  );
}

export default ChatInterface;

