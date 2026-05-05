"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchModules, fetchProgress, fetchReviewQueue, fetchMastery, fetchNotebooks,
  type Module, type ProgressData, type ReviewQueue, type MasteryData, type NotebookSummary,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import {
  BookOpen, Star, Zap, ArrowRight, RefreshCw, AlertCircle, Box, Clock, CheckCircle,
} from "lucide-react";

interface DashboardClientProps {
  initialModules: Module[];
  initialModulesError: string | null;
}

export default function DashboardClient({
  initialModules,
  initialModulesError,
}: DashboardClientProps) {
  const [modules, setModules] = useState<Module[]>(initialModules);
  const [modulesError, setModulesError] = useState<string | null>(null);
  const [modulesLoading, setModulesLoading] = useState(initialModules.length === 0);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [reviewQueue, setReviewQueue] = useState<ReviewQueue | null>(null);
  const [mastery, setMastery] = useState<MasteryData | null>(null);
  const [notebooks, setNotebooks] = useState<NotebookSummary[]>([]);

  useEffect(() => {
    const userKey = getUserKey();

    if (initialModules.length === 0) {
      fetchModules()
        .then((loadedModules) => {
          setModules(loadedModules);
          setModulesError(null);
        })
        .catch((error) => {
          console.error(error);
          setModulesError(initialModulesError || "Modules could not be loaded from the backend.");
        })
        .finally(() => setModulesLoading(false));
    }

    fetchProgress(userKey)
      .then(setProgress)
      .catch(console.error);
    fetchReviewQueue(userKey).then(setReviewQueue).catch(() => null);
    fetchMastery(userKey).then(setMastery).catch(() => null);
    fetchNotebooks(userKey).then(setNotebooks).catch(() => null);
  }, [initialModules.length, initialModulesError]);

  const readyNotebooks = notebooks.filter((notebook) => notebook.status === "ready");
  const notebookLessonCount = readyNotebooks.reduce((s, n) => s + n.lesson_count, 0);
  const totalLessons = modules.reduce((s, m) => s + m.lesson_count, 0) + notebookLessonCount;
  const completedLessons = progress ? progress.lessons.filter((l) => l.completed).length : 0;
  const totalStars = progress ? progress.lessons.reduce((s, l) => s + l.stars, 0) : 0;
  const totalStudyMinutes = progress
    ? Math.round(Object.values(progress.study_log ?? {}).reduce((s, minutes) => s + minutes, 0))
    : 0;
  const overallPct = totalLessons ? Math.round((completedLessons / totalLessons) * 100) : 0;
  const nextModule = progress
    ? modules.find((module) => {
        const status = progress.module_status[module.id];
        return (status?.completed_count ?? 0) < module.lesson_count;
      })
    : modules[0];
  const nextNotebook = progress && !nextModule
    ? readyNotebooks.find((notebook) => {
        const status = progress.module_status[notebook.id];
        return (status?.completed_count ?? 0) < notebook.lesson_count;
      })
    : null;
  const nextStatusText = !progress
    ? "Progress is loading."
    : completedLessons === 0
    ? "Start with the first Python module and build momentum one lesson at a time."
    : nextModule
    ? `Continue ${nextModule.title}. You have completed ${completedLessons} of ${totalLessons} lessons.`
    : nextNotebook
    ? `Continue ${nextNotebook.title}. Saved modules now count toward your learning progress.`
    : "All visible curriculum modules are complete. Use review and quiz sessions to keep skills sharp.";

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 space-y-8 pb-20">
      <div className="flex items-center gap-5 animate-slide-up" style={{ animationDelay: "0.1s" }}>
        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-light)] rounded-2xl blur opacity-20" />
          <div className="relative w-16 h-16 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border)] flex items-center justify-center overflow-hidden">
            <span className="text-[var(--color-accent)] font-bold text-3xl">O</span>
          </div>
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-[var(--color-text-primary)] mb-1">
            Welcome Back
          </h1>
          <p className="text-[var(--color-text-secondary)] text-sm font-medium">Orion / WashU FinTech Analytics Prep</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 animate-slide-up" style={{ animationDelay: "0.2s" }}>
        <div className="md:col-span-5 grid grid-cols-2 gap-4">
          {[
            { icon: <Clock size={20} />, value: totalStudyMinutes, label: "Study Minutes", colSpan: "" },
            { icon: <BookOpen size={20} />, value: completedLessons, label: "Lessons Done", colSpan: "" },
            { icon: <Star size={20} />, value: totalStars, label: "Total Stars", colSpan: "col-span-2" },
          ].map(({ icon, value, label, colSpan }) => (
            <div key={label} className={`bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl relative overflow-hidden ${colSpan || ""}`}>
              <div className="relative z-10 flex flex-col gap-3">
                <div className="w-8 h-8 rounded-full flex items-center justify-center border border-[var(--color-border)] bg-[var(--color-surface-2)] text-[var(--color-accent)]">
                  {icon}
                </div>
                <div>
                  <div className="text-3xl font-black text-[var(--color-text-primary)]">{value}</div>
                  <div className="text-xs font-medium text-[var(--color-text-muted)] mt-1 uppercase tracking-wider">{label}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="md:col-span-7 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 relative overflow-hidden flex flex-col">
          <div className="absolute -inset-2 bg-gradient-to-br from-[var(--color-accent)]/10 via-transparent to-[var(--color-accent-light)]/5 z-0 pointer-events-none blur-xl" />

          <div className="relative z-10 flex items-center gap-3 mb-6">
            <div className="w-8 h-8 rounded-full bg-[var(--color-accent)]/20 border border-[var(--color-accent)]/30 flex items-center justify-center">
              <BookOpen size={14} className="text-[var(--color-accent)]" />
            </div>
            <h2 className="text-sm font-bold text-[var(--color-text-secondary)] uppercase tracking-widest">Curriculum Status</h2>
          </div>

          <div className="flex-1 flex flex-col justify-center">
            <div className="text-[var(--color-text-secondary)] leading-relaxed text-lg font-medium">
              <p className="border-l-2 border-[var(--color-accent)]/50 pl-4 py-1">{nextStatusText}</p>
            </div>
          </div>

          <div className="mt-6 pt-5 border-t border-[var(--color-border)] flex justify-between items-center">
            <div className="w-full">
              <div className="flex justify-between items-end mb-2">
                <span className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider">Curriculum Mastery</span>
                <span className="text-sm font-bold text-[var(--color-text-primary)]">{overallPct}% <span className="text-[var(--color-text-muted)] font-normal">/ 100%</span></span>
              </div>
              <div className="h-2 bg-[var(--color-surface-2)] rounded-full overflow-hidden border border-[var(--color-border)]">
                <div
                  className="h-full bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-light)] rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${overallPct}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-slide-up" style={{ animationDelay: "0.3s" }}>
        {reviewQueue && reviewQueue.total_due > 0 && (
          <Link
            href="/review-queue"
            className="group bg-[var(--color-surface)] border border-[var(--color-accent)]/30 p-5 rounded-2xl flex items-center justify-between overflow-hidden relative hover:border-[var(--color-accent)] transition-colors"
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/20 flex items-center justify-center">
                <RefreshCw size={20} className="text-[var(--color-accent)]" />
              </div>
              <div>
                <p className="font-bold text-[var(--color-text-primary)] mb-0.5">{reviewQueue.total_due} Review{reviewQueue.total_due !== 1 ? "s" : ""} Due</p>
                <p className="text-xs text-[var(--color-text-secondary)] font-medium">Spaced repetition queue requires attention</p>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-[var(--color-surface-2)] border border-[var(--color-border)] flex items-center justify-center group-hover:bg-[var(--color-accent)] transition-colors">
              <ArrowRight size={14} className="text-[var(--color-text-muted)] group-hover:text-white" />
            </div>
          </Link>
        )}

        {mastery && mastery.focus_areas.length > 0 && (
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl flex flex-col justify-center">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <AlertCircle size={14} className="text-[var(--color-warning)]" />
                <span className="text-xs font-bold text-[var(--color-text-secondary)] uppercase tracking-widest">Focus Areas</span>
              </div>
              <Link href="/progress" className="text-xs font-semibold text-[var(--color-accent)] hover:opacity-80 uppercase tracking-wider">Metrics</Link>
            </div>
            <div className="space-y-3">
              {mastery.focus_areas.slice(0, 2).map(({ tag, mastery: score }) => (
                <div key={tag} className="flex items-center gap-4">
                  <span className="text-sm font-medium text-[var(--color-text-secondary)] w-1/3 truncate capitalize">{tag.replace(/_/g, " ")}</span>
                  <div className="flex-1 h-1.5 bg-[var(--color-surface-2)] rounded-full overflow-hidden border border-[var(--color-border)]">
                    <div className="h-full bg-[var(--color-accent)] rounded-full" style={{ width: `${score}%` }} />
                  </div>
                  <span className="text-xs font-mono text-[var(--color-text-muted)] w-10 text-right">{score}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="animate-slide-up" style={{ animationDelay: "0.4s" }}>
        <div className="flex items-center gap-3 mb-6">
          <Box size={20} className="text-[var(--color-text-muted)]" />
          <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Learning Curriculum</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {modulesLoading && Array.from({ length: 2 }).map((_, index) => (
            <div
              key={`module-loading-${index}`}
              className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 space-y-4"
            >
              <div className="flex justify-between items-start">
                <div className="w-10 h-10 rounded-xl bg-[var(--color-surface-2)] animate-pulse" />
                <div className="w-16 h-6 rounded-full bg-[var(--color-surface-2)] animate-pulse" />
              </div>
              <div className="space-y-2">
                <div className="h-5 w-2/3 rounded bg-[var(--color-surface-2)] animate-pulse" />
                <div className="h-4 w-1/2 rounded bg-[var(--color-surface-2)] animate-pulse" />
              </div>
              <div className="h-2 rounded-full bg-[var(--color-surface-2)] animate-pulse" />
            </div>
          ))}

          {!modulesLoading && modules.length === 0 && readyNotebooks.length === 0 && (
            <div className="md:col-span-2 rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
              <p className="text-sm font-semibold text-[var(--color-text-primary)]">Modules unavailable</p>
              <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
                {modulesError || "The dashboard did not receive any curriculum modules."}
              </p>
            </div>
          )}

          {!modulesLoading && modules.map((module) => {
            const status = progress?.module_status[module.id];
            const completedInMod = status?.completed_count ?? 0;
            const masteryPct = status?.mastery_pct ?? 0;
            const pct = module.lesson_count ? (completedInMod / module.lesson_count) * 100 : 0;
            const isCompleted = pct === 100;

            return (
              <Link
                href={`/curriculum/${module.id}`}
                key={module.id}
                className="group relative overflow-hidden rounded-2xl transition-all duration-300 bg-[var(--color-surface)] border border-[var(--color-border)] hover:-translate-y-1 hover:shadow-xl cursor-pointer p-[1px] block"
              >
                <div className="bg-[var(--color-surface)] w-full h-full rounded-2xl p-6 relative z-10">
                  <div className="flex justify-between items-start mb-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm shadow-inner ${
                      isCompleted
                        ? "bg-[var(--color-success)]/20 text-[var(--color-success)] border border-[var(--color-success)]/30"
                        : "bg-[var(--color-accent)]/10 text-[var(--color-accent)] border border-[var(--color-accent)]/20"
                    }`}
                    >
                      {isCompleted ? <CheckCircle size={18} /> : module.order}
                    </div>

                    <div className="px-3 py-1 rounded-full bg-[var(--color-surface-2)] border border-[var(--color-border)] text-xs font-semibold text-[var(--color-text-secondary)] flex gap-1 items-center">
                      <span>{completedInMod}</span>
                      <span className="text-[var(--color-text-muted)]">/</span>
                      <span className="text-[var(--color-text-muted)]">{module.lesson_count}</span>
                    </div>
                  </div>

                  <div className="space-y-1 mb-5">
                    <h3 className="font-bold text-lg truncate text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)] transition-colors">
                      {module.title}
                    </h3>
                    <p className="text-sm text-[var(--color-text-muted)] font-medium truncate">{module.course}</p>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-1.5 bg-[var(--color-surface-2)] rounded-full overflow-hidden border border-[var(--color-border)]">
                      <div
                        className={`h-full rounded-full transition-all duration-700 ${isCompleted ? "bg-[var(--color-success)]" : "bg-[var(--color-accent)]"}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    {masteryPct > 0 && (
                      <span className="text-xs font-mono font-medium text-[var(--color-text-muted)]">{masteryPct}% <span className="text-[10px] text-[var(--color-text-muted)]">MR</span></span>
                    )}
                  </div>
                </div>

                <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 via-transparent to-yellow-500/5 opacity-0 group-hover:opacity-100 transition-opacity z-0 pointer-events-none" />
              </Link>
            );
          })}

          {!modulesLoading && readyNotebooks.map((notebook) => {
            const status = progress?.module_status[notebook.id];
            const completedInMod = status?.completed_count ?? 0;
            const masteryPct = status?.mastery_pct ?? 0;
            const pct = notebook.lesson_count ? (completedInMod / notebook.lesson_count) * 100 : 0;
            const isCompleted = pct === 100 && notebook.lesson_count > 0;

            return (
              <Link
                href={`/notebooks/${notebook.id}`}
                key={notebook.id}
                className="group relative overflow-hidden rounded-2xl transition-all duration-300 bg-[var(--color-surface)] border border-[var(--color-border)] hover:-translate-y-1 hover:shadow-xl cursor-pointer p-[1px] block"
              >
                <div className="bg-[var(--color-surface)] w-full h-full rounded-2xl p-6 relative z-10">
                  <div className="flex justify-between items-start mb-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm shadow-inner ${
                      isCompleted
                        ? "bg-[var(--color-success)]/20 text-[var(--color-success)] border border-[var(--color-success)]/30"
                        : "bg-[var(--color-accent)]/10 text-[var(--color-accent)] border border-[var(--color-accent)]/20"
                    }`}
                    >
                      {isCompleted ? <CheckCircle size={18} /> : "N"}
                    </div>

                    <div className="px-3 py-1 rounded-full bg-[var(--color-surface-2)] border border-[var(--color-border)] text-xs font-semibold text-[var(--color-text-secondary)] flex gap-1 items-center">
                      <span>{completedInMod}</span>
                      <span className="text-[var(--color-text-muted)]">/</span>
                      <span className="text-[var(--color-text-muted)]">{notebook.lesson_count}</span>
                    </div>
                  </div>

                  <div className="space-y-1 mb-5">
                    <h3 className="font-bold text-lg truncate text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)] transition-colors">
                      {notebook.title || "Untitled Notebook"}
                    </h3>
                    <p className="text-sm text-[var(--color-text-muted)] font-medium truncate">Saved Module</p>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-1.5 bg-[var(--color-surface-2)] rounded-full overflow-hidden border border-[var(--color-border)]">
                      <div
                        className={`h-full rounded-full transition-all duration-700 ${isCompleted ? "bg-[var(--color-success)]" : "bg-[var(--color-accent)]"}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    {masteryPct > 0 && (
                      <span className="text-xs font-mono font-medium text-[var(--color-text-muted)]">{masteryPct}% <span className="text-[10px] text-[var(--color-text-muted)]">MR</span></span>
                    )}
                  </div>
                </div>

                <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 via-transparent to-yellow-500/5 opacity-0 group-hover:opacity-100 transition-opacity z-0 pointer-events-none" />
              </Link>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 animate-slide-up" style={{ animationDelay: "0.5s" }}>
        <Link
          href="/quiz"
          className="bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl flex items-center gap-4 group hover:bg-[var(--color-surface-2)]"
        >
          <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/20 flex items-center justify-center shrink-0">
            <RefreshCw size={20} className="text-[var(--color-accent)]" />
          </div>
          <div>
            <p className="font-bold text-[var(--color-text-primary)] text-sm group-hover:text-[var(--color-accent)] transition-colors">Daily Quiz</p>
            <p className="text-xs text-[var(--color-text-muted)]">Review specific weak spots</p>
          </div>
        </Link>

        <Link
          href="/glossary"
          className="bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl flex items-center gap-4 group hover:bg-[var(--color-surface-2)]"
        >
          <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/20 flex items-center justify-center shrink-0">
            <Zap size={20} className="text-[var(--color-accent)]" />
          </div>
          <div>
            <p className="font-bold text-[var(--color-text-primary)] text-sm group-hover:text-[var(--color-accent)] transition-colors">Term Glossary</p>
            <p className="text-xs text-[var(--color-text-muted)]">Search technical vocabulary</p>
          </div>
        </Link>

        <Link
          href="/week-review"
          className="bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl flex items-center justify-between group hover:bg-[var(--color-surface-2)]"
        >
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/20 flex items-center justify-center shrink-0">
              <BookOpen size={20} className="text-[var(--color-accent)]" />
            </div>
            <div>
              <p className="font-bold text-[var(--color-text-primary)] text-sm group-hover:text-[var(--color-accent)] transition-colors">Week in Review</p>
              <p className="text-xs text-[var(--color-text-muted)]">Review weekly progress</p>
            </div>
          </div>
          <div className="w-8 h-8 rounded-full bg-[var(--color-surface-2)] border border-[var(--color-border)] flex items-center justify-center group-hover:bg-[var(--color-accent)] transition-colors">
            <ArrowRight size={14} className="text-[var(--color-text-muted)] group-hover:text-white" />
          </div>
        </Link>
      </div>
    </div>
  );
}
