"use client";

import { useEffect, useState } from "react";
import { fetchProgress, type ProgressData } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { BarChart2, Target, Clock, AlertCircle, Star } from "lucide-react";

export default function ProgressPage() {
  const userKey = getUserKey();
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgress(userKey)
      .then((p) => { setProgress(p); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [userKey]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-sm text-[var(--color-text-muted)]">Loading progress data...</p>
      </div>
    );
  }

  const completedLessons = progress?.lessons.filter((l) => l.completed).length ?? 0;
  const totalMinutes = Object.values(progress?.study_log ?? {}).reduce((a, b) => a + b, 0);
  const avgStars = progress && progress.lessons.length > 0
    ? (progress.lessons.reduce((s, l) => s + l.stars, 0) / progress.lessons.length).toFixed(1)
    : "0.0";

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">
      <div className="flex items-center gap-2">
        <BarChart2 size={18} className="text-[var(--color-accent)]" />
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Progress & Diagnostics</h1>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Lessons Done", value: completedLessons, icon: <Target size={15} />, color: "text-[var(--color-success)]" },
          { label: "Study Minutes", value: Math.round(totalMinutes), icon: <Clock size={15} />, color: "text-[var(--color-accent)]" },
          { label: "Avg Stars", value: avgStars, icon: <Star size={15} />, color: "text-[var(--color-star)]" },
        ].map(({ label, value, icon, color }) => (
          <div key={label} className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-3 text-center">
            <div className={`flex items-center justify-center gap-1 ${color} mb-1`}>
              {icon}
              <span className="text-lg font-bold text-[var(--color-text-primary)]">{value}</span>
            </div>
            <p className="text-xs text-[var(--color-text-muted)]">{label}</p>
          </div>
        ))}
      </div>

      {/* Weak Topics */}
      {progress && progress.weak_topics.length > 0 && (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <AlertCircle size={14} className="text-[var(--color-error)]" />
            <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Weak Topics</h2>
            <span className="text-xs text-[var(--color-text-muted)]">— lessons with &lt; 3 stars</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {progress.weak_topics.map((topic) => (
              <span key={topic} className="text-xs bg-[var(--color-error)]/10 text-[var(--color-error)] border border-[var(--color-error)]/30 px-2 py-1 rounded-full">
                {topic.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Module Progress */}
      {progress && Object.keys(progress.module_status).length > 0 && (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Module Progress</h2>
          <div className="space-y-3">
            {Object.entries(progress.module_status).map(([modId, status]) => {
              const pct = status.total > 0 ? Math.round((status.completed_count / status.total) * 100) : 0;
              return (
                <div key={modId} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-[var(--color-text-primary)] font-medium">{modId.toUpperCase()}</span>
                    <span className="text-[var(--color-text-muted)]">{status.completed_count}/{status.total} · {pct}%</span>
                  </div>
                  <div className="h-1.5 bg-[var(--color-surface-2)] rounded-full overflow-hidden border border-[var(--color-border)]">
                    <div
                      className="h-full bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-hover)] rounded-full"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Mastered Concepts */}
      {progress && progress.mastered_concepts.length > 0 && (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <Star size={14} className="text-[var(--color-star)]" />
            <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Mastered Concepts</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {progress.mastered_concepts.map((topic) => (
              <span key={topic} className="text-xs bg-[var(--color-success)]/10 text-[var(--color-success)] border border-[var(--color-success)]/30 px-2 py-1 rounded-full">
                {topic.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Streak */}
      {progress && progress.streak > 0 && (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-star)] to-[var(--color-error)] flex items-center justify-center">
            <span className="text-xl font-bold text-white">{progress.streak}</span>
          </div>
          <div>
            <p className="text-sm font-semibold text-[var(--color-text-primary)]">Study Streak</p>
            <p className="text-xs text-[var(--color-text-muted)]">{progress.streak === 1 ? "1 day" : `${progress.streak} days in a row`}</p>
          </div>
        </div>
      )}
    </div>
  );
}
