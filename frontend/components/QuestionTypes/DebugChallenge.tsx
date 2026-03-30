"use client";

import { useState } from "react";
import { Bug, CheckCircle, XCircle } from "lucide-react";

interface DebugChallengeProps {
  question: string;
  brokenCode: string;
  answer: string;
  explanation: string;
  onAnswer: (correct: boolean) => void;
}

export default function DebugChallenge({
  question,
  brokenCode,
  answer,
  explanation,
  onAnswer,
}: DebugChallengeProps) {
  const [userAnswer, setUserAnswer] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [correct, setCorrect] = useState(false);

  function handleSubmit() {
    const isCorrect = userAnswer.trim().toLowerCase() === answer.trim().toLowerCase();
    setCorrect(isCorrect);
    setSubmitted(true);
    onAnswer(isCorrect);
  }

  return (
    <div className="space-y-4">
      {/* Question */}
      <div className="flex items-start gap-2">
        <Bug size={16} className="text-orange-400 mt-0.5 shrink-0" />
        <p className="text-sm text-[#e2e8f0] leading-relaxed">{question}</p>
      </div>

      {/* Broken code display */}
      <div className="bg-[#0a0a14] rounded-lg overflow-hidden">
        <div className="flex items-center gap-2 px-3 py-2 border-b border-[#1e293b] bg-orange-500/5">
          <Bug size={12} className="text-orange-400" />
          <span className="text-xs text-orange-400 font-medium">Broken Code — find the bug</span>
        </div>
        <pre className="p-4 text-sm text-[#e2e8f0] font-mono leading-relaxed overflow-x-auto">
          <code>{brokenCode}</code>
        </pre>
      </div>

      {/* Answer input */}
      {!submitted ? (
        <div className="space-y-2">
          <label className="text-xs text-[#94a3b8]">
            What is wrong? Type the corrected expression or keyword:
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && userAnswer.trim() && handleSubmit()}
              placeholder="Type your fix here..."
              className="flex-1 bg-[#0f0f1a] border border-[#2d2d4a] rounded-lg px-3 py-2 text-sm text-[#e2e8f0] placeholder-[#475569] font-mono focus:outline-none focus:border-[#3b82f6] transition-colors"
            />
            <button
              onClick={handleSubmit}
              disabled={!userAnswer.trim()}
              className="px-4 py-2 bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-[#2d2d4a] disabled:text-[#475569] text-white text-sm font-medium rounded-lg transition-colors"
            >
              Check
            </button>
          </div>
        </div>
      ) : (
        <div className={`rounded-xl border p-4 space-y-2 ${
          correct
            ? "bg-green-500/10 border-green-500/30"
            : "bg-red-500/10 border-red-500/30"
        }`}>
          <div className="flex items-center gap-2">
            {correct
              ? <CheckCircle size={16} className="text-green-400" />
              : <XCircle size={16} className="text-red-400" />}
            <span className={`text-sm font-semibold ${correct ? "text-green-400" : "text-red-400"}`}>
              {correct ? "Bug found!" : `Not quite — the fix is: ${answer}`}
            </span>
          </div>
          <p className="text-sm text-[#94a3b8] leading-relaxed">{explanation}</p>
        </div>
      )}
    </div>
  );
}
