"use client";

import { useState } from "react";

interface ConfidenceRatingProps {
  lessonTitle: string;
  onRate: (rating: number) => void;
}

const LABELS: Record<number, { text: string; color: string; bg: string }> = {
  1: {
    text: "Lost - I need to revisit this",
    color: "text-[var(--color-error)]",
    bg: "bg-[var(--color-error)]/10 border-[var(--color-error)]/40",
  },
  2: {
    text: "Shaky - I can follow parts of it",
    color: "text-[var(--color-warning)]",
    bg: "bg-[var(--color-warning)]/10 border-[var(--color-warning)]/40",
  },
  3: {
    text: "Developing - I understand the main idea",
    color: "text-[var(--color-star)]",
    bg: "bg-[var(--color-star)]/10 border-[var(--color-star)]/40",
  },
  4: {
    text: "Ready - I can apply it with notes",
    color: "text-[var(--color-accent)]",
    bg: "bg-[var(--color-accent)]/10 border-[var(--color-accent)]/40",
  },
  5: {
    text: "Solid - I can explain and reuse it",
    color: "text-[var(--color-success)]",
    bg: "bg-[var(--color-success)]/10 border-[var(--color-success)]/40",
  },
};

export default function ConfidenceRating({ lessonTitle, onRate }: ConfidenceRatingProps) {
  const [hovered, setHovered] = useState<number | null>(null);
  const [selected, setSelected] = useState<number | null>(null);

  const active = hovered ?? selected;

  function handleSelect(rating: number) {
    setSelected(rating);
    onRate(rating);
  }

  return (
    <div className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-xl p-3">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--color-text-muted)]">
            Confidence check
          </p>
          <p className="text-xs text-[var(--color-text-secondary)] truncate">{lessonTitle}</p>
        </div>

        <div className="flex gap-1.5 sm:min-w-64">
          {[1, 2, 3, 4, 5].map((n) => (
            <button
              key={n}
              onMouseEnter={() => setHovered(n)}
              onMouseLeave={() => setHovered(null)}
              onClick={() => handleSelect(n)}
              aria-label={`Confidence ${n}`}
              className={`h-8 flex-1 rounded-lg border text-sm font-semibold transition-all ${
                selected === n
                  ? `${LABELS[n].bg} ${LABELS[n].color}`
                  : active && active >= n
                    ? "bg-[var(--color-accent)]/10 border-[var(--color-accent)]/30 text-[var(--color-accent)]"
                    : "bg-[var(--color-surface)] border-[var(--color-border)] text-[var(--color-text-muted)] hover:border-[var(--color-accent)]/40"
              }`}
            >
              {n}
            </button>
          ))}
        </div>
      </div>

      {active && (
        <p className={`mt-2 text-xs font-medium ${LABELS[active].color} transition-all`}>
          {LABELS[active].text}
        </p>
      )}

      {selected && (
        <p className="mt-1 text-xs text-[var(--color-text-muted)]">
          Orion will use this to adjust your study plan and focus areas.
        </p>
      )}
    </div>
  );
}
