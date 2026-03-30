"use client";

import { useEffect, useState } from "react";
import { fetchGlossary, type GlossaryEntry } from "@/lib/api";
import { Search } from "lucide-react";

const MODULE_COLORS: Record<string, string> = {
  Python: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  "Data Analytics": "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
  SQL: "bg-purple-500/10 text-purple-400 border-purple-500/20",
  ML: "bg-green-500/10 text-green-400 border-green-500/20",
  AI: "bg-orange-500/10 text-orange-400 border-orange-500/20",
};

export default function GlossaryPage() {
  const [entries, setEntries] = useState<GlossaryEntry[]>([]);
  const [search, setSearch] = useState("");
  const [moduleFilter, setModuleFilter] = useState("All");

  useEffect(() => {
    fetchGlossary().then(setEntries).catch(console.error);
  }, []);

  const modules = ["All", ...Array.from(new Set(entries.map((e) => e.module)))];

  const filtered = entries.filter((e) => {
    const matchSearch = search === "" ||
      e.term.toLowerCase().includes(search.toLowerCase()) ||
      e.definition.toLowerCase().includes(search.toLowerCase());
    const matchModule = moduleFilter === "All" || e.module === moduleFilter;
    return matchSearch && matchModule;
  });

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      <h1 className="text-xl font-bold text-[#e2e8f0]">Glossary</h1>
      <p className="text-sm text-[#94a3b8]">{entries.length} terms across all modules.</p>

      {/* Search */}
      <div className="relative">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#64748b]" />
        <input
          type="text"
          placeholder="Search terms..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-9 pr-4 py-2.5 bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl text-sm text-[#e2e8f0] placeholder-[#64748b] outline-none focus:border-[#3b82f6] transition-all"
        />
      </div>

      {/* Module filters */}
      <div className="flex gap-2 flex-wrap">
        {modules.map((m) => (
          <button
            key={m}
            onClick={() => setModuleFilter(m)}
            className={`px-3 py-1 rounded-full text-xs border transition-all ${
              moduleFilter === m
                ? "bg-[#3b82f6] text-white border-[#3b82f6]"
                : "bg-[#1a1a2e] border-[#2d2d4a] text-[#94a3b8] hover:border-[#3b82f6]"
            }`}
          >
            {m}
          </button>
        ))}
      </div>

      {/* Results */}
      <div className="space-y-2">
        {filtered.length === 0 && (
          <p className="text-sm text-[#64748b] text-center py-8">No terms found.</p>
        )}
        {filtered.map((entry) => (
          <div key={entry.term} className="bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl p-4">
            <div className="flex items-start justify-between gap-2 mb-1">
              <p className="font-semibold text-sm text-[#e2e8f0]">{entry.term}</p>
              <span className={`text-xs px-2 py-0.5 rounded-full border shrink-0 ${MODULE_COLORS[entry.module] ?? "bg-[#242438] text-[#94a3b8] border-[#2d2d4a]"}`}>
                {entry.module}
              </span>
            </div>
            <p className="text-xs text-[#94a3b8] leading-relaxed">{entry.definition}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
