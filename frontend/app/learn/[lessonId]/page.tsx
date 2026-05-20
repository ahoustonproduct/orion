"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import dynamic from "next/dynamic";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle,
  ChevronLeft,
  ChevronRight,
  Code,
  HelpCircle,
  Lightbulb,
  Play,
  Save,
  Star,
  XCircle,
} from "lucide-react";
import {
  addToReviewQueue,
  executePython,
  fetchBookmark,
  fetchLesson,
  fetchModules,
  fetchNotebook,
  recordMastery,
  saveBookmark,
  saveConfidence,
  saveProgress,
  type Lesson,
  type Question,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import ConfidenceRating from "@/components/ConfidenceRating";
import WorkedExample from "@/components/WorkedExample";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

type Step = "concept" | "questions" | "challenge";
type AnswerValue = string | number | boolean | number[];
type ChallengeResult = { output?: string; error?: string };

interface AnswerState {
  answer: AnswerValue;
  correct: boolean;
}

const STEP_ORDER: Step[] = ["concept", "questions", "challenge"];

function stepFromIndex(index: number): Step {
  return STEP_ORDER[Math.max(0, Math.min(index, STEP_ORDER.length - 1))];
}

function indexFromStep(step: Step): number {
  return STEP_ORDER.indexOf(step);
}

function notebookIdFromLessonId(id: string): string | null {
  if (!id.startsWith("notebook_")) return null;
  const lessonSuffixIndex = id.lastIndexOf("-l");
  return lessonSuffixIndex > 0 ? id.slice(0, lessonSuffixIndex) : null;
}

function normalizeText(value: unknown): string {
  return String(value ?? "").trim().toLowerCase();
}

function arraysEqual(left: number[], right: number[]) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function parseOrderInput(value: string): number[] {
  return value
    .split(/[,\s]+/)
    .map((part) => Number(part.trim()))
    .filter((part) => Number.isFinite(part));
}

function isAnswerCorrect(expected: Question["answer"], answer: AnswerValue) {
  if (Array.isArray(expected)) {
    if (!Array.isArray(answer)) return false;
    return arraysEqual(answer, expected) || arraysEqual(answer.map((value) => value - 1), expected);
  }

  if (typeof expected === "string") {
    return normalizeText(expected) === normalizeText(answer);
  }

  return expected === answer;
}

function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeSanitize]}
      components={{
        pre: ({ children }) => (
          <pre className="my-4 overflow-x-auto rounded-xl border border-[var(--color-border)] bg-[#161413] p-4">
            {children}
          </pre>
        ),
        code: ({ className, children }) => {
          const isBlock = Boolean(className);
          return isBlock ? (
            <code className={`${className} text-[13px] leading-relaxed text-[#f5f0e8]`}>{children}</code>
          ) : (
            <code className="rounded border border-[var(--color-border)] bg-[var(--color-surface-2)] px-1.5 py-0.5 text-sm text-[var(--color-accent)]">
              {children}
            </code>
          );
        },
        p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
        ul: ({ children }) => <ul className="mb-3 ml-6 list-disc space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="mb-3 ml-6 list-decimal space-y-1">{children}</ol>,
        blockquote: ({ children }) => (
          <blockquote className="my-4 border-l-4 border-[var(--color-accent)] bg-[var(--color-surface)] px-4 py-3 text-[var(--color-text-primary)]">
            {children}
          </blockquote>
        ),
        strong: ({ children }) => <strong className="font-semibold text-[var(--color-text-primary)]">{children}</strong>,
        h2: ({ children }) => <h2 className="mb-3 mt-7 text-xl font-bold text-[var(--color-text-primary)]">{children}</h2>,
        h3: ({ children }) => <h3 className="mb-2 mt-5 text-lg font-bold text-[var(--color-text-primary)]">{children}</h3>,
      }}
    >
      {text}
    </ReactMarkdown>
  );
}

export default function LessonPage() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const userKey = getUserKey();
  const startTimeRef = useRef(Date.now());

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [step, setStep] = useState<Step>("concept");
  const [completed, setCompleted] = useState(false);
  const [currentQ, setCurrentQ] = useState(0);
  const [answersByQuestion, setAnswersByQuestion] = useState<Record<number, AnswerState>>({});
  const [typedAnswers, setTypedAnswers] = useState<Record<number, string>>({});
  const [challengeCode, setChallengeCode] = useState("");
  const [challengeResult, setChallengeResult] = useState<ChallengeResult | null>(null);
  const [challengePassed, setChallengePassed] = useState(false);
  const [runningCode, setRunningCode] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [stars, setStars] = useState(0);
  const [confidence, setConfidence] = useState(0);
  const [challengeFeedback, setChallengeFeedback] = useState("");
  const [nextLessonId, setNextLessonId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setLesson(null);
    setStep("concept");
    setCompleted(false);
    setCurrentQ(0);
    setAnswersByQuestion({});
    setTypedAnswers({});
    setChallengeCode("");
    setChallengeResult(null);
    setChallengePassed(false);
    setRunningCode(false);
    setAttempts(0);
    setStars(0);
    setConfidence(0);
    setChallengeFeedback("");
    setNextLessonId(null);
    startTimeRef.current = Date.now();

    Promise.all([
      fetchLesson(lessonId, userKey),
      fetchBookmark(userKey, lessonId).catch(() => null),
    ])
      .then(([loadedLesson, bookmark]) => {
        if (cancelled) return;
        setLesson(loadedLesson);
        const starterCode = loadedLesson.challenge?.starter_code || "";
        setChallengeCode(bookmark?.found && bookmark.saved_code ? bookmark.saved_code : starterCode);
        if (bookmark?.found) {
          setStep(stepFromIndex(bookmark.step_index));
          setCurrentQ(Math.min(bookmark.sub_step || 0, Math.max((loadedLesson.questions?.length || 1) - 1, 0)));
        }
        setLoading(false);
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });

    const notebookId = notebookIdFromLessonId(lessonId);
    if (notebookId) {
      fetchNotebook(userKey, notebookId)
        .then((notebook) => {
          if (cancelled) return;
          const lessons = notebook.module_data?.lessons || [];
          const currentIndex = lessons.findIndex((item) => item.id === lessonId);
          setNextLessonId(currentIndex >= 0 ? lessons[currentIndex + 1]?.id ?? null : null);
        })
        .catch(() => !cancelled && setNextLessonId(null));
    } else {
      fetchModules()
        .then((modules) => {
          if (cancelled) return;
          const allLessons = modules.flatMap((module) => module.lessons || []);
          const currentIndex = allLessons.findIndex((item) => item.id === lessonId);
          setNextLessonId(currentIndex >= 0 ? allLessons[currentIndex + 1]?.id ?? null : null);
        })
        .catch(() => !cancelled && setNextLessonId(null));
    }

    return () => {
      cancelled = true;
    };
  }, [lessonId, userKey]);

  useEffect(() => {
    if (!lesson || loading) return;
    const handle = window.setTimeout(() => {
      void saveBookmark(userKey, {
        lesson_id: lessonId,
        step_index: indexFromStep(step),
        sub_step: step === "questions" ? currentQ : 0,
        saved_code: challengeCode,
      }).catch((error) => console.error("Failed to save bookmark:", error));
    }, step === "challenge" ? 800 : 150);

    return () => window.clearTimeout(handle);
  }, [lesson, loading, userKey, lessonId, step, currentQ, challengeCode]);

  const questionCount = lesson?.questions.length || 0;
  const answeredCount = Object.keys(answersByQuestion).length;
  const correctCount = Object.values(answersByQuestion).filter((answer) => answer.correct).length;
  const practiceComplete = questionCount === 0 || correctCount === questionCount;
  const notebookId = notebookIdFromLessonId(lessonId);
  const backHref = notebookId ? `/notebooks/${notebookId}` : "/curriculum";

  const goToStep = (nextStep: Step) => {
    if (nextStep === "challenge" && !practiceComplete) return;
    setStep(nextStep);
  };

  const goToQuestion = (index: number) => {
    if (!lesson?.questions.length) return;
    setCurrentQ(Math.max(0, Math.min(index, lesson.questions.length - 1)));
  };

  const submitAnswer = (question: Question, answer: AnswerValue) => {
    if (!lesson) return;
    const correct = isAnswerCorrect(question.answer, answer);
    setAnswersByQuestion((previous) => ({
      ...previous,
      [currentQ]: { answer, correct },
    }));

    const questionId = `${lessonId}:q${currentQ + 1}`;
    void recordMastery(userKey, lesson.title, correct).catch(() => undefined);
    if (!correct) {
      void addToReviewQueue(
        userKey,
        questionId,
        lessonId,
        JSON.stringify({ ...question, lesson_id: lessonId }),
      ).catch(() => undefined);
    }
  };

  const submitTypedAnswer = (question: Question) => {
    const rawValue = typedAnswers[currentQ] || "";
    if (!rawValue.trim()) return;
    const answer = question.type === "code_ordering" ? parseOrderInput(rawValue) : rawValue.trim();
    submitAnswer(question, answer);
  };

  const handleRunCode = async () => {
    if (!lesson) return;
    const nextAttempt = attempts + 1;
    setAttempts(nextAttempt);
    setRunningCode(true);
    setChallengePassed(false);
    setCompleted(false);
    setChallengeFeedback("");

    try {
      const result = await executePython(challengeCode);
      setChallengeResult({ output: result.output, error: result.error || undefined });

      if (result.error) {
        setStars(0);
        setChallengeFeedback("The code stopped with an error. Read the output, fix the smallest failing piece, and run it again.");
        void recordMastery(userKey, lesson.title, false).catch(() => undefined);
        return;
      }

      const output = result.output || "";
      const failedOutputChecks = (lesson.challenge?.tests || []).filter((test) =>
        test.type === "output_contains" && test.value !== undefined && !output.includes(String(test.value)),
      );
      const failedCodeChecks = (lesson.challenge?.tests || []).filter((test) =>
        test.type === "code_contains" && test.value !== undefined && !challengeCode.includes(String(test.value)),
      );

      if (failedOutputChecks.length || failedCodeChecks.length) {
        const missingValues = [...failedOutputChecks, ...failedCodeChecks]
          .map((test) => String(test.value))
          .filter(Boolean)
          .join(", ");
        setStars(0);
        setChallengeFeedback(`Your code ran, but it did not satisfy every challenge check. Missing: ${missingValues}.`);
        void recordMastery(userKey, lesson.title, false).catch(() => undefined);
        return;
      }

      const earnedStars = nextAttempt === 1 ? 3 : nextAttempt === 2 ? 2 : 1;
      setStars(earnedStars);
      setChallengePassed(true);
      setChallengeFeedback("Your code ran successfully and satisfied the challenge checks. You can save the lesson now.");
      void recordMastery(userKey, lesson.title, true).catch(() => undefined);
    } catch (error) {
      setChallengeResult({ error: String(error) });
      setChallengeFeedback("The code runner could not complete the request. Confirm the backend is running and try again.");
    } finally {
      setRunningCode(false);
    }
  };

  const handleRevealSolution = () => {
    setChallengeCode(lesson?.challenge?.solution || "");
    setChallengePassed(false);
    setCompleted(false);
    setChallengeFeedback("Solution loaded. Study it, run it, then modify it until the calculation makes sense.");
  };

  const handleComplete = async () => {
    if (!challengePassed) {
      setChallengeFeedback("Run the code and satisfy the challenge checks before completing this lesson.");
      return;
    }

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
      await saveBookmark(userKey, {
        lesson_id: lessonId,
        step_index: indexFromStep("challenge"),
        sub_step: 0,
        saved_code: challengeCode,
      });
      if (confidence > 0) {
        await saveConfidence(userKey, lessonId, confidence);
      }
      setCompleted(true);
    } catch (error) {
      console.error("Failed to save progress:", error);
      setChallengeFeedback("The lesson passed, but progress could not be saved. Check the backend and try Complete Lesson again.");
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="space-y-3 text-center">
          <div className="mx-auto flex h-10 w-10 animate-pulse items-center justify-center rounded-xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent-light)]">
            <span className="font-bold text-white">O</span>
          </div>
          <p className="text-sm text-[var(--color-text-muted)]">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12 text-center">
        <p className="mb-4 text-[var(--color-text-secondary)]">Lesson not found.</p>
        <Link href="/curriculum" className="text-sm text-[var(--color-accent)] hover:underline">
          Back to Curriculum
        </Link>
      </div>
    );
  }

  const steps: { key: Step; label: string; icon: typeof BookOpen }[] = [
    { key: "concept", label: "Learn", icon: BookOpen },
    { key: "questions", label: "Practice", icon: HelpCircle },
    { key: "challenge", label: "Challenge", icon: Code },
  ];
  const stepIndex = steps.findIndex((item) => item.key === step);
  const currentQuestion = lesson.questions[currentQ];
  const currentAnswer = answersByQuestion[currentQ];
  const typedAnswer = typedAnswers[currentQ] || "";
  const hasWorkedExample = Boolean(
    lesson.worked_example?.description || lesson.worked_example?.code || lesson.worked_example?.explanation,
  );

  return (
    <div className="mx-auto max-w-4xl space-y-5 px-4 py-6">
      <div className="flex items-center gap-3">
        <Link href={backHref} className="text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]">
          <ArrowLeft size={18} />
        </Link>
        <div className="min-w-0 flex-1">
          <p className="text-xs text-[var(--color-text-muted)]">{lesson.module_title}</p>
          <h1 className="truncate text-lg font-bold text-[var(--color-text-primary)]">{lesson.title}</h1>
        </div>
      </div>

      <div className="flex gap-1 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] p-1">
        {steps.map((item, index) => {
          const Icon = item.icon;
          const isActive = item.key === step;
          const isDone = index < stepIndex || (item.key === "questions" && practiceComplete);
          const disabled = item.key === "challenge" && !practiceComplete;

          return (
            <button
              key={item.key}
              type="button"
              onClick={() => goToStep(item.key)}
              disabled={disabled}
              className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition-all disabled:cursor-not-allowed disabled:opacity-45 ${
                isActive
                  ? "border border-[var(--color-border)] bg-[var(--color-surface)] text-[var(--color-accent)] shadow-sm"
                  : isDone
                    ? "text-[var(--color-success)]"
                    : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
              }`}
            >
              {isDone ? <CheckCircle size={14} /> : <Icon size={14} />}
              {item.label}
            </button>
          );
        })}
      </div>

      {step === "concept" && (
        <div className="space-y-4">
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] p-8">
            <Markdown text={lesson.concept} />
          </div>

          {hasWorkedExample && (
            <WorkedExample
              description={lesson.worked_example?.description || ""}
              code={lesson.worked_example?.code || ""}
              explanation={lesson.worked_example?.explanation || ""}
            />
          )}

          {lesson.reference?.key_syntax?.length > 0 && (
            <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] p-4">
              <div className="mb-3 flex items-center gap-2">
                <Lightbulb size={14} className="text-[var(--color-star)]" />
                <span className="text-xs font-semibold text-[var(--color-text-secondary)]">Quick Reference</span>
              </div>
              <div className="space-y-1">
                {lesson.reference.key_syntax.map((syntax, index) => (
                  <code key={`${syntax}-${index}`} className="block font-mono text-xs text-[var(--color-accent)]">
                    {syntax}
                  </code>
                ))}
              </div>
              {lesson.reference.notes && (
                <p className="mt-2 text-xs text-[var(--color-text-muted)]">{lesson.reference.notes}</p>
              )}
            </div>
          )}

          <button
            type="button"
            onClick={() => goToStep("questions")}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)]"
          >
            Continue to Practice <ChevronRight size={16} />
          </button>
        </div>
      )}

      {step === "questions" && currentQuestion && (
        <div className="space-y-4">
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
            <div className="mb-4 flex items-center justify-between">
              <span className="text-xs text-[var(--color-text-muted)]">Question {currentQ + 1} of {questionCount}</span>
              <span className="text-xs font-medium text-[var(--color-success)]">{correctCount}/{questionCount} mastered</span>
            </div>

            <div className="space-y-4">
              <p className="text-sm font-medium text-[var(--color-text-primary)]">{currentQuestion.question}</p>

              {currentQuestion.type === "multiple_choice" && currentQuestion.options && (
                <div className="space-y-2">
                  {currentQuestion.options.map((option, index) => {
                    const selected = currentAnswer?.answer === index;
                    const correct = index === currentQuestion.answer;
                    const showResult = Boolean(currentAnswer);

                    return (
                      <button
                        key={`${option}-${index}`}
                        type="button"
                        onClick={() => submitAnswer(currentQuestion, index)}
                        className={`w-full rounded-lg border px-4 py-3 text-left text-sm transition-all ${
                          showResult && correct
                            ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                            : showResult && selected && !correct
                              ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                              : "border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
                        }`}
                      >
                        <span className="mr-2 font-medium">{String.fromCharCode(65 + index)}.</span>
                        {option}
                        {showResult && correct && <CheckCircle size={14} className="ml-2 inline text-[var(--color-success)]" />}
                        {showResult && selected && !correct && <XCircle size={14} className="ml-2 inline text-[var(--color-error)]" />}
                      </button>
                    );
                  })}
                </div>
              )}

              {currentQuestion.type === "true_false" && (
                <div className="flex gap-3">
                  {[true, false].map((value) => {
                    const selected = currentAnswer?.answer === value;
                    const correct = value === currentQuestion.answer;
                    const showResult = Boolean(currentAnswer);

                    return (
                      <button
                        key={String(value)}
                        type="button"
                        onClick={() => submitAnswer(currentQuestion, value)}
                        className={`flex-1 rounded-lg border py-3 text-sm font-medium transition-all ${
                          showResult && correct
                            ? "border-[var(--color-success)] bg-[var(--color-success)]/10 text-[var(--color-success)]"
                            : showResult && selected && !correct
                              ? "border-[var(--color-error)] bg-[var(--color-error)]/10 text-[var(--color-error)]"
                              : "border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-text-primary)] hover:border-[var(--color-accent)]"
                        }`}
                      >
                        {String(value)}
                      </button>
                    );
                  })}
                </div>
              )}

              {currentQuestion.type === "code_ordering" && currentQuestion.lines && (
                <div className="space-y-3">
                  <div className="space-y-2">
                    {currentQuestion.lines.map((line, index) => (
                      <code
                        key={`${line}-${index}`}
                        className="block rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-2)] p-3 font-mono text-sm text-[var(--color-text-primary)]"
                      >
                        {index + 1}. {line}
                      </code>
                    ))}
                  </div>
                  <div className="flex flex-col gap-2 sm:flex-row">
                    <input
                      value={typedAnswer}
                      onChange={(event) => setTypedAnswers((previous) => ({ ...previous, [currentQ]: event.target.value }))}
                      placeholder="Enter order, e.g. 1, 3, 2"
                      className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-2)] px-3 py-2 text-sm text-[var(--color-text-primary)] outline-none transition-colors placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)]"
                    />
                    <button
                      type="button"
                      onClick={() => submitTypedAnswer(currentQuestion)}
                      className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white"
                    >
                      Check Order
                    </button>
                  </div>
                </div>
              )}

              {(currentQuestion.type === "fill_blank" || currentQuestion.type === "debug") && (
                <div className="space-y-3">
                  {currentQuestion.template && (
                    <code className="block rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-2)] p-3 font-mono text-sm text-[var(--color-text-primary)]">
                      {currentQuestion.template}
                    </code>
                  )}
                  {currentQuestion.broken_code && (
                    <pre className="overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[#161413] p-3 text-sm text-[#f5f0e8]">
                      <code>{currentQuestion.broken_code}</code>
                    </pre>
                  )}
                  <div className="flex flex-col gap-2 sm:flex-row">
                    <input
                      value={typedAnswer}
                      onChange={(event) => setTypedAnswers((previous) => ({ ...previous, [currentQ]: event.target.value }))}
                      onKeyDown={(event) => {
                        if (event.key === "Enter") submitTypedAnswer(currentQuestion);
                      }}
                      placeholder="Type your answer..."
                      className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-2)] px-3 py-2 text-sm text-[var(--color-text-primary)] outline-none transition-colors placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)]"
                    />
                    <button
                      type="button"
                      onClick={() => submitTypedAnswer(currentQuestion)}
                      disabled={!typedAnswer.trim()}
                      className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      Submit
                    </button>
                  </div>
                </div>
              )}

              {currentAnswer && (
                <div className={`rounded-lg border p-3 text-xs ${
                  currentAnswer.correct
                    ? "border-[var(--color-success)]/30 bg-[var(--color-success)]/10 text-[var(--color-success)]"
                    : "border-[var(--color-error)]/30 bg-[var(--color-error)]/10 text-[var(--color-error)]"
                }`}>
                  <span className="font-semibold">{currentAnswer.correct ? "Correct." : "Not yet."}</span>{" "}
                  <span>{currentQuestion.explanation}</span>
                </div>
              )}
            </div>
          </div>

          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <button
                type="button"
                onClick={() => goToQuestion(currentQ - 1)}
                disabled={currentQ <= 0}
                className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-all hover:border-[var(--color-accent)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
              >
                <ChevronLeft size={16} />
                Previous Question
              </button>
              <div className="flex-1 text-center text-xs text-[var(--color-text-muted)]">
                {answeredCount} answered, {correctCount} mastered
              </div>
              <button
                type="button"
                onClick={() => goToQuestion(currentQ + 1)}
                disabled={currentQ >= questionCount - 1}
                className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-medium text-[var(--color-text-primary)] transition-all hover:border-[var(--color-accent)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
              >
                Next Question
                <ChevronRight size={16} />
              </button>
              <button
                type="button"
                onClick={() => goToStep("challenge")}
                disabled={!practiceComplete}
                className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)] disabled:cursor-not-allowed disabled:opacity-40 sm:w-44"
              >
                Go to Challenge
                <ChevronRight size={16} />
              </button>
            </div>
            {!practiceComplete && (
              <p className="mt-2 text-center text-xs text-[var(--color-text-muted)]">
                Correct every practice question before moving into the coding challenge.
              </p>
            )}
          </div>
        </div>
      )}

      {step === "challenge" && (
        <div className="space-y-4">
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
            <h3 className="mb-2 text-sm font-bold text-[var(--color-text-primary)]">Coding Challenge</h3>
            <p className="text-sm text-[var(--color-text-secondary)]">{lesson.challenge?.instructions}</p>
          </div>

          <div className="overflow-hidden rounded-xl border border-[#2C2520] bg-[#14110F]">
            <MonacoEditor
              value={challengeCode}
              language="python"
              theme="vs-dark"
              onChange={(value) => {
                setChallengeCode(value ?? "");
                setChallengePassed(false);
                setCompleted(false);
              }}
              height="340px"
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

          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-3">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div className="flex flex-col gap-2 sm:flex-row">
                <button
                  type="button"
                  onClick={handleRunCode}
                  disabled={runningCode}
                  className="flex items-center justify-center gap-2 rounded-xl bg-[var(--color-accent)] px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent-hover)] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <Play size={16} />
                  {runningCode ? "Running..." : "Run Code"}
                </button>
                {attempts >= 3 && stars === 0 && lesson.challenge?.solution && (
                  <button
                    type="button"
                    onClick={handleRevealSolution}
                    className="rounded-xl border border-[var(--color-warning)]/40 bg-[var(--color-warning)]/10 px-4 py-3 text-sm font-medium text-[var(--color-warning)] transition-all hover:bg-[var(--color-warning)]/15"
                  >
                    Reveal Solution
                  </button>
                )}
              </div>

              <div className="flex flex-col gap-2 sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={handleComplete}
                  disabled={!challengePassed || completed}
                  className="flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] px-4 py-3 text-sm font-semibold text-[var(--color-text-primary)] transition-all hover:border-[var(--color-success)] disabled:cursor-not-allowed disabled:opacity-55"
                  title={challengePassed ? "Save lesson progress" : "Run and pass the challenge first"}
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
                    type="button"
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
                <span>Progress saved. Practice: {correctCount}/{questionCount} mastered. Attempts: {attempts || 1}.</span>
                <span className="flex gap-0.5">
                  {[1, 2, 3].map((star) => (
                    <Star
                      key={star}
                      size={14}
                      className={star <= Math.max(stars, 1) ? "fill-[var(--color-star)] text-[var(--color-star)]" : "text-[var(--color-border)]"}
                    />
                  ))}
                </span>
              </div>
            )}
          </div>

          {challengeResult && (
            <div className={`rounded-xl p-4 ${
              challengeResult.error
                ? "border border-[var(--color-error)]/30 bg-[var(--color-error)]/10"
                : "border border-[var(--color-success)]/30 bg-[var(--color-success)]/10"
            }`}>
              {challengeResult.error ? (
                <div>
                  <p className="mb-1 text-xs font-semibold text-[var(--color-error)]">Error</p>
                  <pre className="whitespace-pre-wrap font-mono text-xs text-[var(--color-error)]">{challengeResult.error}</pre>
                </div>
              ) : (
                <div>
                  <p className="mb-1 text-xs font-semibold text-[var(--color-success)]">Output</p>
                  <pre className="whitespace-pre-wrap font-mono text-xs text-[var(--color-success)]">{challengeResult.output || "(no output)"}</pre>
                </div>
              )}
            </div>
          )}

          {challengeFeedback && (
            <div className="relative overflow-hidden rounded-xl border border-[var(--color-accent)]/30 bg-[var(--color-surface)] p-5">
              <div className="absolute left-0 top-0 h-full w-1 bg-[var(--color-accent)]" />
              <div className="mb-2 flex items-center gap-2">
                <Lightbulb size={16} className="text-[var(--color-accent)]" />
                <span className="text-sm font-bold text-[var(--color-text-primary)]">Challenge Feedback</span>
              </div>
              <div className="text-sm leading-relaxed text-[var(--color-text-secondary)]">
                <Markdown text={challengeFeedback} />
              </div>
            </div>
          )}

          {stars > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-text-muted)]">Stars earned:</span>
              <div className="flex gap-0.5">
                {[1, 2, 3].map((star) => (
                  <Star
                    key={star}
                    size={18}
                    className={star <= stars ? "fill-[var(--color-star)] text-[var(--color-star)]" : "text-[var(--color-border)]"}
                  />
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
