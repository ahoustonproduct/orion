"use client";

import { useEffect, useState } from "react";
import { fetchQuiz, type QuizData, type Question } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import MultipleChoice from "@/components/QuestionTypes/MultipleChoice";
import TrueFalse from "@/components/QuestionTypes/TrueFalse";
import FillInBlank from "@/components/QuestionTypes/FillInBlank";
import { Flame, CheckCircle, ArrowRight, RefreshCw } from "lucide-react";

export default function QuizPage() {
  const [quiz, setQuiz] = useState<QuizData | null>(null);
  const [idx, setIdx] = useState(0);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    setIdx(0);
    setScore(0);
    setAnswered(false);
    setDone(false);
    fetchQuiz(getUserKey())
      .then(setQuiz)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const current: Question | undefined = quiz?.questions[idx];

  const handleCorrect = () => { setScore((s) => s + 1); setAnswered(true); };
  const handleWrong = () => setAnswered(true);

  // For TrueFalse/MC we can detect via onCorrect being called
  const next = () => {
    if (!quiz) return;
    if (idx < quiz.questions.length - 1) {
      setIdx(idx + 1);
      setAnswered(false);
    } else {
      setDone(true);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center space-y-2">
          <Flame size={32} className="text-yellow-500 mx-auto animate-pulse" />
          <p className="text-[#94a3b8] text-sm">Loading your quiz...</p>
        </div>
      </div>
    );
  }

  if (!quiz?.questions?.length) {
    return (
      <div className="max-w-md mx-auto px-4 py-12 text-center space-y-4">
        <Flame size={40} className="text-yellow-500/40 mx-auto" />
        <h2 className="text-lg font-semibold text-[#e2e8f0]">No quiz available yet</h2>
        <p className="text-sm text-[#94a3b8]">{quiz?.message ?? "Complete some lessons first. Flagged and low-starred lessons will appear here."}</p>
      </div>
    );
  }

  if (done) {
    const pct = Math.round((score / quiz.questions.length) * 100);
    return (
      <div className="max-w-md mx-auto px-4 py-12 text-center space-y-6">
        <div className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-2xl p-8 space-y-4">
          <CheckCircle size={48} className="text-green-400 mx-auto" />
          <h2 className="text-xl font-bold text-[#e2e8f0]">Quiz Complete!</h2>
          <div className="text-5xl font-bold text-gradient bg-gradient-to-r from-[#3b82f6] to-[#06b6d4] bg-clip-text text-transparent">
            {pct}%
          </div>
          <p className="text-[#94a3b8] text-sm">{score} / {quiz.questions.length} correct</p>
          {pct >= 80 && <p className="text-green-400 text-sm">Great job! 🎉</p>}
          {pct < 80 && <p className="text-[#94a3b8] text-sm">Keep practicing — you&apos;ll get there!</p>}
        </div>
        <button onClick={load} className="flex items-center gap-2 mx-auto px-6 py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-xl text-sm font-medium transition-all">
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
          <h1 className="text-lg font-bold text-[#e2e8f0]">Daily Quiz</h1>
        </div>
        <span className="text-xs text-[#64748b]">{idx + 1} / {quiz.questions.length}</span>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-[#242438] rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-[#3b82f6] to-[#06b6d4] rounded-full transition-all"
          style={{ width: `${((idx + 1) / quiz.questions.length) * 100}%` }}
        />
      </div>

      {/* Lesson label */}
      {(current as any)?.lesson_title && (
        <p className="text-xs text-[#3b82f6]">From: {(current as any).lesson_title}</p>
      )}

      {/* Question */}
      <div className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl p-4">
        {current?.type === "multiple_choice" && current.options && (
          <MultipleChoice
            question={current.question}
            options={current.options}
            answer={current.answer as number}
            explanation={current.explanation}
            onCorrect={handleCorrect}
          />
        )}
        {current?.type === "true_false" && (
          <TrueFalse
            question={current.question}
            answer={current.answer as boolean}
            explanation={current.explanation}
            onCorrect={handleCorrect}
          />
        )}
        {current?.type === "fill_blank" && (
          <FillInBlank
            question={current.question}
            template={(current as any).template ?? ""}
            answer={current.answer as string}
            explanation={current.explanation}
            onCorrect={handleCorrect}
          />
        )}
      </div>

      {answered && (
        <button
          onClick={next}
          className="w-full py-3 bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded-xl text-sm font-medium transition-all flex items-center justify-center gap-2"
        >
          {idx < quiz.questions.length - 1 ? "Next Question" : "See Results"}
          <ArrowRight size={14} />
        </button>
      )}
    </div>
  );
}
