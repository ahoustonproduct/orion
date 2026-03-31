"use client";

import { useEffect, useState, useCallback } from "react";
import { fetchNote, saveNote } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Save, FileText, Check } from "lucide-react";

export default function NotebookPage() {
  const [content, setContent] = useState("");
  const [saved, setSaved] = useState(true);
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  useEffect(() => {
    fetchNote(getUserKey())
      .then((d) => setContent(d.content))
      .catch(console.error);
  }, []);

  const save = useCallback(async () => {
    setSaving(true);
    await saveNote(getUserKey(), content).catch(console.error);
    setSaved(true);
    setSaving(false);
    setLastSaved(new Date());
  }, [content]);

  useEffect(() => {
    if (saved) return;
    const timer = setTimeout(save, 2000);
    return () => clearTimeout(timer);
  }, [content, saved, save]);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 h-[calc(100vh-4rem)] flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText size={18} className="text-[var(--color-accent-light)]" />
          <h1 className="text-xl font-bold text-white">Notebook</h1>
        </div>
        <div className="flex items-center gap-3">
          {lastSaved && (
            <span className="text-xs text-gray-400">
              Saved {lastSaved.toLocaleTimeString()}
            </span>
          )}
          <button
            onClick={save}
            disabled={saved || saving}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20 hover:bg-[var(--color-accent-hover)] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            {saved ? <Check size={12} /> : <Save size={12} />}
            {saving ? "Saving..." : saved ? "Saved" : "Save"}
          </button>
        </div>
      </div>

      <p className="text-xs text-gray-400">
        Your personal notes. Auto-saves every 2 seconds. Use markdown formatting.
      </p>

      <textarea
        value={content}
        onChange={(e) => { setContent(e.target.value); setSaved(false); }}
        placeholder={`# My Notes\n\nUse this space to jot down anything you learn...`}
        className="flex-1 bg-black/20 border border-white/10 rounded-xl p-4 text-sm text-white font-mono placeholder-gray-600 resize-none outline-none focus:border-[var(--color-accent)] transition-all leading-relaxed"
      />

      <p className="text-xs text-center text-gray-400">
        Tip: Write in markdown — headings with #, bullets with -, code with backticks
      </p>
    </div>
  );
}
