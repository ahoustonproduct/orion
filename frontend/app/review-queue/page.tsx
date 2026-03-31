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
  const [answers, setAnswers] = useState<Record<number, string | number | boolean>>({});
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
        <p className="text-sm text-gray-400">Loading review queue...</p>
      </div>
    );
  }

  if (!queue || queue.questions.length === 0) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-green-500/20 mx-auto flex items-center justify-center">
          <CheckCircle size={28} className="text-green-400" />
        </div>
        <h1 className="text-xl font-bold text-white">Queue Clear</h1>
        <p className="text-sm text-gray-300">
          {queue && queue.total_due === 0
            ? "No reviews due. Keep learning to add to your queue."
            : "No questions due right now. Check back later."}
        </p>
      </div>
    );
  }

  if (sessionDone) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-[var(--color-accent)]/20 mx-auto flex items-center justify-center">
          <RefreshCw size={28} className="text-[var(--color-accent-light)]" />
        </div>
        <h1 className="text-xl font-bold text-white">Session Complete</h1>
        <p className="text-sm text-gray-300">
          Reviewed {queue.questions.length} question{queue.questions.length !== 1 ? "s" : ""}.
          {queue.total_due > queue.questions.length
            ? ` ${queue.total_due - queue.questions.length} more due.`
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
        <RefreshCw size={16} className="text-[var(--color-accent-light)]" />
        <h1 className="text-xl font-bold text-white">Review Queue</h1>
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
              className={`h-1 w-6 rounded-full ${i < currentIdx ? "bg-[var(--color-accent)]" : i === currentIdx ? "bg-[var(--color-accent-hover)]" : "bg-black/20"}`}
            />
          ))}
        </div>
        <span className="text-xs text-gray-400">{currentIdx + 1} / {queue.questions.length}</span>
      </div>

      {/* Question source */}
      <div className="text-xs text-gray-400">
        From: <span className="text-gray-300">{item.lesson_id.replace(/_/g, " ")}</span>
        {item.wrong_count > 1 && (
          <span className="ml-2 text-red-400">· missed {item.wrong_count}×</span>
        )}
      </div>

      {/* Question */}
      <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl p-4">
        <div className="flex flex-wrap gap-1 mb-3">
          {(q.concept_tags ?? []).map((tag) => (
            <span key={tag} className="text-xs bg-[var(--color-accent)]/10 text-[var(--color-accent-light)] px-2 py-0.5 rounded-full">
              {tag.replace(/_/g, " ")}
            </span>
          ))}
        </div>
        <p className="text-sm font-medium text-white leading-relaxed">{q.question}</p>
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
                  isRevealed && isCorrect ? "border-green-400 bg-green-500/10 text-green-400"
                  : isRevealed && isSelected && !isCorrect ? "border-red-400 bg-red-500/10 text-red-400"
                  : isSelected ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-white"
                  : "border-white/10 bg-black/20 text-gray-300 hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md"
                }`}
              >
                <div className="flex items-center gap-2">
                  {isRevealed && isCorrect && <CheckCircle size={14} className="text-green-400 shrink-0" />}
                  {isRevealed && isSelected && !isCorrect && <XCircle size={14} className="text-red-400 shrink-0" />}
                  <span className="font-medium mr-2">{String.fromCharCode(65 + i)}.</span>
                  {opt}
                </div>
              </button>
            );
          })}
        </div>
      )}

      {/* True/False */}
      {q.type === "true_false" && (
        <div className="flex gap-3">
          {[true, false].map((val) => {
            const isCorrect = val === (q.correct_index === 0);
            const isSelected = answers[currentIdx] === val;
            return (
              <button
                key={String(val)}
                onClick={() => !isRevealed && setAnswers((prev) => ({ ...prev, [currentIdx]: val }))}
                disabled={!!isRevealed}
                className={`flex-1 py-3 rounded-xl border text-sm font-medium transition-all ${
                  isRevealed && isCorrect ? "border-green-400 bg-green-500/10 text-green-400"
                  : isRevealed && isSelected && !isCorrect ? "border-red-400 bg-red-500/10 text-red-400"
                  : isSelected ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-white"
                  : "border-white/10 bg-black/20 text-gray-300 hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md"
                }`}
              >
                {String(val)}
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
          className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-[var(--color-accent)] transition-all resize-none"
        />
      )}

      {!isRevealed ? (
        <button
          onClick={handleReveal}
          disabled={answers[currentIdx] === undefined}
          className="w-full py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all"
        >
          Check Answer
        </button>
      ) : (
        <div className="space-y-3">
          <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl px-4 py-3">
            <p className="text-xs font-semibold text-[var(--color-accent-light)] mb-1">Explanation</p>
            <p className="text-sm text-gray-300 leading-relaxed">{q.explanation}</p>
            {(q.sample_answer || (q.accepted_answers && q.accepted_answers.length > 0)) && (
              <p className="text-xs text-gray-400 mt-2">
                Sample: {q.sample_answer ?? q.accepted_answers?.[0]}
              </p>
            )}
          </div>
          <button
            onClick={handleNext}
            className="w-full flex items-center justify-center gap-2 py-3 glass-card border-white/5 border border-white/10 border-transparent hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md text-white rounded-xl text-sm font-medium transition-all"
          >
            {currentIdx < queue.questions.length - 1 ? "Next Question" : "Finish Session"}
            <ChevronRight size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
