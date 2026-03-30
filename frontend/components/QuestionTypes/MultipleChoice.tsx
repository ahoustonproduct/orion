"use client";

import { useState } from "react";
import { CheckCircle, XCircle } from "lucide-react";

interface Props {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
  onCorrect: () => void;
}

export default function MultipleChoice({ question, options, answer, explanation, onCorrect }: Props) {
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  const handleSelect = (i: number) => {
    if (revealed) return;
    setSelected(i);
    setRevealed(true);
    if (i === answer) onCorrect();
  };

  return (
    <div className="space-y-3">
      <p className="text-text-primary font-medium">{question}</p>
      <div className="space-y-2">
        {options.map((opt, i) => {
          let cls = "w-full text-left px-4 py-3 rounded-lg border transition-all text-sm ";
          if (!revealed) {
            cls += "border-border hover:border-accent hover:bg-accent/10 text-text-primary cursor-pointer";
          } else if (i === answer) {
            cls += "border-success bg-success/10 text-success";
          } else if (i === selected) {
            cls += "border-error bg-error/10 text-error";
          } else {
            cls += "border-border text-text-muted opacity-50";
          }
          return (
            <button key={i} className={cls} onClick={() => handleSelect(i)}>
              <span className="font-mono text-xs mr-2 opacity-60">{String.fromCharCode(65 + i)}.</span>
              {opt}
              {revealed && i === answer && <CheckCircle size={14} className="inline ml-2" />}
              {revealed && i === selected && i !== answer && <XCircle size={14} className="inline ml-2" />}
            </button>
          );
        })}
      </div>
      {revealed && (
        <div className="text-xs text-text-secondary bg-surface-2 rounded-lg px-4 py-2 border border-border animate-fade-in">
          {explanation}
        </div>
      )}
    </div>
  );
}
