"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Sparkles, Loader2, Youtube } from "lucide-react";
import { getUserKey } from "@/lib/user";
import { createNotebook } from "@/lib/api";

export default function CreateNotebookPage() {
  const router = useRouter();
  const [sourceUrl, setSourceUrl] = useState("");
  const [title, setTitle] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) return;
    setSubmitting(true);
    setError("");
    try {
      const result = await createNotebook(getUserKey(), sourceUrl.trim(), title.trim());
      router.push(`/notebooks/${result.id}`);
    } catch (err) {
      console.error(err);
      setError(
        err instanceof Error
          ? err.message
          : "Could not start notebook generation. Make sure the backend is running."
      );
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-6 space-y-5">
      <Link
        href="/notebooks"
        className="inline-flex items-center gap-1.5 text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
      >
        <ArrowLeft size={13} /> Back to notebooks
      </Link>

      <div className="flex items-center gap-2">
        <Sparkles size={18} className="text-[var(--color-accent)]" />
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">New Notebook</h1>
      </div>

      <p className="text-xs text-[var(--color-text-secondary)]">
        Paste a YouTube URL and Orion will pull the transcript, then turn it into a full Orion module —
        concept pages, worked examples, 3+ practice questions per lesson, and a coding challenge.
      </p>

      <form
        onSubmit={handleSubmit}
        className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-4"
      >
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--color-text-primary)] flex items-center gap-1.5">
            <Youtube size={13} className="text-red-600" /> YouTube URL
            <span className="text-[var(--color-text-muted)] font-normal">(required)</span>
          </label>
          <input
            type="url"
            value={sourceUrl}
            onChange={(e) => setSourceUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            required
            className="w-full bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-xs text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-all"
          />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--color-text-primary)]">
            Title <span className="text-[var(--color-text-muted)] font-normal">(optional — Orion will infer one)</span>
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Moving Averages & RSI Explained"
            className="w-full bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-xs text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-all"
          />
        </div>

        {error && (
          <p className="text-[11px] text-red-700 bg-red-500/10 border border-red-500/20 rounded-lg p-2">
            {error}
          </p>
        )}

        <div className="flex items-center gap-2">
          <button
            type="submit"
            disabled={submitting || !sourceUrl.trim()}
            className="flex items-center gap-1.5 px-4 py-2 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            {submitting ? (
              <><Loader2 size={13} className="animate-spin" /> Starting…</>
            ) : (
              <><Sparkles size={13} /> Generate Notebook</>
            )}
          </button>
          <Link
            href="/notebooks"
            className="px-4 py-2 text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
          >
            Cancel
          </Link>
        </div>
      </form>

      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-2">
        <p className="text-xs font-semibold text-[var(--color-text-primary)]">How it works</p>
        <ol className="text-xs text-[var(--color-text-secondary)] space-y-1.5 list-decimal list-inside">
          <li>Orion fetches the video transcript via the YouTube captions API.</li>
          <li>
            Your local <code className="text-[var(--color-accent)]">orion-tutor</code> model (via Ollama)
            turns it into 3–5 structured lessons.
          </li>
          <li>Each lesson includes a concept, worked example, 3+ questions, and a coding challenge.</li>
          <li>You can study it exactly like a built-in module — progress, streaks, and stars all count.</li>
        </ol>
        <p className="text-[11px] text-[var(--color-text-muted)] pt-1">
          Generation typically takes 30–90 seconds depending on transcript length and your machine.
        </p>
      </div>
    </div>
  );
}
