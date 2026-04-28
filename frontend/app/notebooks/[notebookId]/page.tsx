"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft, BookOpen, Loader2, AlertCircle,
  Clock, ChevronRight, Youtube
} from "lucide-react";
import { getUserKey } from "@/lib/user";
import {
  fetchNotebook,
  fetchProgress,
  type NotebookDetail,
  type ProgressData,
} from "@/lib/api";

export default function NotebookDetailPage() {
  const { notebookId } = useParams<{ notebookId: string }>();
  const [notebook, setNotebook] = useState<NotebookDetail | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  const load = useCallback(async () => {
    try {
      const userKey = getUserKey();
      const [nb, prog] = await Promise.all([
        fetchNotebook(userKey, notebookId),
        fetchProgress(userKey).catch(() => null),
      ]);
      setNotebook(nb);
      if (prog) setProgress(prog);
    } catch (e) {
      console.error(e);
      setErr(e instanceof Error ? e.message : "Could not load notebook.");
    } finally {
      setLoading(false);
    }
  }, [notebookId]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-6">
        <p className="text-xs text-[var(--color-text-secondary)] flex items-center gap-2">
          <Loader2 size={14} className="animate-spin" /> Loading notebook…
        </p>
      </div>
    );
  }

  if (err || !notebook) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
        <Link href="/notebooks" className="inline-flex items-center gap-1.5 text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]">
          <ArrowLeft size={13} /> Back to notebooks
        </Link>
        <p className="text-sm text-red-700">{err || "Notebook not found."}</p>
      </div>
    );
  }

  const lessons = notebook.module_data?.lessons || [];
  const completedLessonIds = new Set(
    (progress?.lessons ?? []).filter((l) => l.completed).map((l) => l.lesson_id)
  );
  const starsByLesson = new Map(
    (progress?.lessons ?? []).map((l) => [l.lesson_id, l.stars])
  );

  const isGenerating = notebook.status === "pending" || notebook.status === "generating";

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-5">
      <Link
        href="/notebooks"
        className="inline-flex items-center gap-1.5 text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
      >
        <ArrowLeft size={13} /> Back to notebooks
      </Link>

      {/* Header */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-2">
        <div className="flex items-start gap-2">
          <BookOpen size={16} className="text-[var(--color-accent)] mt-0.5 shrink-0" />
          <div className="flex-1 min-w-0">
            <h1 className="text-lg font-bold text-[var(--color-text-primary)]">{notebook.title}</h1>
            {notebook.module_data?.description && (
              <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                {notebook.module_data.description}
              </p>
            )}
          </div>
        </div>
        {notebook.source_url && (
          <a
            href={notebook.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-[11px] text-[var(--color-text-muted)] hover:text-[var(--color-accent)]"
          >
            <Youtube size={11} className="text-red-600" />
            <span className="truncate">{notebook.source_url}</span>
          </a>
        )}
      </div>

      {/* Generating state */}
      {isGenerating && (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-6 text-center space-y-3">
          <Clock size={28} className="mx-auto text-[var(--color-accent)]" />
          <p className="text-sm font-medium text-[var(--color-text-primary)]">
            Notebook generation is paused
          </p>
          <p className="text-xs text-[var(--color-text-secondary)]">
            This notebook was queued before automatic generation was disabled. Existing ready notebooks still open normally.
          </p>
        </div>
      )}

      {/* Failed state */}
      {notebook.status === "failed" && (
        <div className="bg-red-500/5 border border-red-500/30 rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <AlertCircle size={15} className="text-red-700" />
            <p className="text-sm font-semibold text-red-700">Generation failed</p>
          </div>
          {notebook.error && (
            <pre className="text-[11px] text-red-700 bg-white/40 rounded-lg p-2 whitespace-pre-wrap break-words">
              {notebook.error}
            </pre>
          )}
        </div>
      )}

      {/* Lesson list */}
      {notebook.status === "ready" && lessons.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold text-[var(--color-text-primary)]">
            {lessons.length} Lesson{lessons.length === 1 ? "" : "s"}
          </p>
          {lessons.map((lesson, idx) => {
            const done = completedLessonIds.has(lesson.id);
            const stars = starsByLesson.get(lesson.id) ?? 0;
            return (
              <Link
                key={lesson.id}
                href={`/learn/${lesson.id}`}
                className="block p-3 rounded-xl border bg-[var(--color-surface)] border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all"
              >
                <div className="flex items-start gap-3">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 ${
                    done
                      ? "bg-green-500/20 text-green-700"
                      : "bg-[var(--color-accent)]/15 text-[var(--color-accent)]"
                  }`}>
                    {done ? "✓" : idx + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm text-[var(--color-text-primary)]">
                      {lesson.title}
                    </p>
                    <div className="flex items-center gap-3 text-[11px] text-[var(--color-text-muted)] mt-1">
                      <span className="flex items-center gap-1">
                        <Clock size={10} /> ~{lesson.duration_min || 20} min
                      </span>
                      {done && stars > 0 && (
                        <span className="text-[var(--color-star)]">
                          {"★".repeat(stars)}{"☆".repeat(3 - stars)}
                        </span>
                      )}
                    </div>
                  </div>
                  <ChevronRight size={14} className="text-[var(--color-text-muted)] shrink-0 mt-1" />
                </div>
              </Link>
            );
          })}
        </div>
      )}

      {notebook.status === "ready" && lessons.length === 0 && (
        <div className="bg-[var(--color-surface)] border border-dashed border-[var(--color-border)] rounded-xl p-6 text-center space-y-2">
          <p className="text-sm text-[var(--color-text-primary)]">
            No lessons were generated.
          </p>
          <button
            disabled
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white rounded-lg text-[11px] font-medium"
          >
            Generation disabled
          </button>
        </div>
      )}
    </div>
  );
}
