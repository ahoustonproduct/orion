"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchWeekData, streamWeekReview, type WeekData } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import OrionPanel from "@/components/OrionPanel";
import { ArrowLeft, Calendar, Clock, BookOpen, Star } from "lucide-react";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export default function WeekReviewPage() {
  const router = useRouter();
  const userKey = getUserKey();
  const [weekData, setWeekData] = useState<WeekData | null>(null);
  const [orionText, setOrionText] = useState("");
  const [orionLoading, setOrionLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWeekData(userKey)
      .then((data) => {
        setWeekData(data);
        setLoading(false);
        setOrionLoading(true);
        streamWeekReview(userKey, data, (chunk) => setOrionText((p) => p + chunk))
          .then(() => setOrionLoading(false))
          .catch(() => setOrionLoading(false));
      })
      .catch(() => setLoading(false));
  }, [userKey]);

  const today = new Date();
  const monday = new Date(today);
  monday.setDate(today.getDate() - today.getDay() + 1);

  const weekDays = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    const key = d.toISOString().split("T")[0];
    const minutes = weekData?.study_log[key] ?? 0;
    return { label: DAYS[i], date: key, minutes, isToday: key === today.toISOString().split("T")[0] };
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-400 text-sm">Loading week data...</div>
      </div>
    );
  }

  const avgStars = weekData && Object.keys(weekData.stars_earned).length > 0
    ? (Object.values(weekData.stars_earned).reduce((a, b) => a + b, 0) / Object.keys(weekData.stars_earned).length).toFixed(1)
    : "—";

  return (
    <div className="max-w-xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center gap-3">
        <button onClick={() => router.back()} className="text-gray-400 hover:text-gray-300 transition-colors">
          <ArrowLeft size={18} />
        </button>
        <div>
          <h1 className="text-lg font-bold text-white">Week in Review</h1>
          <p className="text-xs text-gray-400">Your learning this week</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        {[
          { icon: <Calendar size={15} />, value: `${weekData?.days_studied ?? 0}/7`, label: "Days Studied", color: "text-blue-400" },
          { icon: <Clock size={15} />, value: `${weekData?.total_minutes ?? 0}m`, label: "Total Time", color: "text-green-400" },
          { icon: <Star size={15} />, value: avgStars, label: "Avg Stars", color: "text-yellow-400" },
        ].map(({ icon, value, label, color }) => (
          <div key={label} className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl p-3 text-center">
            <div className={`flex items-center justify-center gap-1 ${color} mb-1`}>
              {icon}
              <span className="text-base font-bold text-white">{value}</span>
            </div>
            <p className="text-gray-400 text-xs">{label}</p>
          </div>
        ))}
      </div>

      <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl p-4 space-y-3">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Daily Activity</p>
        <div className="flex items-end gap-2 h-20">
          {weekDays.map(({ label, minutes, isToday }) => {
            const maxMin = 60;
            const heightPct = Math.min((minutes / maxMin) * 100, 100);
            const goalMet = minutes >= 30;
            return (
              <div key={label} className="flex-1 flex flex-col items-center gap-1">
                <div className="w-full bg-black/20 rounded-t-md overflow-hidden" style={{ height: "64px" }}>
                  <div
                    className={`w-full rounded-t-md transition-all duration-500 ${
                      goalMet ? "bg-gradient-to-t from-[var(--color-accent)] to-[var(--color-accent-hover)]" : "bg-black/10"
                    }`}
                    style={{ height: `${heightPct}%`, marginTop: `${100 - heightPct}%` }}
                  />
                </div>
                <span className={`text-[10px] font-medium ${isToday ? "text-[var(--color-accent-light)]" : "text-gray-400"}`}>
                  {label}
                </span>
                {minutes > 0 && (
                  <span className="text-[9px] text-gray-500">{minutes}m</span>
                )}
              </div>
            );
          })}
        </div>
        <p className="text-[10px] text-gray-500">Goal: 30 min/day — colored bars = goal met</p>
      </div>

      {weekData && weekData.lessons_completed.length > 0 && (
        <div className="glass-card border-white/5 border border-white/10 border-transparent rounded-xl p-4 space-y-3">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
            Lessons Completed ({weekData.lessons_completed.length})
          </p>
          <div className="space-y-1.5">
            {weekData.lessons_completed.map((title, i) => {
              const lessonId = Object.keys(weekData.stars_earned)[i];
              const stars = lessonId ? weekData.stars_earned[lessonId] : 0;
              return (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <BookOpen size={12} className="text-[var(--color-accent-light)] shrink-0" />
                    <p className="text-sm text-gray-300 truncate">{title}</p>
                  </div>
                  {stars > 0 && (
                    <span className="text-yellow-400 text-xs shrink-0">{"★".repeat(stars)}</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Orion&apos;s Review</p>
        <OrionPanel content={orionText} loading={orionLoading} title="This Week" />
      </div>
    </div>
  );
}
