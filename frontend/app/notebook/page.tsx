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

  // Auto-save after 2s of inactivity
  useEffect(() => {
    if (saved) return;
    const timer = setTimeout(save, 2000);
    return () => clearTimeout(timer);
  }, [content, saved, save]);

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 h-[calc(100vh-4rem)] flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText size={18} className="text-[#3b82f6]" />
          <h1 className="text-xl font-bold text-[#e2e8f0]">Notebook</h1>
        </div>
        <div className="flex items-center gap-3">
          {lastSaved && (
            <span className="text-xs text-[#64748b]">
              Saved {lastSaved.toLocaleTimeString()}
            </span>
          )}
          <button
            onClick={save}
            disabled={saved || saving}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#3b82f6] hover:bg-[#2563eb] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            {saved ? <Check size={12} /> : <Save size={12} />}
            {saving ? "Saving..." : saved ? "Saved" : "Save"}
          </button>
        </div>
      </div>

      <p className="text-xs text-[#64748b]">
        Your personal notes. Auto-saves every 2 seconds. Use markdown formatting.
      </p>

      {/* Editor */}
      <textarea
        value={content}
        onChange={(e) => { setContent(e.target.value); setSaved(false); }}
        placeholder={`# My Notes

Use this space to jot down anything you learn...

## Python Basics
- Variables store values: name = "Alice"
- Lists: scores = [85, 92, 78]

## Things to Review
- [ ] List comprehensions
- [ ] Pandas groupby
`}
        className="flex-1 bg-[#1a1a2e] border border-[#2d2d4a] rounded-xl p-4 text-sm text-[#e2e8f0] font-mono placeholder-[#64748b]/50 resize-none outline-none focus:border-[#3b82f6] transition-all leading-relaxed"
      />

      <p className="text-xs text-center text-[#64748b]">
        Tip: Write in markdown — headings with #, bullets with -, code with backticks
      </p>
    </div>
  );
}
