"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchModules, fetchProgress, fetchReviewQueue, fetchMastery, streamWhatNext,
  type Module, type ProgressData, type ReviewQueue, type MasteryData,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Flame, BookOpen, Star, Zap, ChevronRight, Lock, ArrowRight, RefreshCw, AlertCircle } from "lucide-react";

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
        <div className="text-center space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#a01c2c] to-[#b8822a] mx-auto flex items-center justify-center">
            <span className="text-white font-bold text-xl">O</span>
          </div>
          <p className="text-[#5c4f45] text-sm">Loading Orion Code...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-5">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#a01c2c] to-[#b8822a] flex items-center justify-center shadow-lg shadow-red-500/25">
          <span className="text-white font-bold text-lg">O</span>
        </div>
        <div className="flex-1">
          <h1 className="text-xl font-bold bg-gradient-to-r from-[#a01c2c] to-[#b8822a] bg-clip-text text-transparent">
            Orion Code
          </h1>
          <p className="text-[#5c4f45] text-xs">Your WashU FinTech Analytics prep companion</p>
        </div>
        {/* Countdown */}
        <div className="text-right">
          <p className="text-lg font-bold text-[#1c1410]">{daysUntilStart}</p>
          <p className="text-[10px] text-[#9a8c80] leading-tight">days to<br/>program</p>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { icon: <Flame size={16} />, value: progress?.streak ?? 0, label: "Day Streak", color: "text-yellow-500" },
          { icon: <BookOpen size={16} />, value: completedLessons, label: "Lessons Done", color: "text-green-400" },
          { icon: <Star size={16} />, value: totalStars, label: "Stars Earned", color: "text-yellow-400" },
        ].map(({ icon, value, label, color }) => (
          <div key={label} className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-3 text-center">
            <div className={`flex items-center justify-center gap-1 ${color} mb-1`}>
              {icon}
              <span className="text-lg font-bold text-[#1c1410]">{value}</span>
            </div>
            <p className="text-[#9a8c80] text-xs">{label}</p>
          </div>
        ))}
      </div>

      {/* Overall progress */}
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-[#5c4f45]">Overall Progress</span>
          <span className="text-[#a01c2c] font-medium">{completedLessons} / {totalLessons} lessons · {overallPct}%</span>
        </div>
        <div className="h-2 bg-[#f5f0ea] rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-[#a01c2c] to-[#b8822a] rounded-full transition-all duration-500"
            style={{ width: `${overallPct}%` }}
          />
        </div>
      </div>

      {/* What's Next */}
      <div className="bg-[#f8eaec] border border-[#a01c2c]/30 rounded-xl p-4 space-y-2">
        <p className="text-xs font-semibold text-[#a01c2c] uppercase tracking-wider">What's Next</p>
        {whatNextLoading && !whatNext ? (
          <div className="space-y-1.5">
            <div className="h-3 bg-[#ffffff] rounded animate-pulse w-4/5" />
            <div className="h-3 bg-[#ffffff] rounded animate-pulse w-3/5" />
          </div>
        ) : whatNext ? (
          <p className="text-sm text-[#5c4f45] leading-relaxed">{whatNext}</p>
        ) : (
          <p className="text-sm text-[#9a8c80]">Pick up where you left off.</p>
        )}
      </div>

      {/* Due for Review */}
      {reviewQueue && reviewQueue.total_due > 0 && (
        <Link
          href="/review-queue"
          className="flex items-center justify-between bg-red-500/10 border border-red-500/30 rounded-xl p-4 hover:border-red-500/50 transition-all"
        >
          <div className="flex items-center gap-3">
            <RefreshCw size={18} className="text-red-400" />
            <div>
              <p className="text-sm font-semibold text-[#1c1410]">{reviewQueue.total_due} Review{reviewQueue.total_due !== 1 ? "s" : ""} Due</p>
              <p className="text-xs text-[#5c4f45]">Questions you got wrong — spaced repetition</p>
            </div>
          </div>
          <span className="text-xs text-red-400 font-medium">Start →</span>
        </Link>
      )}

      {/* Focus Areas */}
      {mastery && mastery.focus_areas.length > 0 && (
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle size={14} className="text-yellow-500" />
              <span className="text-xs font-semibold text-[#5c4f45] uppercase tracking-wider">Focus Areas</span>
            </div>
            <Link href="/progress" className="text-xs text-[#a01c2c] hover:underline">View all →</Link>
          </div>
          <div className="space-y-2">
            {mastery.focus_areas.slice(0, 3).map(({ tag, mastery: score }) => (
              <div key={tag} className="flex items-center gap-3">
                <span className="text-xs text-[#1c1410] flex-1 truncate">{tag.replace(/_/g, " ")}</span>
                <div className="w-24 h-1.5 bg-[#f5f0ea] rounded-full overflow-hidden">
                  <div className="h-full bg-red-500 rounded-full" style={{ width: `${score}%` }} />
                </div>
                <span className="text-xs text-red-400 w-8 text-right">{score}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Module skill map */}
      <div>
        <h2 className="text-xs font-semibold text-[#5c4f45] uppercase tracking-wider mb-3">Learning Path</h2>
        <div className="space-y-2">
          {modules.map((module, idx) => {
            const status = progress?.module_status[module.id];
            const unlocked = status?.unlocked ?? idx === 0;
            const completedInMod = status?.completed_count ?? 0;
            const masteryPct = status?.mastery_pct ?? 0;
            const pct = module.lesson_count ? (completedInMod / module.lesson_count) * 100 : 0;

            return (
              <div key={module.id} className="relative">
                {idx < modules.length - 1 && (
                  <div className="absolute left-5 top-full w-px h-2 bg-[#e5ddd4] z-10" />
                )}
                <Link
                  href={unlocked ? `/curriculum/${module.id}` : "#"}
                  className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                    unlocked
                      ? "bg-[#ffffff] border-[#e5ddd4] hover:border-[#a01c2c] hover:bg-[#f5f0ea] cursor-pointer"
                      : "bg-[#ffffff]/40 border-[#e5ddd4]/40 cursor-not-allowed opacity-50"
                  }`}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 font-bold text-sm ${
                    pct === 100 ? "bg-green-500/20 text-green-400" :
                    unlocked ? "bg-[#a01c2c]/20 text-[#a01c2c]" :
                    "bg-[#e5ddd4]/50 text-[#9a8c80]"
                  }`}>
                    {unlocked ? (pct === 100 ? "✓" : module.order) : <Lock size={14} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2 mb-0.5">
                      <p className="font-medium text-sm text-[#1c1410] truncate">{module.title}</p>
                      {unlocked && (
                        <span className="text-xs text-[#a01c2c] font-medium shrink-0">
                          {completedInMod}/{module.lesson_count}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-[#9a8c80] truncate">{module.course}</p>
                    {unlocked && (
                      <div className="flex items-center gap-2 mt-2">
                        <div className="flex-1 h-1 bg-[#f5f0ea] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-[#a01c2c] to-[#b8822a] rounded-full transition-all"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        {masteryPct > 0 && (
                          <span className="text-[10px] text-yellow-400 shrink-0">{masteryPct}% mastery</span>
                        )}
                      </div>
                    )}
                  </div>
                  {unlocked && <ChevronRight size={16} className="text-[#9a8c80] shrink-0" />}
                </Link>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-2 gap-3">
        <Link
          href="/quiz"
          className="flex items-center gap-3 bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 hover:border-yellow-500/50 hover:bg-yellow-500/5 transition-all"
        >
          <Flame size={20} className="text-yellow-500" />
          <div>
            <p className="text-sm font-medium text-[#1c1410]">Daily Quiz</p>
            <p className="text-xs text-[#9a8c80]">Review weak spots</p>
          </div>
        </Link>
        <Link
          href="/glossary"
          className="flex items-center gap-3 bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 hover:border-[#b8822a]/50 hover:bg-[#b8822a]/5 transition-all"
        >
          <Zap size={20} className="text-[#b8822a]" />
          <div>
            <p className="text-sm font-medium text-[#1c1410]">Glossary</p>
            <p className="text-xs text-[#9a8c80]">Look up terms</p>
          </div>
        </Link>
      </div>

      {/* Week in Review link */}
      <Link
        href="/week-review"
        className="flex items-center justify-between bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 hover:border-[#a01c2c]/40 transition-all"
      >
        <div>
          <p className="text-sm font-medium text-[#1c1410]">Week in Review</p>
          <p className="text-xs text-[#9a8c80]">See what you learned this week</p>
        </div>
        <ArrowRight size={16} className="text-[#9a8c80]" />
      </Link>
    </div>
  );
}
