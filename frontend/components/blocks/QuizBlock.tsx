"use client";

import { useState } from "react";
import { QuizBlock2 as BlockType, QuizQuestion2, recordMastery, addToReviewQueue } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { CheckCircle, XCircle, ChevronRight } from "lucide-react";

interface Props { block: BlockType; lessonId: string; }

export default function QuizBlock({ block, lessonId }: Props) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string | number>>({});
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});
  const [completed, setCompleted] = useState(false);
  const userKey = getUserKey();

  const question: QuizQuestion2 = block.questions[currentIdx];

  const correctCount = Object.keys(revealed).filter((i) => {
    const q = block.questions[Number(i)];
    if (q.type === "multiple_choice") return answers[Number(i)] === q.correct_index;
    return !!answers[Number(i)]; // short answer / WWYD: counted if answered
  }).length;

  const handleReveal = async (qIdx: number) => {
    const q = block.questions[qIdx];
    const userAns = answers[qIdx];
    const isCorrect = q.type === "multiple_choice" ? userAns === q.correct_index : true;

    setRevealed((prev) => ({ ...prev, [qIdx]: true }));

    for (const tag of q.concept_tags) {
      try { await recordMastery(userKey, tag, isCorrect); } catch {}
    }

    if (!isCorrect) {
      try { await addToReviewQueue(userKey, q.id, lessonId, JSON.stringify(q)); } catch {}
    }
  };

  const handleNext = () => {
    if (currentIdx < block.questions.length - 1) {
      setCurrentIdx((i) => i + 1);
    } else {
      setCompleted(true);
    }
  };

  if (completed) {
    const score = Math.round((correctCount / block.questions.length) * 100);
    return (
      <div className="text-center space-y-4 py-6">
        <div className={`text-4xl font-bold ${score >= 80 ? "text-green-400" : score >= 60 ? "text-yellow-400" : "text-red-400"}`}>
          {score}%
        </div>
        <p className="text-sm text-[#5c4f45]">{correctCount} of {block.questions.length} correct</p>
        {score < 70 && (
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl px-4 py-3">
            <p className="text-xs text-yellow-200">
              Missed questions have been added to your Review Queue. You&apos;ll see them tomorrow.
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="flex gap-1">
          {block.questions.map((_, i) => (
            <div
              key={i}
              className={`h-1 w-6 rounded-full ${i < currentIdx ? "bg-[#a01c2c]" : i === currentIdx ? "bg-[#c97a84]" : "bg-[#e5ddd4]"}`}
            />
          ))}
        </div>
        <span className="text-xs text-[#9a8c80]">{currentIdx + 1} / {block.questions.length}</span>
      </div>

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <div className="flex flex-wrap gap-1 mb-3">
          {question.concept_tags.map((tag) => (
            <span key={tag} className="text-xs bg-[#a01c2c]/10 text-[#a01c2c] px-2 py-0.5 rounded-full">
              {tag.replace(/_/g, " ")}
            </span>
          ))}
        </div>
        <p className="text-sm font-medium text-[#1c1410] leading-relaxed">{question.question}</p>
      </div>

      {question.type === "multiple_choice" && question.options && (
        <div className="space-y-2">
          {question.options.map((opt, i) => {
            const isRevealed = revealed[currentIdx];
            const isCorrect = i === question.correct_index;
            const isSelected = answers[currentIdx] === i;
            return (
              <button
                key={i}
                onClick={() => !isRevealed && setAnswers((prev) => ({ ...prev, [currentIdx]: i }))}
                disabled={!!isRevealed}
                className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                  isRevealed && isCorrect
                    ? "border-green-500/50 bg-green-500/10 text-green-300"
                    : isRevealed && isSelected && !isCorrect
                    ? "border-red-500/50 bg-red-500/10 text-red-300"
                    : isSelected
                    ? "border-[#a01c2c] bg-[#a01c2c]/10 text-[#1c1410]"
                    : "border-[#e5ddd4] bg-[#ffffff] text-[#5c4f45] hover:border-[#a01c2c]/50"
                }`}
              >
                <div className="flex items-center gap-2">
                  {isRevealed && isCorrect && <CheckCircle size={14} className="text-green-400 shrink-0" />}
                  {isRevealed && isSelected && !isCorrect && <XCircle size={14} className="text-red-400 shrink-0" />}
                  {opt}
                </div>
              </button>
            );
          })}
        </div>
      )}

      {(question.type === "short_answer" || question.type === "what_would_you_do") && (
        <textarea
          value={(answers[currentIdx] as string) ?? ""}
          onChange={(e) => !revealed[currentIdx] && setAnswers((prev) => ({ ...prev, [currentIdx]: e.target.value }))}
          disabled={!!revealed[currentIdx]}
          placeholder={
            question.type === "what_would_you_do"
              ? "What would you do? Be specific about the action and your reasoning..."
              : "Write your answer..."
          }
          rows={4}
          className="w-full bg-[#ffffff] border border-[#e5ddd4] rounded-xl px-4 py-3 text-sm text-[#1c1410] placeholder-[#9a8c80] outline-none focus:border-[#a01c2c] transition-all resize-none"
        />
      )}

      {!revealed[currentIdx] ? (
        <button
          onClick={() => handleReveal(currentIdx)}
          disabled={answers[currentIdx] === undefined}
          className="w-full py-3 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all"
        >
          Check Answer
        </button>
      ) : (
        <div className="space-y-3">
          <div className="bg-[#f8eaec] border border-[#a01c2c]/20 rounded-xl px-4 py-3">
            <p className="text-xs font-semibold text-[#a01c2c] mb-1">Explanation</p>
            <p className="text-sm text-[#5c4f45] leading-relaxed">{question.explanation}</p>
            {(question.sample_answer || (question.accepted_answers && question.accepted_answers.length > 0)) && (
              <p className="text-xs text-[#9a8c80] mt-2">
                Sample answer: {question.sample_answer ?? question.accepted_answers?.[0]}
              </p>
            )}
          </div>
          <button
            onClick={handleNext}
            className="w-full flex items-center justify-center gap-2 py-3 bg-[#ffffff] border border-[#e5ddd4] hover:border-[#a01c2c] text-[#1c1410] rounded-xl text-sm font-medium transition-all"
          >
            {currentIdx < block.questions.length - 1 ? "Next Question" : "Finish Quiz"}
            <ChevronRight size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
