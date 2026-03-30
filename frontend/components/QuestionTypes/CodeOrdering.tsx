"use client";

import { useState } from "react";
import { GripVertical, CheckCircle } from "lucide-react";

interface Props {
  question: string;
  lines: string[];
  answer: number[];
  explanation: string;
  onCorrect: () => void;
}

export default function CodeOrdering({ question, lines, answer, explanation, onCorrect }: Props) {
  const [order, setOrder] = useState(() =>
    [...lines].map((line, i) => ({ id: i, text: line })).sort(() => Math.random() - 0.5)
  );
  const [revealed, setRevealed] = useState(false);
  const [correct, setCorrect] = useState(false);
  const [dragging, setDragging] = useState<number | null>(null);

  const handleCheck = () => {
    const currentOrder = order.map((item) => item.id);
    const isCorrect = JSON.stringify(currentOrder) === JSON.stringify(answer);
    setCorrect(isCorrect);
    setRevealed(true);
    if (isCorrect) onCorrect();
  };

  const moveUp = (index: number) => {
    if (index === 0) return;
    const newOrder = [...order];
    [newOrder[index - 1], newOrder[index]] = [newOrder[index], newOrder[index - 1]];
    setOrder(newOrder);
  };

  const moveDown = (index: number) => {
    if (index === order.length - 1) return;
    const newOrder = [...order];
    [newOrder[index], newOrder[index + 1]] = [newOrder[index + 1], newOrder[index]];
    setOrder(newOrder);
  };

  const correctOrder = answer.map((i) => lines[i]);

  return (
    <div className="space-y-3">
      <p className="text-text-primary font-medium">{question}</p>

      <div className="space-y-1">
        {order.map((item, i) => (
          <div
            key={item.id}
            className={`flex items-center gap-2 bg-surface-2 border rounded-lg px-3 py-2 font-mono text-sm group transition-all ${
              revealed
                ? correct
                  ? "border-success text-success"
                  : "border-border text-text-muted"
                : "border-border hover:border-accent text-cyan-DEFAULT"
            }`}
          >
            <GripVertical size={14} className="text-text-muted shrink-0" />
            <code className="flex-1">{item.text}</code>
            {!revealed && (
              <div className="flex flex-col gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                <button onClick={() => moveUp(i)} className="text-text-muted hover:text-accent text-xs leading-none">▲</button>
                <button onClick={() => moveDown(i)} className="text-text-muted hover:text-accent text-xs leading-none">▼</button>
              </div>
            )}
          </div>
        ))}
      </div>

      {!revealed && (
        <button
          onClick={handleCheck}
          className="px-4 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-all"
        >
          Check Order
        </button>
      )}

      {revealed && !correct && (
        <div className="space-y-2 animate-fade-in">
          <p className="text-xs text-error font-medium">Correct order:</p>
          <div className="space-y-1">
            {correctOrder.map((line, i) => (
              <div key={i} className="flex items-center gap-2 bg-success/10 border border-success rounded-lg px-3 py-2">
                <CheckCircle size={12} className="text-success shrink-0" />
                <code className="font-mono text-sm text-success">{line}</code>
              </div>
            ))}
          </div>
        </div>
      )}

      {revealed && (
        <div className="text-xs text-text-secondary bg-surface-2 rounded-lg px-4 py-2 border border-border animate-fade-in">
          {explanation}
        </div>
      )}
    </div>
  );
}
