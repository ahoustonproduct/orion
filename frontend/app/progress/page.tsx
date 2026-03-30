"use client";

import { useEffect, useState } from "react";
import { fetchMastery, fetchProgress, type MasteryData, type ProgressData } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import MasteryHeatmap from "@/components/MasteryHeatmap";
import { BarChart2, Target, Clock, AlertCircle } from "lucide-react";

export default function ProgressPage() {
  const userKey = getUserKey();
  const [mastery, setMastery] = useState<MasteryData | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchMastery(userKey), fetchProgress(userKey)])
      .then(([m, p]) => { setMastery(m); setProgress(p); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [userKey]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-sm text-[#9a8c80]">Loading progress data...</p>
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
        <BarChart2 size={18} className="text-[#a01c2c]" />
        <h1 className="text-xl font-bold text-[#1c1410]">Progress & Diagnostics</h1>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Lessons Done", value: completedLessons, icon: <Target size={15} />, color: "text-green-400" },
          { label: "Study Minutes", value: Math.round(totalMinutes), icon: <Clock size={15} />, color: "text-[#a01c2c]" },
          { label: "Avg Stars", value: avgStars, icon: <BarChart2 size={15} />, color: "text-yellow-400" },
        ].map(({ label, value, icon, color }) => (
          <div key={label} className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-3 text-center">
            <div className={`flex items-center justify-center gap-1 ${color} mb-1`}>
              {icon}
              <span className="text-lg font-bold text-[#1c1410]">{value}</span>
            </div>
            <p className="text-xs text-[#9a8c80]">{label}</p>
          </div>
        ))}
      </div>

      {/* Focus Areas */}
      {mastery && mastery.focus_areas.length > 0 && (
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <AlertCircle size={14} className="text-red-400" />
            <h2 className="text-sm font-semibold text-[#1c1410]">Focus Areas</h2>
            <span className="text-xs text-[#9a8c80]">— concepts below 70% mastery</span>
          </div>
          <div className="space-y-2">
            {mastery.focus_areas.map(({ tag, mastery: score }) => (
              <div key={tag} className="flex items-center gap-3">
                <span className="text-xs text-[#1c1410] w-48 truncate">{tag.replace(/_/g, " ")}</span>
                <div className="flex-1 h-1.5 bg-[#f5f0ea] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-red-500 rounded-full"
                    style={{ width: `${score}%` }}
                  />
                </div>
                <span className="text-xs text-red-400 w-10 text-right">{score}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mastery Heatmap */}
      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
        <h2 className="text-sm font-semibold text-[#1c1410]">Concept Mastery Map</h2>
        {mastery ? (
          <MasteryHeatmap data={mastery} />
        ) : (
          <p className="text-sm text-[#9a8c80]">No mastery data yet. Complete some quiz questions to build your map.</p>
        )}
      </div>

      {/* Wrong Answer Log */}
      {progress && progress.weak_topics.length > 0 && (
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
          <h2 className="text-sm font-semibold text-[#1c1410]">Weak Topics</h2>
          <div className="flex flex-wrap gap-2">
            {progress.weak_topics.map((topic) => (
              <span key={topic} className="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-1 rounded-full">
                {topic.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Module scores */}
      {progress && Object.keys(progress.module_status).length > 0 && (
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 space-y-3">
          <h2 className="text-sm font-semibold text-[#1c1410]">Module Progress</h2>
          <div className="space-y-3">
            {Object.entries(progress.module_status).map(([modId, status]) => {
              const pct = status.total > 0 ? Math.round((status.completed_count / status.total) * 100) : 0;
              return (
                <div key={modId} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-[#1c1410] font-medium">{modId.toUpperCase()}</span>
                    <span className="text-[#9a8c80]">{status.completed_count}/{status.total} · {pct}%</span>
                  </div>
                  <div className="h-1.5 bg-[#f5f0ea] rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-[#a01c2c] to-[#b8822a] rounded-full"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
