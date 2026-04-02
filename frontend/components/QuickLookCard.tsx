"use client";

import { X, Zap } from "lucide-react";
import type { LessonProgress } from "@/lib/api";
import StarRating from "./StarRating";

interface QuickLookCardProps {
  lessonId: string;
  lessonTitle: string;
  keySyntax: string[];
  notes: string;
  progress: LessonProgress | undefined;
  onClose: () => void;
}

export default function QuickLookCard({
  lessonTitle,
  keySyntax,
  notes,
  progress,
  onClose,
}: QuickLookCardProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/60 p-4">
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl w-full max-w-md shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-[var(--color-border)]">
          <div className="flex items-center gap-2">
            <Zap size={15} className="text-[var(--color-accent)]" />
            <span className="text-sm font-semibold text-[var(--color-text-primary)]">Quick Look</span>
          </div>
          <button onClick={onClose} className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] transition-colors">
            <X size={16} />
          </button>
        </div>

        <div className="p-5 space-y-4">
          <div>
            <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Lesson</p>
            <p className="font-semibold text-[var(--color-text-primary)]">{lessonTitle}</p>
            {progress && (
              <div className="mt-1">
                <StarRating stars={progress.stars} size="sm" />
              </div>
            )}
          </div>

          {/* Key syntax */}
          <div>
            <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">Key Syntax</p>
            <div className="space-y-1.5">
              {keySyntax.map((s, i) => (
                <div
                  key={i}
                  className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 font-mono text-sm text-[var(--color-accent)]"
                >
                  {s}
                </div>
              ))}
            </div>
          </div>

          {/* Notes */}
          {notes && (
            <div>
              <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Remember</p>
              <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
