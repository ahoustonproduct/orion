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
        <p className="text-sm text-[var(--color-text-muted)]">Loading review queue...</p>
      </div>
    );
  }

  if (!queue || queue.questions.length === 0) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-[var(--color-success)]/20 mx-auto flex items-center justify-center">
          <CheckCircle size={28} className="text-[var(--color-success)]" />
        </div>
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Queue Clear</h1>
        <p className="text-sm text-[var(--color-text-secondary)]">
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
          <RefreshCw size={28} className="text-[var(--color-accent)]" />
        </div>
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Session Complete</h1>
        <p className="text-sm text-[var(--color-text-secondary)]">
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
        <RefreshCw size={16} className="text-[var(--color-accent)]" />
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Review Queue</h1>
        <span className="text-xs bg-[var(--color-error)]/15 text-[var(--color-error)] px-2 py-0.5 rounded-full">
          {queue.total_due} due
        </span>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-3">
        <div className="flex gap-1">
          {queue.questions.map((_, i) => (
            <div
              key={i}
              className={`h-1 w-6 rounded-full ${i < currentIdx ? "bg-[var(--color-accent)]" : i === currentIdx ? "bg-[var(--color-accent-hover)]" : "bg-[var(--color-surface-2)]"}`}
            />
          ))}
        </div>
        <span className="text-xs text-[var(--color-text-muted)]">{currentIdx + 1} / {queue.questions.length}</span>
      </div>

      {/* Question source */}
      <div className="text-xs text-[var(--color-text-muted)]">
        From: <span className="text-[var(--color-text-secondary)]">{item.lesson_id.replace(/_/g, " ")}</span>
        {item.wrong_count > 1 && (
          <span className="ml-2 text-[var(--color-error)]">· missed {item.wrong_count}×</span>
        )}
      </div>

      {/* Question */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4">
        <div className="flex flex-wrap gap-1 mb-3">
          {(q.concept_tags ?? []).map((tag) => (
            <span key={tag} className="text-xs bg-[var(--color-accent)]/10 text-[var(--color-accent)] px-2 py-0.5 rounded-full">
              {tag.replace(/_/g, " ")}
            </span>
          ))}
        </div>
        <p className="text-sm font-medium text-[var(--color-text-primary)] leading-relaxed">{q.question}</p>
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
                  isRevealed && isCorrect ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                  : isRevealed && isSelected && !isCorrect ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                  : isSelected ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-text-primary)]"
                  : "border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
                }`}
              >
                <div className="flex items-center gap-2">
                  {isRevealed && isCorrect && <CheckCircle size={14} className="text-[var(--color-success)] shrink-0" />}
                  {isRevealed && isSelected && !isCorrect && <XCircle size={14} className="text-[var(--color-error)] shrink-0" />}
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
                  isRevealed && isCorrect ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                  : isRevealed && isSelected && !isCorrect ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                  : isSelected ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-[var(--color-text-primary)]"
                  : "border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
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
          className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl px-4 py-3 text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-all resize-none"
        />
      )}

      {!isRevealed ? (
        <button
          onClick={handleReveal}
          disabled={answers[currentIdx] === undefined}
          className="w-full py-3 bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all"
        >
          Check Answer
        </button>
      ) : (
        <div className="space-y-3">
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl px-4 py-3">
            <p className="text-xs font-semibold text-[var(--color-accent)] mb-1">Explanation</p>
            <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{q.explanation}</p>
            {(q.sample_answer || (q.accepted_answers && q.accepted_answers.length > 0)) && (
              <p className="text-xs text-[var(--color-text-muted)] mt-2">
                Sample: {q.sample_answer ?? q.accepted_answers?.[0]}
              </p>
            )}
          </div>
          <button
            onClick={handleNext}
            className="w-full flex items-center justify-center gap-2 py-3 bg-[var(--color-surface)] border border-[var(--color-border)] hover:border-[var(--color-accent)] text-[var(--color-text-primary)] rounded-xl text-sm font-medium transition-all"
          >
            {currentIdx < queue.questions.length - 1 ? "Next Question" : "Finish Session"}
            <ChevronRight size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
