"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  fetchLesson, saveProgress, saveConfidence, fetchModules,
  type Lesson, type Question
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import {
  ArrowLeft, CheckCircle, XCircle, Lightbulb, Trophy, Code,
  ChevronRight, BookOpen, HelpCircle, Star
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import dynamic from "next/dynamic";
import ConfidenceRating from "@/components/ConfidenceRating";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

type Step = "concept" | "questions" | "challenge";

function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeSanitize]}
      components={{
        code: ({ className, children }) => {
          const isBlock = className?.includes("block");
          return isBlock
            ? <pre className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg p-3 my-2 overflow-x-auto"><code className={className}>{children}</code></pre>
            : <code className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded px-1.5 py-0.5 text-sm">{children}</code>;
        },
        p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
        ul: ({ children }) => <ul className="list-disc ml-6 mb-3 space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal ml-6 mb-3 space-y-1">{children}</ol>,
        strong: ({ children }) => <strong className="font-semibold text-[var(--color-text-primary)]">{children}</strong>,
        h3: ({ children }) => <h3 className="text-lg font-bold text-[var(--color-text-primary)] mt-4 mb-2">{children}</h3>,
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
  const startTimeRef = useRef(Date.now());
  const [completed, setCompleted] = useState(false);

  // Question state
  const [currentQ, setCurrentQ] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | number | boolean | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);

  const [challengeCode, setChallengeCode] = useState("");
  const [challengeResult, setChallengeResult] = useState<{ output?: string; error?: string } | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [stars, setStars] = useState(0);
  const [confidence, setConfidence] = useState(0);
  
  const [challengeFeedback, setChallengeFeedback] = useState("");
  const [nextLessonId, setNextLessonId] = useState<string | null>(null);

  // Fill-in-blank input state
  const [fillInput, setFillInput] = useState("");

  useEffect(() => {
    fetchLesson(lessonId)
      .then((l) => {
        setLesson(l);
        setChallengeCode(l.challenge?.starter_code || "");
        setLoading(false);
      })
      .catch(() => setLoading(false));

    // Pre-calculate next lesson ID so it's ready upon completion
    fetchModules()
      .then((modules) => {
        let foundCurrent = false;
        let nextId = null;
        for (const m of modules) {
          for (const l of m.lessons || []) {
            if (foundCurrent) {
              nextId = l.id;
              break;
            }
            if (l.id === lessonId) foundCurrent = true;
          }
          if (nextId) break;
        }
        setNextLessonId(nextId);
      })
      .catch(console.error);
  }, [lessonId]);

  const handleComplete = async () => {
    const timeSpent = (Date.now() - startTimeRef.current) / 60000;
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
    } catch (err) {
      console.error("Failed to save progress:", err);
    }
    setCompleted(true);
    // Next lesson ID is now eagerly loaded in useEffect and set when lesson loads.
  };

  const checkAnswer = (q: Question, answer: string | number | boolean) => {
    setSelectedAnswer(answer);
    setShowAnswer(true);
    const isCorrect = answer === q.answer;
    if (isCorrect) setCorrectCount((c) => c + 1);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent-light)] mx-auto flex items-center justify-center animate-pulse">
            <span className="text-white font-bold">O</span>
          </div>
          <p className="text-sm text-[var(--color-text-muted)]">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-[var(--color-text-secondary)] mb-4">Lesson not found.</p>
        <Link href="/curriculum" className="text-[var(--color-accent)] text-sm hover:underline">← Back to Curriculum</Link>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-6">
        <div className="w-16 h-16 rounded-2xl bg-[var(--color-success)] mx-auto flex items-center justify-center shadow-lg">
          <Trophy size={28} className="text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">Lesson Complete!</h1>
          <p className="text-[var(--color-text-secondary)]">{lesson.title}</p>
        </div>
        <div className="flex justify-center gap-1">
          {[1, 2, 3].map((s) => (
            <Star key={s} size={32} className={s <= stars ? "fill-[var(--color-star)] text-[var(--color-star)]" : "text-[var(--color-border)]"} />
          ))}
        </div>
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 text-sm text-[var(--color-text-secondary)]">
          Questions: {correctCount}/{lesson.questions.length} correct · Attempts: {attempts}
        </div>
        <div className="flex gap-3">
          <Link
            href="/curriculum"
            className="flex-1 py-3 bg-[var(--color-surface)] border border-[var(--color-border)] hover:border-[var(--color-accent)] text-[var(--color-text-primary)] rounded-xl text-sm font-medium transition-all text-center"
          >
            ← Curriculum
          </Link>
          {nextLessonId ? (
            <Link
              href={`/learn/${nextLessonId}`}
              className="flex-1 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-semibold transition-all text-center flex items-center justify-center gap-2"
            >
              Next Lesson <ChevronRight size={16} />
            </Link>
          ) : (
            <Link
              href="/"
              className="flex-1 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-semibold transition-all text-center"
            >
              Dashboard
            </Link>
          )}
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
  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link href="/curriculum" className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]">
          <ArrowLeft size={18} />
        </Link>
        <div className="flex-1 min-w-0">
          <p className="text-xs text-[var(--color-text-muted)]">{lesson.module_title}</p>
          <h1 className="text-lg font-bold text-[var(--color-text-primary)] truncate">{lesson.title}</h1>
        </div>
      </div>

      {/* Step tabs */}
      <div className="flex gap-1 bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-xl p-1">
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
                  ? "bg-[var(--color-surface)] border border-[var(--color-border)] shadow-sm text-[var(--color-accent)]"
                  : isDone
                  ? "text-[var(--color-success)]"
                  : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
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
          <div className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-xl p-8">
            <Markdown text={lesson.concept} />
          </div>
          {lesson.reference?.key_syntax && lesson.reference.key_syntax.length > 0 && (
            <div className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb size={14} className="text-[var(--color-star)]" />
                <span className="text-xs font-semibold text-[var(--color-text-secondary)]">Quick Reference</span>
              </div>
              <div className="space-y-1">
                {lesson.reference.key_syntax.map((s: string, i: number) => (
                  <code key={i} className="block text-xs text-[var(--color-accent)] font-mono">{s}</code>
                ))}
              </div>
              {lesson.reference.notes && (
                <p className="text-xs text-[var(--color-text-muted)] mt-2">{lesson.reference.notes}</p>
              )}
            </div>
          )}
          <button
            onClick={() => setStep("questions")}
            className="w-full flex items-center justify-center gap-2 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-semibold transition-all"
          >
            Continue to Practice <ChevronRight size={16} />
          </button>
        </div>
      )}

      {/* ── Questions Step ── */}
      {step === "questions" && lesson.questions.length > 0 && (
        <div className="space-y-4">
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs text-[var(--color-text-muted)]">Question {currentQ + 1} of {lesson.questions.length}</span>
              <span className="text-xs text-[var(--color-success)] font-medium">{correctCount} correct</span>
            </div>
            {(() => {
              const q = lesson.questions[currentQ];
              return (
                <div key={currentQ} className="space-y-4">
                  <p className="text-sm font-medium text-[var(--color-text-primary)]">{q.question}</p>
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
                                ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                                : showResult && isSelected && !isCorrect
                                ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                                : "border-[var(--color-border)] bg-[var(--color-surface-2)] hover:border-[var(--color-accent)] text-[var(--color-text-primary)]"
                            }`}
                          >
                            <span className="font-medium mr-2">{String.fromCharCode(65 + i)}.</span>
                            {opt}
                            {showResult && isCorrect && <CheckCircle size={14} className="inline ml-2 text-[var(--color-success)]" />}
                            {showResult && isSelected && !isCorrect && <XCircle size={14} className="inline ml-2 text-[var(--color-error)]" />}
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
                                ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                                : showResult && isSelected && !isCorrect
                                ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                                : "border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
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
                      <code className="block bg-[var(--color-surface-2)] border border-[var(--color-border)] text-[var(--color-text-primary)] p-3 rounded-lg text-sm font-mono">
                        {q.template}
                      </code>
                      {showAnswer ? (
                        <div className="bg-[var(--color-success)]/10 border border-[var(--color-success)]/30 rounded-lg p-3">
                          <p className="text-xs text-[var(--color-success)] font-mono">Answer: <code>{String(q.answer)}</code></p>
                        </div>
                      ) : (
                        <div className="flex gap-2">
                          <input
                            type="text"
                            value={fillInput}
                            onChange={(e) => setFillInput(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter" && fillInput.trim()) { checkAnswer(q, fillInput.trim()); setFillInput(""); } }}
                            placeholder="Type your answer..."
                            className="flex-1 bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-colors"
                          />
                          <button
                            onClick={() => { if (fillInput.trim()) { checkAnswer(q, fillInput.trim()); setFillInput(""); } }}
                            disabled={!fillInput.trim()}
                            className="px-4 py-2 bg-[var(--color-accent)] text-white rounded-lg text-sm font-medium disabled:opacity-40 transition-colors"
                          >
                            Submit
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                  {showAnswer && (
                    <div className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg p-3 text-xs text-[var(--color-text-secondary)]">
                      <span className="font-medium text-[var(--color-text-primary)]">Explanation:</span> {q.explanation}
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
              className="flex-1 py-3 bg-[var(--color-surface)] border border-[var(--color-border)] hover:border-[var(--color-accent)] disabled:opacity-30 text-[var(--color-text-primary)] rounded-xl text-sm font-medium transition-all"
            >
              Next Question
            </button>
            <button
              onClick={() => setStep("challenge")}
              className="flex-1 flex items-center justify-center gap-2 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-semibold transition-all"
            >
              Go to Challenge <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* ── Challenge Step ── */}
      {step === "challenge" && (
        <div className="space-y-4">
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-6">
            <h3 className="text-sm font-bold text-[var(--color-text-primary)] mb-2">Coding Challenge</h3>
            <p className="text-sm text-[var(--color-text-secondary)] mb-4">{lesson.challenge?.instructions}</p>
          </div>
          <div className="bg-[#14110F] border border-[#2C2520] rounded-xl overflow-hidden">
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
                wordWrap: "off",
                scrollbar: { horizontal: "auto" },
              }}
            />
          </div>
          {challengeResult && (
            <div className={`rounded-xl p-4 ${challengeResult.error ? "bg-[var(--color-error)]/10 border border-[var(--color-error)]/30" : "bg-[var(--color-success)]/10 border border-[var(--color-success)]/30"}`}>
              {challengeResult.error ? (
                <div>
                  <p className="text-xs font-semibold text-[var(--color-error)] mb-1">Error</p>
                  <pre className="text-xs text-[var(--color-error)] font-mono whitespace-pre-wrap">{challengeResult.error}</pre>
                </div>
              ) : (
                <div>
                  <p className="text-xs font-semibold text-[var(--color-success)] mb-1">Output</p>
                  <pre className="text-xs text-[var(--color-success)] font-mono whitespace-pre-wrap">{challengeResult.output || "(no output)"}</pre>
                </div>
              )}
            </div>
          )}
          
          {challengeFeedback && (
            <div className="mt-4 p-5 bg-[var(--color-surface)] border border-[var(--color-accent)]/30 rounded-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-[var(--color-accent)]"></div>
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb size={16} className="text-[var(--color-accent)]" />
                <span className="text-sm font-bold text-[var(--color-text-primary)]">Challenge Feedback</span>
              </div>
              <div className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                <Markdown text={challengeFeedback} />
              </div>
            </div>
          )}
          {stars > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-text-muted)]">Stars earned:</span>
              <div className="flex gap-0.5">
                {[1, 2, 3].map((s) => (
                  <Star key={s} size={18} className={s <= stars ? "fill-[var(--color-star)] text-[var(--color-star)]" : "text-[var(--color-border)]"} />
                ))}
              </div>
            </div>
          )}
          <ConfidenceRating lessonTitle={lesson.title} onRate={setConfidence} />
            <div className="flex gap-3">
            <button
              onClick={async () => {
                const nextAttempt = attempts + 1;
                setAttempts(nextAttempt);
                setChallengeFeedback("");
                try {
                  const { executePython } = await import("@/lib/api");
                  const result = await executePython(challengeCode);
                  setChallengeResult({ output: result.output, error: result.error || undefined });
                  
                  if (!result.error) {
                    const output = result.output || "";
                    const failedOutputChecks = (lesson.challenge?.tests || []).filter((test) =>
                      test.type === "output_contains" &&
                      test.value !== undefined &&
                      !output.includes(String(test.value))
                    );
                    const failedCodeChecks = (lesson.challenge?.tests || []).filter((test) =>
                      test.type === "code_contains" &&
                      test.value !== undefined &&
                      !challengeCode.includes(String(test.value))
                    );

                    if (failedOutputChecks.length || failedCodeChecks.length) {
                      setStars(0);
                      const missingValues = [...failedOutputChecks, ...failedCodeChecks]
                        .map((test) => String(test.value))
                        .filter(Boolean)
                        .join(", ");
                      setChallengeFeedback(
                        `Your code ran, but it did not satisfy every challenge check. Missing expected item${missingValues.includes(",") ? "s" : ""}: ${missingValues}.`
                      );
                    } else {
                      const newStars = nextAttempt === 1 ? 3 : nextAttempt === 2 ? 2 : 1;
                      setStars(newStars);
                      setChallengeFeedback(
                        nextAttempt === 1
                          ? "Your code ran successfully and met the challenge checks on the first attempt."
                          : "Your code ran successfully and met the challenge checks. Review the solution after completion if you want to compare approaches."
                      );
                    }
                  } else {
                    setStars(0);
                    setChallengeFeedback(
                      "The code stopped with an error. Read the error output first, then check variable names, imports, indentation, and whether the expected print statement is present."
                    );
                  }
                } catch (err: unknown) {
                  setChallengeResult({ error: String(err) });
                  setChallengeFeedback("The code runner could not complete the request. Confirm the backend is running on the Windows PC and try again.");
                }
              }}
              className="flex-1 py-3 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] text-white rounded-xl text-sm font-semibold transition-all"
            >
              Run Code
            </button>
            {attempts >= 3 && stars === 0 && lesson.challenge?.solution && (
              <button
                onClick={() => {
                  setChallengeCode(lesson.challenge!.solution || "");
                  setChallengeFeedback("Here is the solution. Study it carefully, then try modifying it to understand how it works.");
                }}
                className="px-4 py-3 bg-yellow-600/20 border border-yellow-600/50 text-yellow-400 rounded-xl text-sm font-medium hover:bg-yellow-600/30 transition-all"
              >
                Reveal Solution
              </button>
            )}
            <button
              onClick={handleComplete}
              className="flex-1 py-3 bg-[var(--color-success)] hover:opacity-90 text-white rounded-xl text-sm font-semibold transition-all"
            >
              Complete Lesson
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
