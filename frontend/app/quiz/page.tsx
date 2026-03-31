"use client";

import { useEffect, useState } from "react";
import { fetchQuiz, type QuizData, type Question } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Flame, CheckCircle, ArrowRight, RefreshCw, XCircle } from "lucide-react";

export default function QuizPage() {
  const [quiz, setQuiz] = useState<QuizData | null>(null);
  const [idx, setIdx] = useState(0);
  const [score, setScore] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | number | boolean | null>(null);
  const [answered, setAnswered] = useState(false);
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    setIdx(0);
    setScore(0);
    setAnswered(false);
    setSelectedAnswer(null);
    setDone(false);
    fetchQuiz(getUserKey())
      .then(setQuiz)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const current: Question | undefined = quiz?.questions[idx];

  const checkAnswer = (answer: string | number | boolean) => {
    setSelectedAnswer(answer);
    setAnswered(true);
    if (answer === current?.answer) setScore((s) => s + 1);
  };

  const next = () => {
    if (!quiz) return;
    if (idx < quiz.questions.length - 1) {
      setIdx(idx + 1);
      setAnswered(false);
      setSelectedAnswer(null);
    } else {
      setDone(true);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center space-y-2">
          <Flame size={32} className="text-yellow-500 mx-auto animate-pulse" />
          <p className="text-sm text-gray-400">Loading your quiz...</p>
        </div>
      </div>
    );
  }

  if (!quiz?.questions?.length) {
    return (
      <div className="max-w-md mx-auto px-4 py-12 text-center space-y-4">
        <Flame size={40} className="text-yellow-500/40 mx-auto" />
        <h2 className="text-lg font-semibold text-white">No quiz available yet</h2>
        <p className="text-sm text-gray-300">{quiz?.message ?? "Complete some lessons first. Flagged and low-starred lessons will appear here."}</p>
      </div>
    );
  }

  if (done) {
    const pct = Math.round((score / quiz.questions.length) * 100);
    return (
      <div className="max-w-md mx-auto px-4 py-12 text-center space-y-6">
        <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-2xl p-8 space-y-4">
          <CheckCircle size={48} className="text-green-400 mx-auto" />
          <h2 className="text-xl font-bold text-white">Quiz Complete!</h2>
          <div className="text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
            {pct}%
          </div>
          <p className="text-gray-300 text-sm">{score} / {quiz.questions.length} correct</p>
          {pct >= 80 && <p className="text-green-400 text-sm">Great job!</p>}
          {pct < 80 && <p className="text-gray-300 text-sm">Keep practicing — you'll get there!</p>}
        </div>
        <button onClick={load} className="flex items-center gap-2 mx-auto px-6 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-medium transition-all">
          <RefreshCw size={14} /> Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Flame size={18} className="text-yellow-500" />
          <h1 className="text-lg font-bold text-white">Daily Quiz</h1>
        </div>
        <span className="text-xs text-gray-400">{idx + 1} / {quiz.questions.length}</span>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-black/20 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-hover)] rounded-full transition-all"
          style={{ width: `${((idx + 1) / quiz.questions.length) * 100}%` }}
        />
      </div>

      {/* Lesson label */}
      {(current as any)?.lesson_title && (
        <p className="text-xs text-[var(--color-accent-light)]">From: {(current as any).lesson_title}</p>
      )}

      {/* Question */}
      <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl p-4">
        {current && (
          <div className="space-y-4">
            <p className="text-sm font-medium text-white">{current.question}</p>
            {current.type === "multiple_choice" && current.options && (
              <div className="space-y-2">
                {current.options.map((opt: string, i: number) => {
                  const isSelected = selectedAnswer === i;
                  const isCorrect = i === current.answer;
                  return (
                    <button
                      key={i}
                      onClick={() => !answered && checkAnswer(i)}
                      disabled={answered}
                      className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-all ${
                        answered && isCorrect
                          ? "border-green-400 bg-green-500/10 text-green-400"
                          : answered && isSelected && !isCorrect
                          ? "border-red-400 bg-red-500/10 text-red-400"
                          : isSelected
                          ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-white"
                          : "border-white/10 hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md"
                      }`}
                    >
                      <span className="font-medium mr-2">{String.fromCharCode(65 + i)}.</span>
                      {opt}
                      {answered && isCorrect && <CheckCircle size={14} className="inline ml-2 text-green-500" />}
                      {answered && isSelected && !isCorrect && <XCircle size={14} className="inline ml-2 text-red-500" />}
                    </button>
                  );
                })}
              </div>
            )}
            {current.type === "true_false" && (
              <div className="flex gap-3">
                {[true, false].map((val) => {
                  const isSelected = selectedAnswer === val;
                  const isCorrect = val === current.answer;
                  return (
                    <button
                      key={String(val)}
                      onClick={() => !answered && checkAnswer(val)}
                      disabled={answered}
                      className={`flex-1 py-3 rounded-lg border text-sm font-medium transition-all ${
                        answered && isCorrect
                          ? "border-green-400 bg-green-500/10 text-green-400"
                          : answered && isSelected && !isCorrect
                          ? "border-red-400 bg-red-500/10 text-red-400"
                          : isSelected
                          ? "border-[var(--color-accent)] bg-[var(--color-accent)]/10 text-white"
                          : "border-white/10 hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md"
                      }`}
                    >
                      {String(val)}
                    </button>
                  );
                })}
              </div>
            )}
            {current.type === "fill_blank" && (current as any).template && (
              <div className="space-y-3">
                <code className="block bg-black/40 text-green-300 p-3 rounded-lg text-sm font-mono">
                  {(current as any).template}
                </code>
                {!answered && (
                  <button
                    onClick={() => {
                      const input = prompt("Your answer:");
                      if (input !== null) checkAnswer(input.trim());
                    }}
                    className="px-4 py-2 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 text-white rounded-lg text-sm font-medium"
                  >
                    Submit Answer
                  </button>
                )}
                {answered && (
                  <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3">
                    <p className="text-xs text-green-400 font-mono">Answer: <code>{String(current.answer)}</code></p>
                  </div>
                )}
              </div>
            )}
            {answered && (
              <div className="bg-black/20 rounded-lg p-3 text-xs text-gray-300">
                <span className="font-medium">Explanation:</span> {current.explanation}
              </div>
            )}
          </div>
        )}
      </div>

      {answered && (
        <button
          onClick={next}
          className="w-full py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-medium transition-all flex items-center justify-center gap-2"
        >
          {idx < quiz.questions.length - 1 ? "Next Question" : "See Results"}
          <ArrowRight size={14} />
        </button>
      )}
    </div>
  );
}
