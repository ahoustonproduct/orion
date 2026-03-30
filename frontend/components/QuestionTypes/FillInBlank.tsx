"use client";

import { useState } from "react";
import { CheckCircle, XCircle } from "lucide-react";

interface Props {
  question: string;
  template: string;
  answer: string;
  explanation: string;
  onCorrect: () => void;
}

export default function FillInBlank({ question, template, answer, explanation, onCorrect }: Props) {
  const [input, setInput] = useState("");
  const [revealed, setRevealed] = useState(false);
  const [correct, setCorrect] = useState(false);

  const handleSubmit = () => {
    if (revealed) return;
    const isCorrect = input.trim().toLowerCase() === answer.trim().toLowerCase();
    setCorrect(isCorrect);
    setRevealed(true);
    if (isCorrect) onCorrect();
  };

  const displayCode = template.replace("___", `[${input || "___"}]`);

  return (
    <div className="space-y-3">
      <p className="text-text-primary font-medium">{question}</p>

      <div className="bg-[#0f0f1a] border border-border rounded-lg p-3 font-mono text-sm text-cyan-DEFAULT">
        <pre className="whitespace-pre-wrap">{displayCode}</pre>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          disabled={revealed}
          placeholder="Type your answer..."
          className="flex-1 bg-surface-2 border border-border rounded-lg px-3 py-2 text-sm text-text-primary outline-none focus:border-accent font-mono disabled:opacity-60"
        />
        <button
          onClick={handleSubmit}
          disabled={revealed || !input.trim()}
          className="px-4 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Check
        </button>
      </div>

      {revealed && (
        <div className={`flex items-start gap-2 text-xs rounded-lg px-4 py-3 border animate-fade-in ${
          correct ? "bg-success/10 border-success text-success" : "bg-error/10 border-error text-error"
        }`}>
          {correct ? <CheckCircle size={14} className="mt-0.5 shrink-0" /> : <XCircle size={14} className="mt-0.5 shrink-0" />}
          <div>
            {!correct && <p className="mb-1 font-medium">Correct answer: <code className="font-mono">{answer}</code></p>}
            <p className="text-text-secondary">{explanation}</p>
          </div>
        </div>
      )}
    </div>
  );
}
