"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  fetchLesson, saveProgress, saveConfidence, fetchModules, fetchNotebook,
  type Lesson, type Question
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import {
  ArrowLeft, CheckCircle, XCircle, Lightbulb, Code,
  ChevronRight, ChevronLeft, BookOpen, HelpCircle, Star, Play, Save, ArrowRight
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import dynamic from "next/dynamic";
import ConfidenceRating from "@/components/ConfidenceRating";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

type Step = "concept" | "questions" | "challenge";
type AnswerValue = string | number | boolean;

interface AnswerState {
  answer: AnswerValue;
  correct: boolean;
}

function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeSanitize]}
      components={{
        pre: ({ children }) => (
          <pre className="bg-[#161413] border border-[var(--color-border)] rounded-xl p-4 my-4 overflow-x-auto">
            {children}
          </pre>
        ),
        code: ({ className, children }) => {
          const isBlock = Boolean(className);
          return isBlock
            ? <code className={`${className} text-[13px] leading-relaxed text-[#f5f0e8]`}>{children}</code>
            : <code className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded px-1.5 py-0.5 text-sm text-[var(--color-accent)]">{children}</code>;
        },
        p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
        ul: ({ children }) => <ul className="list-disc ml-6 mb-3 space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal ml-6 mb-3 space-y-1">{children}</ol>,
        blockquote: ({ children }) => (
          <blockquote className="my-4 border-l-4 border-[var(--color-accent)] bg-[var(--color-surface)] px-4 py-3 text-[var(--color-text-primary)]">
            {children}
          </blockquote>
        ),
        strong: ({ children }) => <strong className="font-semibold text-[var(--color-text-primary)]">{children}</strong>,
        h2: ({ children }) => <h2 className="text-xl font-bold text-[var(--color-text-primary)] mt-7 mb-3">{children}</h2>,
        h3: ({ children }) => <h3 className="text-lg font-bold text-[var(--color-text-primary)] mt-5 mb-2">{children}</h3>,
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
  const [selectedAnswer, setSelectedAnswer] = useState<AnswerValue | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [answersByQuestion, setAnswersByQuestion] = useState<Record<number, AnswerState>>({});

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
    setLoading(true);
    setLesson(null);
    setStep("concept");
    setCompleted(false);
    setCurrentQ(0);
    setSelectedAnswer(null);
    setShowAnswer(false);
    setAnswersByQuestion({});
    setChallengeCode("");
    setChallengeResult(null);
    setAttempts(0);
    setStars(0);
    setConfidence(0);
    setChallengeFeedback("");
    setNextLessonId(null);
    setFillInput("");
    startTimeRef.current = Date.now();

    fetchLesson(lessonId, userKey)
      .then((l) => {
        setLesson(l);
        setChallengeCode(l.challenge?.starter_code || "");
        setLoading(false);
      })
      .catch(() => setLoading(false));

    // Pre-calculate next lesson ID so it's ready upon completion.
    if (lessonId.startsWith("notebook_")) {
      const notebookId = lessonId.split("-", 1)[0];
      fetchNotebook(userKey, notebookId)
        .then((notebook) => {
          const lessons = notebook.module_data?.lessons || [];
          const currentIndex = lessons.findIndex((l) => l.id === lessonId);
          setNextLessonId(currentIndex >= 0 ? lessons[currentIndex + 1]?.id ?? null : null);
        })
        .catch(() => setNextLessonId(null));
      return;
    }

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
  }, [lessonId, userKey]);

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

  const handleRunCode = async () => {
    if (!lesson) return;

    const nextAttempt = attempts + 1;
    setAttempts(nextAttempt);
    setChallengeFeedback("");
    setCompleted(false);

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
  };

  const handleRevealSolution = () => {
    setChallengeCode(lesson?.challenge?.solution || "");
    setChallengeFeedback("Here is the solution. Study it carefully, then try modifying it to understand how it works.");
    setCompleted(false);
  };

  const checkAnswer = (q: Question, answer: AnswerValue) => {
    setSelectedAnswer(answer);
    setShowAnswer(true);
    const isCorrect = answer === q.answer;
    setAnswersByQuestion((previous) => ({
      ...previous,
      [currentQ]: { answer, correct: isCorrect },
    }));
  };

  const goToQuestion = (index: number) => {
    if (!lesson?.questions.length) return;
    const nextIndex = Math.max(0, Math.min(index, lesson.questions.length - 1));
    const saved = answersByQuestion[nextIndex];
    setCurrentQ(nextIndex);
    setSelectedAnswer(saved?.answer ?? null);
    setShowAnswer(Boolean(saved));
    setFillInput("");
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

  const notebookId = lessonId.startsWith("notebook_") ? lessonId.split("-", 1)[0] : null;
  const backHref = notebookId ? `/notebooks/${notebookId}` : "/curriculum";
  const questionCount = lesson.questions.length;
  const answeredCount = Object.keys(answersByQuestion).length;
  const correctCount = Object.values(answersByQuestion).filter((answer) => answer.correct).length;
  const practiceComplete = questionCount > 0 && answeredCount === questionCount;

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
        <Link href={backHref} className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]">
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
              <span className="text-xs text-[var(--color-text-muted)]">Question {currentQ + 1} of {questionCount}</span>
              <span className="text-xs text-[var(--color-success)] font-medium">{correctCount}/{answeredCount || 0} correct</span>
            </div>
            {(() => {
              const q = lesson.questions[currentQ];
              const savedAnswer = answersByQuestion[currentQ];
              const displayAnswer = savedAnswer?.answer ?? selectedAnswer;
              const shouldShowAnswer = showAnswer || Boolean(savedAnswer);
              return (
                <div key={currentQ} className="space-y-4">
                  <p className="text-sm font-medium text-[var(--color-text-primary)]">{q.question}</p>
                  {q.type === "multiple_choice" && q.options && (
                    <div className="space-y-2">
                      {q.options.map((opt: string, i: number) => {
                        const isSelected = displayAnswer === i;
                        const isCorrect = i === q.answer;
                        const showResult = shouldShowAnswer;
                        return (
                          <button
                            key={i}
                            onClick={() => !showResult && checkAnswer(q, i)}
                            disabled={showResult}
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
                        const isSelected = displayAnswer === val;
                        const isCorrect = val === q.answer;
                        const showResult = shouldShowAnswer;
                        return (
                          <button
                            key={String(val)}
                            onClick={() => !showResult && checkAnswer(q, val)}
                            disabled={showResult}
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
                      {shouldShowAnswer ? (
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
                  {shouldShowAnswer && (
                    <div className="bg-[var(--color-surface-2)] border border-[var(--color-border)] rounded-lg p-3 text-xs text-[var(--color-text-secondary)]">
                      <span className="font-medium text-[var(--color-text-primary)]">Explanation:</span> {q.explanation}
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-3">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <button
                onClick={() => goToQuestion(currentQ - 1)}
                disabled={currentQ <= 0}
                className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-all hover:border-[var(--color-accent)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
              >
                <ChevronLeft size={16} />
                Previous Question
              </button>
              <div className="flex-1 text-center text-xs text-[var(--color-text-muted)]">
                {answeredCount} of {questionCount} answered
              </div>
              <button
                onClick={() => goToQuestion(currentQ + 1)}
                disabled={currentQ >= questionCount - 1}
                className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-all hover:border-[var(--color-accent)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
              >
                Next Question
                <ChevronRight size={16} />
              </button>
              <button
                onClick={() => practiceComplete && setStep("challenge")}
                disabled={!practiceComplete}
                className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
                title={practiceComplete ? "Go to the coding challenge" : "Answer all practice questions to unlock the challenge"}
              >
                Go to Challenge
                <ChevronRight size={16} />
              </button>
            </div>
            {!practiceComplete && (
              <p className="mt-2 text-center text-xs text-[var(--color-text-muted)]">
                Answer each practice question before moving into the coding challenge.
              </p>
            )}
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
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-3">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div className="flex flex-col gap-2 sm:flex-row">
                <button
                  onClick={handleRunCode}
                  className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)]"
                >
                  <Play size={16} />
                  Run Code
                </button>
                {attempts >= 3 && stars === 0 && lesson.challenge?.solution && (
                  <button
                    onClick={handleRevealSolution}
                    className="rounded-xl border border-[var(--color-warning)]/40 bg-[var(--color-warning)]/10 px-4 py-3 text-sm font-medium text-[var(--color-warning)] transition-all hover:bg-[var(--color-warning)]/15"
                  >
                    Reveal Solution
                  </button>
                )}
              </div>

              <div className="flex flex-col gap-2 sm:flex-row sm:justify-end">
                <button
                  onClick={handleComplete}
                  disabled={completed}
                  className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-semibold text-[var(--color-text-primary)] transition-all hover:border-[var(--color-success)] disabled:cursor-not-allowed disabled:opacity-55"
                >
                  <Save size={16} />
                  {completed ? "Lesson Saved" : "Complete Lesson"}
                </button>
                {completed && nextLessonId ? (
                  <Link
                    href={`/learn/${nextLessonId}`}
                    className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)]"
                  >
                    Go to Next Lesson
                    <ArrowRight size={16} />
                  </Link>
                ) : (
                  <button
                    disabled
                    className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white opacity-40"
                  >
                    Go to Next Lesson
                    <ArrowRight size={16} />
                  </button>
                )}
              </div>
            </div>
            {completed && (
              <div className="mt-3 flex flex-col gap-2 rounded-lg border border-[var(--color-success)]/30 bg-[var(--color-success)]/10 px-3 py-2 text-xs text-[var(--color-success)] sm:flex-row sm:items-center sm:justify-between">
                <span>Progress saved. Practice: {correctCount}/{questionCount} correct. Attempts: {attempts || 1}.</span>
                <span className="flex gap-0.5">
                  {[1, 2, 3].map((s) => (
                    <Star key={s} size={14} className={s <= Math.max(stars, 1) ? "fill-[var(--color-star)] text-[var(--color-star)]" : "text-[var(--color-border)]"} />
                  ))}
                </span>
              </div>
            )}
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
        </div>
      )}

    </div>
  );
}
