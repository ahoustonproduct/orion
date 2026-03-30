"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Eye } from "lucide-react";

interface WorkedExampleProps {
  description: string;
  code: string;
  explanation: string;
}

export default function WorkedExample({ description, code, explanation }: WorkedExampleProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border border-[#3b82f6]/30 rounded-xl overflow-hidden bg-[#0f172a]">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-[#1a1a2e] transition-colors"
      >
        <div className="flex items-center gap-2">
          <Eye size={15} className="text-[#3b82f6]" />
          <span className="text-sm font-medium text-[#3b82f6]">Worked Example</span>
          <span className="text-xs text-[#64748b]">— see a similar problem solved first</span>
        </div>
        {expanded
          ? <ChevronUp size={15} className="text-[#64748b]" />
          : <ChevronDown size={15} className="text-[#64748b]" />}
      </button>

      {expanded && (
        <div className="border-t border-[#3b82f6]/20 px-4 py-4 space-y-4">
          <p className="text-sm text-[#94a3b8]">{description}</p>

          {/* Code block */}
          <div className="bg-[#0a0a14] rounded-lg overflow-x-auto">
            <div className="flex items-center gap-2 px-3 py-2 border-b border-[#1e293b]">
              <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f57]" />
              <div className="w-2.5 h-2.5 rounded-full bg-[#febc2e]" />
              <div className="w-2.5 h-2.5 rounded-full bg-[#28c840]" />
              <span className="text-[#475569] text-xs ml-1">example.py</span>
            </div>
            <pre className="p-4 text-sm text-[#e2e8f0] font-mono leading-relaxed overflow-x-auto">
              <code>{code}</code>
            </pre>
          </div>

          {/* Step-by-step explanation */}
          <div className="space-y-1">
            <p className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider">How it works:</p>
            <p className="text-sm text-[#cbd5e1] leading-relaxed whitespace-pre-line">{explanation}</p>
          </div>
        </div>
      )}
    </div>
  );
}
