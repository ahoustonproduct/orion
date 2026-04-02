"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchModules, fetchProgress, fetchReviewQueue, fetchMastery, streamWhatNext,
  type Module, type ProgressData, type ReviewQueue, type MasteryData,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Flame, BookOpen, Star, Zap, ChevronRight, Lock, ArrowRight, RefreshCw, AlertCircle, Activity, Box, Cpu } from "lucide-react";

export default function Dashboard() {
  const [modules, setModules] = useState<Module[]>([]);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [reviewQueue, setReviewQueue] = useState<ReviewQueue | null>(null);
  const [mastery, setMastery] = useState<MasteryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [whatNext, setWhatNext] = useState("");
  const [whatNextLoading, setWhatNextLoading] = useState(false);

  useEffect(() => {
    const userKey = getUserKey();
    Promise.all([
      fetchModules(),
      fetchProgress(userKey),
      fetchReviewQueue(userKey).catch(() => null),
      fetchMastery(userKey).catch(() => null),
    ])
      .then(([mods, prog, rq, mast]) => {
        setModules(mods);
        setProgress(prog);
        setReviewQueue(rq);
        setMastery(mast);

        setWhatNextLoading(true);
        streamWhatNext(userKey, prog, (chunk) => setWhatNext((p) => p + chunk))
          .then(() => setWhatNextLoading(false))
          .catch(() => setWhatNextLoading(false));
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const totalLessons = modules.reduce((s, m) => s + m.lesson_count, 0);
  const completedLessons = progress ? progress.lessons.filter((l) => l.completed).length : 0;
  const totalStars = progress ? progress.lessons.reduce((s, l) => s + l.stars, 0) : 0;
  const overallPct = totalLessons ? Math.round((completedLessons / totalLessons) * 100) : 0;

  // Days until WashU Fall 2026 start
  const daysUntilStart = Math.max(0, Math.round(
    (new Date("2026-08-24").getTime() - Date.now()) / (1000 * 60 * 60 * 24)
  ));

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="relative w-24 h-24 flex items-center justify-center">
          <div className="absolute inset-0 border-t-2 border-r-2 border-[var(--color-accent)] rounded-full animate-spin"></div>
          <div className="absolute inset-2 border-b-2 border-l-2 border-[var(--color-accent-light)] rounded-full animate-[spin_1.5s_reverse_infinite]"></div>
          <div className="w-12 h-12 rounded-full bg-[var(--color-surface-2)] flex items-center justify-center animate-pulse">
            <span className="text-[var(--color-accent)] font-bold text-xl">O</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10 space-y-8 pb-20">
      {/* Header Profile Section */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 animate-slide-up" style={{ animationDelay: "0.1s" }}>
        <div className="flex items-center gap-5">
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
        
        {/* Countdown Badge */}
        <div className="glass-card px-5 py-3 rounded-2xl flex items-center gap-4">
           <div className="flex flex-col">
              <span className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-rose-400 to-yellow-400">
                {daysUntilStart}
              </span>
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-0.5">Days to Start</span>
           </div>
           <div className="w-10 h-10 rounded-full bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-500">
              <Activity size={18} />
           </div>
        </div>
      </div>

      {/* Main Grid: Stats & What's Next */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 animate-slide-up" style={{ animationDelay: "0.2s" }}>
        
        {/* Left Column: Stats Cards */}
        <div className="md:col-span-5 grid grid-cols-2 gap-4">
          {[
            { icon: <Flame size={20} />, value: progress?.streak ?? 0, label: "Day Streak", gradient: "from-orange-500/20 to-rose-500/5", color: "text-orange-400", border: "border-orange-500/20" },
            { icon: <BookOpen size={20} />, value: completedLessons, label: "Lessons Done", gradient: "from-emerald-500/20 to-teal-500/5", color: "text-emerald-400", border: "border-emerald-500/20" },
            { icon: <Star size={20} />, value: totalStars, label: "Total Stars", gradient: "from-yellow-500/20 to-amber-500/5", color: "text-yellow-400", border: "border-yellow-500/20", colSpan: "col-span-2" },
          ].map(({ icon, value, label, gradient, color, border, colSpan }) => (
            <div key={label} className={`bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl relative overflow-hidden ${colSpan || ""}`}>
              <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${gradient} rounded-full blur-2xl -translate-y-10 translate-x-10`} />
              <div className="relative z-10 flex flex-col gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center border ${border} bg-[var(--color-surface-2)]/50 ${color}`}>
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

        {/* Right Column: AI Assistant Context */}
        <div className="md:col-span-7 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 relative overflow-hidden flex flex-col">
          <div className="absolute -inset-2 bg-gradient-to-br from-[var(--color-accent)]/10 via-transparent to-[var(--color-accent-light)]/5 z-0 pointer-events-none blur-xl" />
          
          <div className="relative z-10 flex items-center gap-3 mb-6">
            <div className="w-8 h-8 rounded-full bg-[var(--color-accent)]/20 border border-[var(--color-accent)]/30 flex items-center justify-center">
              <Cpu size={14} className="text-[var(--color-accent)]" />
            </div>
            <h2 className="text-sm font-bold text-[var(--color-text-secondary)] uppercase tracking-widest">Orion Intelligence</h2>
          </div>
          
          <div className="flex-1 flex flex-col justify-center">
            {whatNextLoading && !whatNext ? (
              <div className="space-y-3">
                <div className="h-4 bg-[var(--color-surface-2)] rounded animate-pulse w-full" />
                <div className="h-4 bg-[var(--color-surface-2)] rounded animate-pulse w-5/6" />
                <div className="h-4 bg-[var(--color-surface-2)] rounded animate-pulse w-4/6" />
              </div>
            ) : whatNext ? (
              <div className="text-[var(--color-text-secondary)] leading-relaxed text-lg font-medium">
                <p className="border-l-2 border-[var(--color-accent)]/50 pl-4 py-1">{whatNext}</p>
              </div>
            ) : (
              <p className="text-[var(--color-text-muted)] italic">Analyzing your recent performance to determine the optimal next steps...</p>
            )}
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

      {/* Dynamic Alerts row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-slide-up" style={{ animationDelay: "0.3s" }}>
        {/* Due for Review Alert */}
        {reviewQueue && reviewQueue.total_due > 0 && (
          <Link
            href="/review-queue"
            className="group glass-card !border-rose-500/30 p-5 rounded-2xl flex items-center justify-between overflow-hidden relative"
          >
            <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-rose-500/10 to-transparent pointer-events-none group-hover:from-rose-500/20 transition-all" />
            <div className="flex items-center gap-4 relative z-10">
              <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center">
                <RefreshCw size={20} className="text-rose-400" />
              </div>
              <div>
                <p className="font-bold text-white mb-0.5">{reviewQueue.total_due} Review{reviewQueue.total_due !== 1 ? "s" : ""} Due</p>
                <p className="text-xs text-rose-300/80 font-medium">Spaced repetition queue requires attention</p>
              </div>
            </div>
            <div className="w-8 h-8 rounded-full bg-rose-500/10 flex items-center justify-center group-hover:bg-rose-500 transition-colors relative z-10">
              <ArrowRight size={14} className="text-rose-500 group-hover:text-white" />
            </div>
          </Link>
        )}

        {/* Focus Areas Mini widget */}
        {mastery && mastery.focus_areas.length > 0 && (
          <div className="glass-card p-5 rounded-2xl flex flex-col justify-center">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <AlertCircle size={14} className="text-yellow-500" />
                <span className="text-xs font-bold text-slate-300 uppercase tracking-widest">Focus Areas</span>
              </div>
              <Link href="/progress" className="text-xs font-semibold text-rose-400 hover:text-rose-300 uppercase tracking-wider">Metrics →</Link>
            </div>
            <div className="space-y-3">
              {mastery.focus_areas.slice(0, 2).map(({ tag, mastery: score }) => (
                <div key={tag} className="flex items-center gap-4">
                  <span className="text-sm font-medium text-slate-300 w-1/3 truncate capitalize">{tag.replace(/_/g, " ")}</span>
                  <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
                    <div className="h-full bg-rose-500 rounded-full" style={{ width: `${score}%` }} />
                  </div>
                  <span className="text-xs font-mono text-rose-400 w-10 text-right">{score}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modules List */}
      <div className="animate-slide-up" style={{ animationDelay: "0.4s" }}>
        <div className="flex items-center gap-3 mb-6">
          <Box size={20} className="text-[var(--color-text-muted)]" />
          <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Learning Curriculum</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {modules.map((module, idx) => {
            const status = progress?.module_status[module.id];
            const unlocked = status?.unlocked ?? idx === 0;
            const completedInMod = status?.completed_count ?? 0;
            const masteryPct = status?.mastery_pct ?? 0;
            const pct = module.lesson_count ? (completedInMod / module.lesson_count) * 100 : 0;
            const isCompleted = pct === 100;

            return (
              <Link
                href={unlocked ? `/curriculum/${module.id}` : "#"}
                key={module.id}
                className={`group relative overflow-hidden rounded-2xl transition-all duration-300 ${
                  unlocked
                    ? "bg-[var(--color-surface)] border border-[var(--color-border)] hover:-translate-y-1 hover:shadow-xl cursor-pointer p-[1px] block"
                    : "opacity-60 bg-[var(--color-surface-2)]/40 border border-[var(--color-border)] cursor-not-allowed block p-[1px]"
                }`}
              >
                 <div className="bg-[var(--color-surface)] w-full h-full rounded-2xl p-6 relative z-10">
                   {/* Top header row */}
                   <div className="flex justify-between items-start mb-4">
                     <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm shadow-inner
                       ${isCompleted ? "bg-[var(--color-success)]/20 text-[var(--color-success)] border border-[var(--color-success)]/30" :
                       unlocked ? "bg-[var(--color-accent)]/10 text-[var(--color-accent)] border border-[var(--color-accent)]/20" :
                       "bg-[var(--color-surface-2)] text-[var(--color-text-muted)] border border-[var(--color-border)]"
                     }`}
                     >
                       {unlocked ? (isCompleted ? "✓" : module.order) : <Lock size={14} />}
                     </div>
                     
                     {unlocked && (
                       <div className="px-3 py-1 rounded-full bg-[var(--color-surface-2)] border border-[var(--color-border)] text-xs font-semibold text-[var(--color-text-secondary)] flex gap-1 items-center">
                         <span>{completedInMod}</span>
                         <span className="text-[var(--color-text-muted)]">/</span>
                         <span className="text-[var(--color-text-muted)]">{module.lesson_count}</span>
                       </div>
                     )}
                   </div>
                   
                   {/* Content body */}
                   <div className="space-y-1 mb-5">
                      <h3 className={`font-bold text-lg truncate ${unlocked ? "text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)] transition-colors" : "text-[var(--color-text-muted)]"}`}>
                        {module.title}
                      </h3>
                      <p className="text-sm text-[var(--color-text-muted)] font-medium truncate">{module.course}</p>
                   </div>
                   
                   {/* Progress footer */}
                   {unlocked ? (
                     <div className="flex items-center gap-3">
                       <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700/50">
                         <div
                           className={`h-full rounded-full transition-all duration-700 ${isCompleted ? 'bg-emerald-500' : 'bg-gradient-to-r from-rose-500 to-yellow-500'}`}
                           style={{ width: `${pct}%` }}
                         />
                       </div>
                       {masteryPct > 0 && (
                         <span className="text-xs font-mono font-medium text-yellow-500/80">{masteryPct}% <span className="text-[10px] text-slate-600">MR</span></span>
                       )}
                     </div>
                   ) : (
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden border border-slate-700/50 relative">
                         <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0wIDQwbDQwLTQwSDB6IiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDUpIi8+Cjwvc3ZnPg==')] opacity-20"></div>
                      </div>
                   )}
                 </div>
                 
                 {/* Hover effect gradient */}
                 {unlocked && (
                   <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 via-transparent to-yellow-500/5 opacity-0 group-hover:opacity-100 transition-opacity z-0 pointer-events-none" />
                 )}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Action Footer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 animate-slide-up" style={{ animationDelay: "0.5s" }}>
        <Link
          href="/quiz"
          className="bg-[var(--color-surface)] border border-[var(--color-border)] p-5 rounded-2xl flex items-center gap-4 group hover:bg-[var(--color-surface-2)]"
        >
          <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/20 flex items-center justify-center shrink-0">
            <Flame size={20} className="text-[var(--color-accent)]" />
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
          <div>
            <p className="font-bold text-[var(--color-text-primary)] text-sm group-hover:text-[var(--color-accent)] transition-colors">Week in Review</p>
            <p className="text-xs text-[var(--color-text-muted)]">Read AI summary of progress</p>
          </div>
          <div className="w-8 h-8 rounded-full border border-[var(--color-border)] bg-[var(--color-surface-2)] flex items-center justify-center group-hover:bg-[var(--color-accent)] transition-colors group-hover:border-[var(--color-accent)]">
             <ArrowRight size={14} className="text-[var(--color-text-muted)] group-hover:text-white" />
          </div>
        </Link>
      </div>
      
    </div>
  );
}
