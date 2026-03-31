"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  fetchLesson, saveProgress, saveConfidence,
  type Lesson, type Question,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import {
  ArrowLeft, CheckCircle, XCircle, Lightbulb, Trophy, Code,
  ChevronRight, BookOpen, HelpCircle, Star,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

type Step = "concept" | "questions" | "challenge";

function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      components={{
        code: ({ className, children }) => {
          const isBlock = className?.includes("block");
          return isBlock
            ? <pre className="bg-[#1e1a16] border border-[#2c2520] rounded-lg p-3 my-2 overflow-x-auto"><code className={className}>{children}</code></pre>
            : <code className="bg-[#1e1a16] border border-[#2c2520] rounded px-1.5 py-0.5 text-sm">{children}</code>;
        },
        p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
        ul: ({ children }) => <ul className="list-disc ml-6 mb-3 space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal ml-6 mb-3 space-y-1">{children}</ol>,
        strong: ({ children }) => <strong className="font-semibold text-[#1c1410]">{children}</strong>,
        h3: ({ children }) => <h3 className="text-lg font-bold text-[#1c1410] mt-4 mb-2">{children}</h3>,
      }}
    >
      {text}
    </ReactMarkdown>
  );
}

export default function LessonPage() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const userKey = getUserKey();

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [step, setStep] = useState<Step>("concept");
  const [startTime] = useState(Date.now());
  const [completed, setCompleted] = useState(false);

  // Question state
  const [currentQ, setCurrentQ] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | number | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);

  // Challenge state
  const [challengeCode, setChallengeCode] = useState("");
  const [challengeResult, setChallengeResult] = useState<{ output?: string; error?: string } | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [stars, setStars] = useState(0);
  const [confidence, setConfidence] = useState(0);

  useEffect(() => {
    fetchLesson(lessonId)
      .then((l) => {
        setLesson(l);
        setChallengeCode(l.challenge?.starter_code || "");
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [lessonId]);

  const handleComplete = async () => {
    const timeSpent = (Date.now() - startTime) / 60000;
    try {
      await saveProgress(userKey, {
        lesson_id: lessonId,
        stars: Math.max(stars, 1),
        attempts: Math.max(attempts, 1),
        hints_used: 0,
        completed: true,
        time_spent_minutes: timeSpent,
      });
      if (confidence > 0) {
        await saveConfidence(userKey, lessonId, confidence);
      }
    } catch {}
    setCompleted(true);
  };

  const checkAnswer = (q: Question, answer: string | number) => {
    setSelectedAnswer(answer);
    setShowAnswer(true);
    const isCorrect = answer === q.answer;
    if (isCorrect) setCorrectCount((c) => c + 1);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#a01c2c] to-[#b8822a] mx-auto flex items-center justify-center animate-pulse">
            <span className="text-white font-bold">O</span>
          </div>
          <p className="text-sm text-[#9a8c80]">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-[#5c4f45] mb-4">Lesson not found.</p>
        <Link href="/curriculum" className="text-[#a01c2c] text-sm hover:underline">← Back to Curriculum</Link>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-6">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-400 to-green-600 mx-auto flex items-center justify-center shadow-lg">
          <Trophy size={28} className="text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-[#1c1410] mb-2">Lesson Complete!</h1>
          <p className="text-[#5c4f45]">{lesson.title}</p>
        </div>
        <div className="flex justify-center gap-1">
          {[1, 2, 3].map((s) => (
            <Star key={s} size={32} className={s <= stars ? "fill-yellow-400 text-yellow-400" : "text-[#e5ddd4]"} />
          ))}
        </div>
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 text-sm text-[#5c4f45]">
          Questions: {correctCount}/{lesson.questions.length} correct · Attempts: {attempts}
        </div>
        <div className="flex gap-3">
          <Link
            href="/curriculum"
            className="flex-1 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all text-center"
          >
            Back to Curriculum
          </Link>
          <Link
            href="/"
            className="flex-1 py-3 bg-[#ffffff] border border-[#e5ddd4] hover:border-[#a01c2c] text-[#1c1410] rounded-xl text-sm font-medium transition-all text-center"
          >
            Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const steps: { key: Step; label: string; icon: typeof BookOpen }[] = [
    { key: "concept", label: "Learn", icon: BookOpen },
    { key: "questions", label: "Practice", icon: HelpCircle },
    { key: "challenge", label: "Challenge", icon: Code },
  ];
  const stepIndex = steps.findIndex((s) => s.key === step);
  const StepIcon = steps[stepIndex].icon;

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link href="/curriculum" className="text-[#9a8c80] hover:text-[#5c4f45]">
          <ArrowLeft size={18} />
        </Link>
        <div className="flex-1 min-w-0">
          <p className="text-xs text-[#9a8c80]">{lesson.module_title}</p>
          <h1 className="text-lg font-bold text-[#1c1410] truncate">{lesson.title}</h1>
        </div>
      </div>

      {/* Step tabs */}
      <div className="flex gap-1 bg-[#f5f0ea] rounded-xl p-1">
        {steps.map((s, i) => {
          const Icon = s.icon;
          const isActive = s.key === step;
          const isDone = i < stepIndex;
          return (
            <button
              key={s.key}
              onClick={() => setStep(s.key)}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-white shadow text-[#a01c2c]"
                  : isDone
                  ? "text-green-600"
                  : "text-[#9a8c80] hover:text-[#5c4f45]"
              }`}
            >
              {isDone ? <CheckCircle size={14} /> : <Icon size={14} />}
              {s.label}
            </button>
          );
        })}
      </div>

      {/* ── Concept Step ── */}
      {step === "concept" && (
        <div className="space-y-4">
          <div className="bg-white border border-[#e5ddd4] rounded-xl p-6">
            <Markdown text={lesson.concept} />
          </div>
          {lesson.reference?.key_syntax && lesson.reference.key_syntax.length > 0 && (
            <div className="bg-[#1e1a16] border border-[#2c2520] rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb size={14} className="text-yellow-400" />
                <span className="text-xs font-semibold text-[#f0ece6]">Quick Reference</span>
              </div>
              <div className="space-y-1">
                {lesson.reference.key_syntax.map((s: string, i: number) => (
                  <code key={i} className="block text-xs text-green-300 font-mono">{s}</code>
                ))}
              </div>
              {lesson.reference.notes && (
                <p className="text-xs text-[#9a8c80] mt-2">{lesson.reference.notes}</p>
              )}
            </div>
          )}
          <button
            onClick={() => setStep("questions")}
            className="w-full flex items-center justify-center gap-2 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all"
          >
            Continue to Practice <ChevronRight size={16} />
          </button>
        </div>
      )}

      {/* ── Questions Step ── */}
      {step === "questions" && lesson.questions.length > 0 && (
        <div className="space-y-4">
          <div className="bg-white border border-[#e5ddd4] rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs text-[#9a8c80]">Question {currentQ + 1} of {lesson.questions.length}</span>
              <span className="text-xs text-green-600 font-medium">{correctCount} correct</span>
            </div>
            {(() => {
              const q = lesson.questions[currentQ];
              return (
                <div key={currentQ} className="space-y-4">
                  <p className="text-sm font-medium text-[#1c1410]">{q.question}</p>
                  {q.type === "multiple_choice" && q.options && (
                    <div className="space-y-2">
                      {q.options.map((opt: string, i: number) => {
                        const isSelected = selectedAnswer === i;
                        const isCorrect = i === q.answer;
                        const showResult = showAnswer;
                        return (
                          <button
                            key={i}
                            onClick={() => !showAnswer && checkAnswer(q, i)}
                            disabled={showAnswer}
                            className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-all ${
                              showResult && isCorrect
                                ? "border-green-400 bg-green-50 text-green-700"
                                : showResult && isSelected && !isCorrect
                                ? "border-red-400 bg-red-50 text-red-700"
                                : "border-[#e5ddd4] hover:border-[#a01c2c]"
                            }`}
                          >
                            <span className="font-medium mr-2">{String.fromCharCode(65 + i)}.</span>
                            {opt}
                            {showResult && isCorrect && <CheckCircle size={14} className="inline ml-2 text-green-500" />}
                            {showResult && isSelected && !isCorrect && <XCircle size={14} className="inline ml-2 text-red-500" />}
                          </button>
                        );
                      })}
                    </div>
                  )}
                  {q.type === "true_false" && (
                    <div className="flex gap-3">
                      {[true, false].map((val) => {
                        const isSelected = selectedAnswer === val;
                        const isCorrect = val === q.answer;
                        const showResult = showAnswer;
                        return (
                          <button
                            key={String(val)}
                            onClick={() => !showAnswer && checkAnswer(q, val)}
                            disabled={showAnswer}
                            className={`flex-1 py-3 rounded-lg border text-sm font-medium transition-all ${
                              showResult && isCorrect
                                ? "border-green-400 bg-green-50 text-green-700"
                                : showResult && isSelected && !isCorrect
                                ? "border-red-400 bg-red-50 text-red-700"
                                : "border-[#e5ddd4] hover:border-[#a01c2c]"
                            }`}
                          >
                            {String(val)}
                          </button>
                        );
                      })}
                    </div>
                  )}
                  {q.type === "fill_blank" && q.template && (
                    <div className="space-y-3">
                      <code className="block bg-[#1e1a16] text-green-300 p-3 rounded-lg text-sm font-mono">
                        {q.template}
                      </code>
                      {showAnswer && (
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                          <p className="text-xs text-green-700 font-mono">Answer: <code>{String(q.answer)}</code></p>
                        </div>
                      )}
                      {!showAnswer && (
                        <button
                          onClick={() => {
                            const input = prompt("Your answer:");
                            if (input !== null) checkAnswer(q, input.trim());
                          }}
                          className="px-4 py-2 bg-[#a01c2c] text-white rounded-lg text-sm font-medium"
                        >
                          Submit Answer
                        </button>
                      )}
                    </div>
                  )}
                  {showAnswer && (
                    <div className="bg-[#f5f0ea] rounded-lg p-3 text-xs text-[#5c4f45]">
                      <span className="font-medium">Explanation:</span> {q.explanation}
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => {
                if (currentQ < lesson.questions.length - 1) {
                  setCurrentQ((q) => q + 1);
                  setSelectedAnswer(null);
                  setShowAnswer(false);
                }
              }}
              disabled={currentQ >= lesson.questions.length - 1}
              className="flex-1 py-3 bg-white border border-[#e5ddd4] disabled:opacity-30 text-[#1c1410] rounded-xl text-sm font-medium transition-all"
            >
              Next Question
            </button>
            <button
              onClick={() => setStep("challenge")}
              className="flex-1 flex items-center justify-center gap-2 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all"
            >
              Go to Challenge <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* ── Challenge Step ── */}
      {step === "challenge" && (
        <div className="space-y-4">
          <div className="bg-white border border-[#e5ddd4] rounded-xl p-6">
            <h3 className="text-sm font-bold text-[#1c1410] mb-2">Coding Challenge</h3>
            <p className="text-sm text-[#5c4f45] mb-4">{lesson.challenge?.instructions}</p>
          </div>
          <div className="bg-[#1e1a16] border border-[#2c2520] rounded-xl overflow-hidden">
            <MonacoEditor
              value={challengeCode}
              language="python"
              theme="vs-dark"
              onChange={(v) => setChallengeCode(v ?? "")}
              height="300px"
              options={{
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                fontSize: 13,
                lineNumbers: "on",
                padding: { top: 12, bottom: 12 },
              }}
            />
          </div>
          {challengeResult && (
            <div className={`rounded-xl p-4 ${challengeResult.error ? "bg-red-50 border border-red-200" : "bg-green-50 border border-green-200"}`}>
              {challengeResult.error ? (
                <div>
                  <p className="text-xs font-semibold text-red-600 mb-1">Error</p>
                  <pre className="text-xs text-red-700 font-mono whitespace-pre-wrap">{challengeResult.error}</pre>
                </div>
              ) : (
                <div>
                  <p className="text-xs font-semibold text-green-600 mb-1">Output</p>
                  <pre className="text-xs text-green-700 font-mono whitespace-pre-wrap">{challengeResult.output || "(no output)"}</pre>
                </div>
              )}
            </div>
          )}
          {stars > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-[#9a8c80]">Stars earned:</span>
              <div className="flex gap-0.5">
                {[1, 2, 3].map((s) => (
                  <Star key={s} size={18} className={s <= stars ? "fill-yellow-400 text-yellow-400" : "text-[#e5ddd4]"} />
                ))}
              </div>
            </div>
          )}
          <div className="flex gap-3">
            <button
              onClick={async () => {
                setAttempts((a) => a + 1);
                // Simple evaluation: check if code runs without error
                try {
                  const { executePython } = await import("@/lib/api");
                  const result = await executePython(challengeCode);
                  setChallengeResult({ output: result.output, error: result.error || undefined });
                  if (!result.error) {
                    const newStars = attempts === 0 ? 3 : attempts < 2 ? 2 : 1;
                    setStars(newStars);
                  }
                } catch (err: unknown) {
                  setChallengeResult({ error: String(err) });
                }
              }}
              className="flex-1 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all"
            >
              Run Code
            </button>
            <button
              onClick={handleComplete}
              className="flex-1 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl text-sm font-semibold transition-all"
            >
              Complete Lesson
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
