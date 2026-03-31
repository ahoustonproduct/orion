"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchModules, fetchProgress, type Module, type ProgressData } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Lock, ChevronRight, Clock, BookOpen } from "lucide-react";

export default function CurriculumPage() {
  const [modules, setModules] = useState<Module[]>([]);
  const [progress, setProgress] = useState<ProgressData | null>(null);

  useEffect(() => {
    const userKey = getUserKey();
    Promise.all([fetchModules(), fetchProgress(userKey)])
      .then(([mods, prog]) => { setModules(mods); setProgress(prog); })
      .catch(console.error);
  }, []);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      <h1 className="text-xl font-bold text-[#1c1410]">Curriculum</h1>
      <p className="text-sm text-[#5c4f45]">4 modules — Python, Data Analytics, SQL, Machine Learning.</p>

      <div className="space-y-3">
        {modules.map((module, idx) => {
          const status = progress?.module_status[module.id];
          const unlocked = status?.unlocked ?? idx === 0;
          const completedInMod = status?.completed_count ?? 0;
          const pct = module.lesson_count ? (completedInMod / module.lesson_count) * 100 : 0;

          return (
            <Link
              key={module.id}
              href={unlocked ? `/curriculum/${module.id}` : "#"}
              className={`block p-4 rounded-xl border transition-all ${
                unlocked
                  ? "bg-[#ffffff] border-[#e5ddd4] hover:border-[#a01c2c]"
                  : "bg-[#ffffff]/40 border-[#e5ddd4]/40 opacity-50 cursor-not-allowed"
              }`}
            >
              <div className="flex items-start gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 ${
                  pct === 100 ? "bg-green-500/20 text-green-400" :
                  unlocked ? "bg-[#a01c2c]/20 text-[#a01c2c]" :
                  "bg-[#e5ddd4] text-[#9a8c80]"
                }`}>
                  {unlocked ? (pct === 100 ? "✓" : module.order) : <Lock size={12} />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm text-[#1c1410]">{module.title}</p>
                  <p className="text-xs text-[#a01c2c] mb-1">{module.course}</p>
                  <p className="text-xs text-[#9a8c80] mb-2">{module.description}</p>
                  <div className="flex items-center gap-3 text-xs text-[#9a8c80]">
                    <span className="flex items-center gap-1"><BookOpen size={11} /> {module.lesson_count} lessons</span>
                    <span className="flex items-center gap-1"><Clock size={11} /> ~{module.lesson_count * 18} min</span>
                    {unlocked && <span className="text-[#a01c2c]">{completedInMod}/{module.lesson_count} done</span>}
                  </div>
                  {unlocked && (
                    <div className="h-1 bg-[#f5f0ea] rounded-full mt-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-[#a01c2c] to-[#b8822a] rounded-full"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  )}
                </div>
                {unlocked && <ChevronRight size={16} className="text-[#9a8c80] shrink-0 mt-1" />}
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
