"use client";

import { useState } from "react";
import { CheckCircle, XCircle } from "lucide-react";

interface Props {
  question: string;
  answer: boolean;
  explanation: string;
  onCorrect: () => void;
}

export default function TrueFalse({ question, answer, explanation, onCorrect }: Props) {
  const [selected, setSelected] = useState<boolean | null>(null);
  const [revealed, setRevealed] = useState(false);

  const handleSelect = (value: boolean) => {
    if (revealed) return;
    setSelected(value);
    setRevealed(true);
    if (value === answer) onCorrect();
  };

  const btn = (value: boolean, label: string) => {
    let cls = "flex-1 py-3 rounded-lg border transition-all font-medium text-sm flex items-center justify-center gap-2 ";
    if (!revealed) {
      cls += "border-border hover:border-accent hover:bg-accent/10 text-text-primary cursor-pointer";
    } else if (value === answer) {
      cls += "border-success bg-success/10 text-success";
    } else if (value === selected) {
      cls += "border-error bg-error/10 text-error";
    } else {
      cls += "border-border text-text-muted opacity-50";
    }
    return (
      <button className={cls} onClick={() => handleSelect(value)}>
        {revealed && value === answer && <CheckCircle size={14} />}
        {revealed && value === selected && value !== answer && <XCircle size={14} />}
        {label}
      </button>
    );
  };

  return (
    <div className="space-y-3">
      <p className="text-text-primary font-medium">{question}</p>
      <div className="flex gap-3">
        {btn(true, "True")}
        {btn(false, "False")}
      </div>
      {revealed && (
        <div className="text-xs text-text-secondary bg-surface-2 rounded-lg px-4 py-2 border border-border animate-fade-in">
          {explanation}
        </div>
      )}
    </div>
  );
}
