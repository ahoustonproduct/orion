"use client";

import { useState } from "react";

interface ConfidenceRatingProps {
  lessonTitle: string;
  onRate: (rating: number) => void;
}

const LABELS: Record<number, { text: string; color: string; bg: string }> = {
  1: { text: "Lost — I need to revisit this", color: "text-red-400", bg: "bg-red-500/20 border-red-500/50" },
  2: { text: "Shaky — I sort of get it", color: "text-orange-400", bg: "bg-orange-500/20 border-orange-500/50" },
  3: { text: "Okay — I get the basics", color: "text-yellow-400", bg: "bg-yellow-500/20 border-yellow-500/50" },
  4: { text: "Good — mostly confident", color: "text-blue-400", bg: "bg-blue-500/20 border-blue-500/50" },
  5: { text: "Solid — totally got it", color: "text-green-400", bg: "bg-green-500/20 border-green-500/50" },
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
    <div className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl p-5 space-y-4">
      <div>
        <p className="text-sm font-semibold text-[#e2e8f0]">How confident do you feel about this?</p>
        <p className="text-xs text-[#64748b] mt-0.5">{lessonTitle}</p>
      </div>

      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            onMouseEnter={() => setHovered(n)}
            onMouseLeave={() => setHovered(null)}
            onClick={() => handleSelect(n)}
            className={`flex-1 py-3 rounded-lg border text-lg font-bold transition-all ${
              selected === n
                ? LABELS[n].bg + " " + LABELS[n].color
                : active && active >= n
                ? "bg-[#3b82f6]/15 border-[#3b82f6]/40 text-[#3b82f6]"
                : "bg-[#0f0f1a] border-[#2d2d4a] text-[#475569] hover:border-[#3b82f6]/30"
            }`}
          >
            {n}
          </button>
        ))}
      </div>

      {active && (
        <p className={`text-sm font-medium ${LABELS[active].color} transition-all`}>
          {LABELS[active].text}
        </p>
      )}

      {selected && (
        <p className="text-xs text-[#475569]">
          Orion will use this to adjust your study plan and focus areas.
        </p>
      )}
    </div>
  );
}
