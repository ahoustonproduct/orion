"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchModule, fetchProgress, type Module, type ProgressData, type LessonSummary } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Clock, ChevronRight, ArrowLeft, Flag, Download, Zap, LayoutGrid, List } from "lucide-react";
import StarRating from "@/components/StarRating";
import ConceptMap from "@/components/ConceptMap";
import QuickLookCard from "@/components/QuickLookCard";

type ViewMode = "list" | "map";

// Extend LessonSummary with fields from curriculum data
interface LessonSummaryExtended extends LessonSummary {
  difficulty?: "beginner" | "intermediate" | "advanced";
  is_capstone?: boolean;
}

interface ModuleExtended extends Module {
  concept_map?: { id: string; label: string; connects_to?: string[] }[];
  lessons?: LessonSummaryExtended[];
  supplementary_courses?: {
    title: string;
    provider: string;
    url: string;
    duration: string;
    level: string;
    free_audit: boolean;
    description: string;
    syllabus?: { module: string; topics: string }[];
    tools?: string;
    prerequisites?: string;
  }[];
}

export default function ModulePage() {
  const { moduleId } = useParams<{ moduleId: string }>();
  const [module, setModule] = useState<ModuleExtended | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [quickLookLesson, setQuickLookLesson] = useState<string | null>(null);

  useEffect(() => {
    const userKey = getUserKey();
    Promise.all([fetchModule(moduleId), fetchProgress(userKey)])
      .then(([mod, prog]) => {
        setModule(mod as ModuleExtended);
        setProgress(prog);
      })
      .catch(console.error);
  }, [moduleId]);

  if (!module) {
    return <div className="flex items-center justify-center min-h-screen text-[#94a3b8]">Loading...</div>;
  }

  const lessonProgressMap = Object.fromEntries(
    (progress?.lessons ?? []).map((l) => [l.lesson_id, l])
  );

  const moduleStatus = progress?.module_status[module.id];
  const completedCount = moduleStatus?.completed_count ?? 0;
  const totalCount = module.lesson_count ?? 0;
  const masteryPct = moduleStatus?.mastery_pct ?? 0;
  const pct = totalCount ? Math.round((completedCount / totalCount) * 100) : 0;

  // Get full lesson data for Quick Look (keyed by lesson ID)
  const lessonDataMap: Record<string, LessonSummaryExtended> = Object.fromEntries(
    (module.lessons ?? []).map((l) => [l.id, l])
  );

  const quickLookData = quickLookLesson ? lessonDataMap[quickLookLesson] : null;

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      {/* Back */}
      <Link
        href="/curriculum"
        className="flex items-center gap-2 text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] text-sm transition-colors"
      >
        <ArrowLeft size={14} /> Back to Curriculum
      </Link>

      {/* Module header */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="inline-block text-xs text-[var(--color-accent)] bg-[var(--color-accent)]/10 rounded-full px-2 py-0.5 mb-2">
              {module.course}
            </div>
            <h1 className="text-xl font-bold text-[var(--color-text-primary)] mb-1">{module.title}</h1>
            <p className="text-sm text-[var(--color-text-secondary)]">{module.description}</p>
          </div>
          <a
            href={`/api/curriculum/modules/${moduleId}/export`}
            download
            title="Download study packet for NotebookLM"
            className="shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-accent)]/10 text-[var(--color-text-muted)] hover:text-[var(--color-accent)] text-xs font-medium transition-all"
          >
            <Download size={13} />
            <span className="hidden sm:inline">Study Packet</span>
          </a>
        </div>

        {/* Module progress */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs text-[var(--color-text-muted)]">
            <span>{completedCount}/{totalCount} lessons complete</span>
            <span className="text-[var(--color-star)]">{masteryPct}% mastery</span>
          </div>
          <div className="h-1.5 bg-[var(--color-surface-2)] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-light)] rounded-full transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
      </div>

      {/* View toggle */}
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider">Lessons</p>
        <div className="flex items-center bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg overflow-hidden">
          <button
            onClick={() => setViewMode("list")}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs transition-all ${
              viewMode === "list" ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]" : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
            }`}
          >
            <List size={12} /> List
          </button>
          <button
            onClick={() => setViewMode("map")}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs transition-all ${
              viewMode === "map" ? "bg-[var(--color-accent)]/20 text-[var(--color-accent)]" : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
            }`}
          >
            <LayoutGrid size={12} /> Map
          </button>
        </div>
      </div>

      {/* Concept map view */}
      {viewMode === "map" && module.concept_map && (
        <ConceptMap
          nodes={module.concept_map}
          lessonProgress={lessonProgressMap}
          moduleUnlocked={true}
        />
      )}

      {/* List view */}
      {viewMode === "list" && (
        <div className="space-y-2">
          {(module.lessons ?? []).map((lesson) => {
            const lp = lessonProgressMap[lesson.id];
            const stars = lp?.stars ?? 0;
            const completed = lp?.completed ?? false;
            const flagged = lp?.flagged ?? false;
            const isCapstone = (lesson as LessonSummaryExtended).is_capstone;
            const difficulty = (lesson as LessonSummaryExtended).difficulty;

            return (
              <div key={lesson.id} className="relative group">
                <Link
                  href={`/learn/${lesson.id}`}
                  className={`flex items-center gap-3 p-4 border rounded-xl transition-all ${
                    isCapstone
                      ? "bg-[var(--color-surface)] border-[var(--color-star)]/20 hover:border-[var(--color-star)]/50 hover:bg-[var(--color-star)]/5"
                      : "bg-[var(--color-surface)] border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-surface-2)]"
                  }`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 ${
                    completed ? "bg-[var(--color-success)]/20 text-[var(--color-success)]" :
                    isCapstone ? "bg-[var(--color-star)]/20 text-[var(--color-star)]" :
                    "bg-[var(--color-surface-2)] text-[var(--color-text-muted)]"
                  }`}>
                    {completed ? "✓" : isCapstone ? "★" : lesson.order}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <p className="text-sm font-medium text-[var(--color-text-primary)] truncate">{lesson.title}</p>
                      {isCapstone && (
                        <span className="text-[10px] bg-[var(--color-star)]/10 border border-[var(--color-star)]/30 text-[var(--color-star)] px-1.5 py-0.5 rounded-full shrink-0">
                          Capstone
                        </span>
                      )}
                      {difficulty && difficulty !== "beginner" && !isCapstone && (
                        <span className={`text-[10px] px-1.5 py-0.5 rounded-full border shrink-0 ${
                          difficulty === "advanced"
                            ? "bg-purple-500/10 border-purple-500/30 text-purple-400"
                            : "bg-blue-500/10 border-blue-500/30 text-blue-400"
                        }`}>
                          {difficulty}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-3 mt-0.5">
                      <span className="text-xs text-[var(--color-text-muted)] flex items-center gap-1">
                        <Clock size={10} /> {lesson.duration_min} min
                      </span>
                      {completed && <StarRating stars={stars} size="sm" />}
                      {flagged && <Flag size={11} className="text-[var(--color-star)]" />}
                    </div>
                  </div>
                  <ChevronRight size={16} className="text-[var(--color-text-muted)] shrink-0" />
                </Link>

                {/* Quick Look button (only for completed lessons) */}
                {completed && (
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      setQuickLookLesson(lesson.id);
                    }}
                    className="absolute right-12 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 flex items-center gap-1 px-2 py-1 bg-[var(--color-background)] border border-[var(--color-border)] rounded-lg text-[var(--color-accent)] text-xs transition-all hover:border-[var(--color-accent)]/50"
                    title="Quick Look"
                  >
                    <Zap size={10} />
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Supplementary Courses */}
      {module.supplementary_courses && module.supplementary_courses.length > 0 && (
        <div className="space-y-4">
          <p className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider">Recommended Coursera Courses</p>
          {module.supplementary_courses.map((course) => (
            <div
              key={course.url}
              className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl overflow-hidden"
            >
              <a
                href={course.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-4 hover:bg-[var(--color-surface-2)] transition-all"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">{course.title}</p>
                    <p className="text-xs text-[var(--color-text-muted)] mb-2">{course.provider} · {course.duration} · {course.level}</p>
                    <p className="text-xs text-[var(--color-text-secondary)] leading-relaxed">{course.description}</p>
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      {course.free_audit && (
                        <span className="text-[10px] bg-[var(--color-success)]/10 border border-[var(--color-success)]/30 text-[var(--color-success)] px-2 py-0.5 rounded-full">
                          Free to audit
                        </span>
                      )}
                      <span className="text-[10px] bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/30 text-[var(--color-accent)] px-2 py-0.5 rounded-full">
                        Coursera
                      </span>
                      {course.prerequisites && (
                        <span className="text-[10px] bg-[var(--color-star)]/10 border border-[var(--color-star)]/30 text-[var(--color-star)] px-2 py-0.5 rounded-full">
                          {course.prerequisites}
                        </span>
                      )}
                    </div>
                  </div>
                  <ChevronRight size={16} className="text-[var(--color-text-muted)] shrink-0 mt-1" />
                </div>
              </a>
              {/* Syllabus */}
              {course.syllabus && course.syllabus.length > 0 && (
                <div className="border-t border-[var(--color-border)] bg-[var(--color-background)] p-4">
                  <p className="text-[10px] font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-3">Syllabus</p>
                  <div className="space-y-2">
                    {course.syllabus.map((s: { module: string; topics: string }, i: number) => (
                      <div key={i} className="flex gap-3">
                        <span className="text-[10px] font-bold text-[var(--color-accent)] shrink-0 w-6 pt-0.5">{i + 1}</span>
                        <div>
                          <p className="text-xs font-medium text-[var(--color-text-primary)]">{s.module}</p>
                          <p className="text-[11px] text-[var(--color-text-muted)]">{s.topics}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  {course.tools && (
                    <p className="text-[10px] text-[var(--color-text-muted)] mt-3">
                      <span className="font-medium text-[var(--color-text-secondary)]">Tools:</span> {course.tools}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Quick Look modal */}
      {quickLookLesson && quickLookData && (
        <QuickLookCard
          lessonId={quickLookLesson}
          lessonTitle={quickLookData.title}
          keySyntax={[]}
          notes=""
          progress={lessonProgressMap[quickLookLesson]}
          onClose={() => setQuickLookLesson(null)}
        />
      )}
    </div>
  );
}
