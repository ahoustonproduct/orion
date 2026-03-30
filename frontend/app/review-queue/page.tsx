"use client";

import { useEffect, useState } from "react";
import { fetchReviewQueue, recordReview, type ReviewQueue, type ReviewQuestion } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { RefreshCw, CheckCircle, XCircle, ChevronRight } from "lucide-react";

export default function ReviewQueuePage() {
  const userKey = getUserKey();
  const [queue, setQueue] = useState<ReviewQueue | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string | number>>({});
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});
  const [sessionDone, setSessionDone] = useState(false);

  useEffect(() => {
    fetchReviewQueue(userKey)
      .then((q) => { setQueue(q); setLoading(false); })
      .catch(() => setLoading(false));
  }, [userKey]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-sm text-[#9a8c80]">Loading review queue...</p>
      </div>
    );
  }

  if (!queue || queue.questions.length === 0) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-green-500/20 mx-auto flex items-center justify-center">
          <CheckCircle size={28} className="text-green-400" />
        </div>
        <h1 className="text-xl font-bold text-[#1c1410]">Queue Clear</h1>
        <p className="text-sm text-[#5c4f45]">
          {queue && queue.total_due === 0
            ? "No reviews due today. Keep learning to add to your queue."
            : "No questions due right now. Check back tomorrow."}
        </p>
      </div>
    );
  }

  if (sessionDone) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-[#a01c2c]/20 mx-auto flex items-center justify-center">
          <RefreshCw size={28} className="text-[#a01c2c]" />
        </div>
        <h1 className="text-xl font-bold text-[#1c1410]">Session Complete</h1>
        <p className="text-sm text-[#5c4f45]">
          Reviewed {queue.questions.length} question{queue.questions.length !== 1 ? "s" : ""}.
          {queue.total_due > queue.questions.length
            ? ` ${queue.total_due - queue.questions.length} more due today.`
            : " All caught up!"}
        </p>
      </div>
    );
  }

  const item: ReviewQuestion = queue.questions[currentIdx];
  const q = item.question;
  const isRevealed = revealed[currentIdx];

  const handleReveal = async () => {
    const userAns = answers[currentIdx];
    const isCorrect = q.type === "multiple_choice" ? userAns === q.correct_index : !!userAns;
    setRevealed((prev) => ({ ...prev, [currentIdx]: true }));
    try {
      await recordReview(userKey, item.question_id, isCorrect);
    } catch {}
  };

  const handleNext = () => {
    if (currentIdx < queue.questions.length - 1) {
      setCurrentIdx((i) => i + 1);
    } else {
      setSessionDone(true);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center gap-2">
        <RefreshCw size={16} className="text-[#a01c2c]" />
        <h1 className="text-xl font-bold text-[#1c1410]">Review Queue</h1>
        <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full">
          {queue.total_due} due
        </span>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-3">
        <div className="flex gap-1">
          {queue.questions.map((_, i) => (
            <div
              key={i}
              className={`h-1 w-6 rounded-full ${i < currentIdx ? "bg-[#a01c2c]" : i === currentIdx ? "bg-[#c97a84]" : "bg-[#e5ddd4]"}`}
            />
          ))}
        </div>
        <span className="text-xs text-[#9a8c80]">{currentIdx + 1} / {queue.questions.length}</span>
      </div>

      {/* Question source */}
      <div className="text-xs text-[#9a8c80]">
        From: <span className="text-[#5c4f45]">{item.lesson_id.replace(/_/g, " ")}</span>
        {item.wrong_count > 1 && (
          <span className="ml-2 text-red-400">· missed {item.wrong_count}×</span>
        )}
      </div>

      {/* Question */}
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <div className="flex flex-wrap gap-1 mb-3">
          {(q.concept_tags ?? []).map((tag) => (
            <span key={tag} className="text-xs bg-[#a01c2c]/10 text-[#a01c2c] px-2 py-0.5 rounded-full">
              {tag.replace(/_/g, " ")}
            </span>
          ))}
        </div>
        <p className="text-sm font-medium text-[#1c1410] leading-relaxed">{q.question}</p>
      </div>

      {/* Multiple choice */}
      {q.type === "multiple_choice" && q.options && (
        <div className="space-y-2">
          {q.options.map((opt, i) => {
            const isCorrect = i === q.correct_index;
            const isSelected = answers[currentIdx] === i;
            return (
              <button
                key={i}
                onClick={() => !isRevealed && setAnswers((prev) => ({ ...prev, [currentIdx]: i }))}
                disabled={!!isRevealed}
                className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                  isRevealed && isCorrect ? "border-green-500/50 bg-green-500/10 text-green-300"
                  : isRevealed && isSelected && !isCorrect ? "border-red-500/50 bg-red-500/10 text-red-300"
                  : isSelected ? "border-[#a01c2c] bg-[#a01c2c]/10 text-[#1c1410]"
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

      {/* Short answer / WWYD */}
      {(q.type === "short_answer" || q.type === "what_would_you_do") && (
        <textarea
          value={(answers[currentIdx] as string) ?? ""}
          onChange={(e) => !isRevealed && setAnswers((prev) => ({ ...prev, [currentIdx]: e.target.value }))}
          disabled={!!isRevealed}
          placeholder="Write your answer..."
          rows={3}
          className="w-full bg-[#ffffff] border border-[#e5ddd4] rounded-xl px-4 py-3 text-sm text-[#1c1410] placeholder-[#9a8c80] outline-none focus:border-[#a01c2c] transition-all resize-none"
        />
      )}

      {!isRevealed ? (
        <button
          onClick={handleReveal}
          disabled={answers[currentIdx] === undefined}
          className="w-full py-3 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all"
        >
          Check Answer
        </button>
      ) : (
        <div className="space-y-3">
          <div className="bg-[#f8eaec] border border-[#a01c2c]/20 rounded-xl px-4 py-3">
            <p className="text-xs font-semibold text-[#a01c2c] mb-1">Explanation</p>
            <p className="text-sm text-[#5c4f45] leading-relaxed">{q.explanation}</p>
            {(q.sample_answer || (q.accepted_answers && q.accepted_answers.length > 0)) && (
              <p className="text-xs text-[#9a8c80] mt-2">
                Sample: {q.sample_answer ?? q.accepted_answers?.[0]}
              </p>
            )}
          </div>
          <button
            onClick={handleNext}
            className="w-full flex items-center justify-center gap-2 py-3 bg-[#ffffff] border border-[#e5ddd4] hover:border-[#a01c2c] text-[#1c1410] rounded-xl text-sm font-medium transition-all"
          >
            {currentIdx < queue.questions.length - 1 ? "Next Question" : "Finish Session"}
            <ChevronRight size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
