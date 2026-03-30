"use client";

import { CheckCircle, Circle, Lock } from "lucide-react";
import Link from "next/link";
import type { LessonProgress } from "@/lib/api";

interface ConceptNode {
  id: string;
  label: string;
  connects_to?: string[];
}

interface ConceptMapProps {
  nodes: ConceptNode[];
  lessonProgress: Record<string, LessonProgress>;
  moduleUnlocked: boolean;
}

export default function ConceptMap({ nodes, lessonProgress, moduleUnlocked }: ConceptMapProps) {
  if (!nodes || nodes.length === 0) return null;

  return (
    <div className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl p-4 space-y-3">
      <p className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider">Concept Map</p>
      <p className="text-xs text-[#64748b]">Each lesson builds on the previous. Click any lesson to jump to it.</p>

      <div className="space-y-1.5 max-h-80 overflow-y-auto pr-1">
        {nodes.map((node, idx) => {
          const prog = lessonProgress[node.id];
          const completed = prog?.completed ?? false;
          const stars = prog?.stars ?? 0;

          return (
            <div key={node.id} className="flex items-center gap-2.5">
              {/* Connector line */}
              <div className="flex flex-col items-center w-5 shrink-0">
                {idx > 0 && <div className="w-px h-2 bg-[#2d2d4a]" />}
                <div className="shrink-0">
                  {completed ? (
                    <CheckCircle size={16} className={stars === 3 ? "text-green-400" : "text-blue-400"} />
                  ) : moduleUnlocked ? (
                    <Circle size={16} className="text-[#2d2d4a]" />
                  ) : (
                    <Lock size={14} className="text-[#2d2d4a]" />
                  )}
                </div>
              </div>

              <Link
                href={moduleUnlocked ? `/learn/${node.id}` : "#"}
                className={`flex-1 text-sm px-3 py-2 rounded-lg transition-all ${
                  completed
                    ? "bg-[#0f1a2e] border border-blue-500/20 text-[#94a3b8] hover:border-blue-500/40"
                    : moduleUnlocked
                    ? "bg-[#0f0f1a] border border-[#2d2d4a] text-[#64748b] hover:border-[#3b82f6]/30 hover:text-[#e2e8f0]"
                    : "bg-[#0f0f1a]/50 border border-[#2d2d4a]/50 text-[#475569] cursor-not-allowed"
                }`}
              >
                <span className="font-medium">{node.label}</span>
                {completed && stars > 0 && (
                  <span className="ml-2 text-yellow-400 text-xs">{"★".repeat(stars)}</span>
                )}
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
}
