"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { BookOpen, Clock, Trash2, AlertCircle, Loader2 } from "lucide-react";
import { getUserKey } from "@/lib/user";
import {
  fetchNotebooks,
  deleteNotebook,
  type NotebookSummary,
} from "@/lib/api";

function StatusBadge({ status }: { status: NotebookSummary["status"] }) {
  const map: Record<NotebookSummary["status"], { label: string; cls: string; icon?: React.ReactNode }> = {
    ready:      { label: "Ready",       cls: "bg-green-500/15 text-green-700" },
    failed:     { label: "Failed",      cls: "bg-red-500/15 text-red-700",           icon: <AlertCircle size={11} /> },
  };
  const v = map[status];
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${v.cls}`}>
      {v.icon}
      {v.label}
    </span>
  );
}

export default function NotebooksListPage() {
  const [notebooks, setNotebooks] = useState<NotebookSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const userKey = getUserKey();
      const rows = await fetchNotebooks(userKey);
      setNotebooks(rows);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this notebook? This can't be undone.")) return;
    try {
      await deleteNotebook(getUserKey(), id);
      setNotebooks((cur) => cur.filter((n) => n.id !== id));
    } catch (e) {
      console.error(e);
      alert("Could not delete notebook.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen size={18} className="text-[var(--color-accent)]" />
          <h1 className="text-xl font-bold text-[var(--color-text-primary)]">My Notebooks</h1>
        </div>
      </div>

      <p className="text-xs text-[var(--color-text-secondary)]">
        Saved study modules imported outside the app remain available here.
      </p>

      {loading ? (
        <div className="flex items-center gap-2 text-xs text-[var(--color-text-secondary)]">
          <Loader2 size={14} className="animate-spin" /> Loading notebooks...
        </div>
      ) : notebooks.length === 0 ? (
        <div className="bg-[var(--color-surface)] border border-dashed border-[var(--color-border)] rounded-xl p-8 text-center space-y-3">
          <BookOpen size={28} className="mx-auto text-[var(--color-accent)] opacity-60" />
          <p className="text-sm font-medium text-[var(--color-text-primary)]">No notebooks yet</p>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Imported study modules will appear here.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {notebooks.map((nb) => {
            const isReady = nb.status === "ready";
            const isFailed = nb.status === "failed";
            return (
              <div
                key={nb.id}
                className="block p-4 rounded-xl border bg-[var(--color-surface)] border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-[var(--color-accent)]/15 text-[var(--color-accent)] flex items-center justify-center shrink-0">
                    <BookOpen size={14} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className="font-semibold text-sm text-[var(--color-text-primary)] truncate">
                        {nb.title || "Untitled Notebook"}
                      </p>
                      <StatusBadge status={nb.status} />
                    </div>
                    {nb.source_url && (
                      <p className="text-[11px] text-[var(--color-text-muted)] mt-1 truncate">
                        {nb.source_url}
                      </p>
                    )}
                    <div className="flex items-center gap-3 text-xs text-[var(--color-text-muted)] mt-2">
                      <span className="flex items-center gap-1"><BookOpen size={11} /> {nb.lesson_count} lessons</span>
                      {nb.created_at && (
                        <span className="flex items-center gap-1">
                          <Clock size={11} /> {new Date(nb.created_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>

                    {isFailed && nb.error && (
                      <p className="mt-2 text-[11px] text-red-700 bg-red-500/10 border border-red-500/20 rounded-lg p-2 whitespace-pre-wrap break-words">
                        {nb.error.slice(0, 300)}
                      </p>
                    )}

                    <div className="flex items-center gap-2 mt-3 flex-wrap">
                      {isReady && (
                        <Link
                          href={`/notebooks/${nb.id}`}
                          className="px-3 py-1.5 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white rounded-lg text-[11px] font-medium transition-all"
                        >
                          Open
                        </Link>
                      )}
                      <button
                        onClick={() => handleDelete(nb.id)}
                        className="flex items-center gap-1 px-3 py-1.5 text-[var(--color-text-muted)] hover:text-red-600 rounded-lg text-[11px] font-medium transition-all"
                      >
                        <Trash2 size={11} /> Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
