"use client";

import Link from "next/link";
import { ArrowLeft, BookOpen, Lock } from "lucide-react";

export default function CreateNotebookPage() {
  return (
    <div className="max-w-xl mx-auto px-4 py-6 space-y-5">
      <Link
        href="/notebooks"
        className="inline-flex items-center gap-1.5 text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
      >
        <ArrowLeft size={13} /> Back to notebooks
      </Link>

      <div className="flex items-center gap-2">
        <BookOpen size={18} className="text-[var(--color-accent)]" />
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">New Notebook</h1>
      </div>

      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-5 space-y-4">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border)] flex items-center justify-center shrink-0">
            <Lock size={15} className="text-[var(--color-text-muted)]" />
          </div>
          <div>
            <p className="text-sm font-semibold text-[var(--color-text-primary)]">Notebook generation is disabled</p>
            <p className="mt-1 text-xs text-[var(--color-text-secondary)] leading-relaxed">
              Existing notebooks remain available, but automatic video-to-module generation is no longer part of the core app.
            </p>
          </div>
        </div>

        <Link
          href="/notebooks"
          className="inline-flex items-center justify-center px-4 py-2 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white rounded-lg text-xs font-medium transition-all"
        >
          View Notebooks
        </Link>
      </div>
    </div>
  );
}
