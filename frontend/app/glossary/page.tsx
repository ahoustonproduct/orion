"use client";

import { useEffect, useState } from "react";
import { fetchGlossary, type GlossaryEntry } from "@/lib/api";
import { Search } from "lucide-react";

const MODULE_COLORS: Record<string, string> = {
  Python: "bg-green-700/10 text-green-700 border-green-700/30",
  "Data Analytics": "bg-cyan-700/10 text-cyan-700 border-cyan-700/30",
  SQL: "bg-purple-700/10 text-purple-700 border-purple-700/30",
  ML: "bg-orange-700/10 text-orange-700 border-orange-700/30",
  AI: "bg-yellow-700/10 text-yellow-700 border-yellow-700/30",
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
      <div>
        <h1 className="text-xl font-bold text-[var(--color-text-primary)]">Glossary</h1>
        <p className="text-sm text-[var(--color-text-muted)]">{entries.length} terms across all modules.</p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]" />
        <input
          type="text"
          placeholder="Search terms..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-9 pr-4 py-2.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl text-sm text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] outline-none focus:border-[var(--color-accent)] transition-all"
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
                ? "bg-[var(--color-accent)] text-white border-[var(--color-accent)]"
                : "bg-[var(--color-surface)] border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent)]"
            }`}
          >
            {m}
          </button>
        ))}
      </div>

      {/* Results */}
      <div className="space-y-2">
        {filtered.length === 0 && (
          <p className="text-sm text-[var(--color-text-muted)] text-center py-8">No terms found.</p>
        )}
        {filtered.map((entry) => (
          <div key={entry.term} className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-xl p-4">
            <div className="flex items-start justify-between gap-2 mb-1">
              <p className="font-semibold text-sm text-[var(--color-text-primary)]">{entry.term}</p>
              <span className={`text-xs px-2 py-0.5 rounded-full border shrink-0 ${MODULE_COLORS[entry.module] ?? "bg-[var(--color-surface-2)] text-[var(--color-text-secondary)] border-[var(--color-border)]"}`}>
                {entry.module}
              </span>
            </div>
            <p className="text-xs text-[var(--color-text-secondary)] leading-relaxed">{entry.definition}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
