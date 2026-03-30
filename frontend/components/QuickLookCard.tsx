"use client";

import { useState } from "react";
import { Zap, X } from "lucide-react";
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
      <div className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-2xl w-full max-w-md shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-[#2d2d4a]">
          <div className="flex items-center gap-2">
            <Zap size={15} className="text-[#06b6d4]" />
            <span className="text-sm font-semibold text-[#e2e8f0]">Quick Look</span>
          </div>
          <button onClick={onClose} className="text-[#64748b] hover:text-[#e2e8f0] transition-colors">
            <X size={16} />
          </button>
        </div>

        <div className="p-5 space-y-4">
          <div>
            <p className="text-xs text-[#64748b] uppercase tracking-wider mb-1">Lesson</p>
            <p className="font-semibold text-[#e2e8f0]">{lessonTitle}</p>
            {progress && (
              <div className="mt-1">
                <StarRating stars={progress.stars} size="sm" />
              </div>
            )}
          </div>

          {/* Key syntax */}
          <div>
            <p className="text-xs text-[#64748b] uppercase tracking-wider mb-2">Key Syntax</p>
            <div className="space-y-1.5">
              {keySyntax.map((s, i) => (
                <div
                  key={i}
                  className="bg-[#0f0f1a] border border-[#2d2d4a] rounded-lg px-3 py-2 font-mono text-sm text-[#06b6d4]"
                >
                  {s}
                </div>
              ))}
            </div>
          </div>

          {/* Notes */}
          {notes && (
            <div>
              <p className="text-xs text-[#64748b] uppercase tracking-wider mb-1">Remember</p>
              <p className="text-sm text-[#94a3b8] leading-relaxed">{notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
