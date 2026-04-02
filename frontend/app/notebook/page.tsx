"use client";

import { useEffect, useState, useCallback } from "react";
import { fetchNote, saveNote, fetchProgress, fetchLesson, fetchModules } from "@/lib/api";
import { getUserKey } from "@/lib/user";
import { Save, FileText, Check, Lightbulb, BookOpen, AlertTriangle, RefreshCw, Wand2, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface StruggleTopic {
  lesson_id: string;
  title: string;
  attempts: number;
  stars: number;
  error?: string;
}

interface ProgressData {
  lessons: { lesson_id: string; stars: number; attempts: number; error?: string }[];
  study_log: Record<string, number>;
}

export default function NotebookPage() {
  const [content, setContent] = useState("");
  const [saved, setSaved] = useState(true);
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  
  // Struggle tracking
  const [struggleTopics, setStruggleTopics] = useState<StruggleTopic[]>([]);
  const [loadingStruggles, setLoadingStruggles] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState<StruggleTopic | null>(null);
  const [topicContent, setTopicContent] = useState("");
  const [generatingContent, setGeneratingContent] = useState(false);

  useEffect(() => {
    const userKey = getUserKey();
    
    // Fetch existing note
    fetchNote(userKey)
      .then((d) => setContent(d.content || generateInitialNote()))
      .catch(() => setContent(generateInitialNote()));
    
    // Fetch progress to find struggles
    fetchProgress(userKey)
      .then((progress: ProgressData) => {
        const struggles: StruggleTopic[] = progress.lessons
          .filter(l => l.stars < 3 || l.attempts > 2 || l.error)
          .map(l => ({
            lesson_id: l.lesson_id,
            title: l.lesson_id.replace(/_/g, " ").replace(/m\d+-l(\d+)/, "Lesson $1"),
            attempts: l.attempts,
            stars: l.stars,
            error: l.error,
          }))
          .slice(0, 10); // Top 10 struggles
        setStruggleTopics(struggles);
        setLoadingStruggles(false);
      })
      .catch(() => setLoadingStruggles(false));
  }, []);

  const generateInitialNote = () => `# My Study Notes

## Quick Reference
- Python basics: variables, lists, dictionaries
- NumPy: arrays, indexing, broadcasting
- Pandas: DataFrames, groupby, merge
- SQL: SELECT, JOIN, GROUP BY

## Today's Goals
- [ ] Complete lesson X
- [ ] Practice challenge Y

---

`;

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

  const generateStudyGuide = async (topic: StruggleTopic) => {
    setSelectedTopic(topic);
    setGeneratingContent(true);
    
    try {
      const lesson = await fetchLesson(topic.lesson_id);
      const guide = `## Study Guide: ${topic.title}

### Why this is challenging
- You attempted this ${topic.attempts} time(s)
- Earned ${topic.stars}/3 stars
${topic.error ? `- Last error: ${topic.error.slice(0, 100)}...` : ""}

### Key Concepts to Review
${lesson.concept?.slice(0, 500) || "Review the lesson concept section."}

### Practice Focus
${lesson.questions?.slice(0, 3).map((q: any) => `- ${q.question}`).join("\n") || "- Complete the challenge"}

### Solution Hint
${lesson.challenge?.solution?.slice(0, 300) || "Check the lesson for the solution."}

---
*Generated from your struggles - review this before your midterm!*
`;
      setTopicContent(guide);
    } catch (e) {
      setTopicContent("Could not generate study guide. Try reviewing the lesson directly.");
    } finally {
      setGeneratingContent(false);
    }
  };

  const insertStruggleNote = () => {
    if (!topicContent) return;
    setContent(prev => prev + "\n\n" + topicContent);
    setSelectedTopic(null);
    setTopicContent("");
  };

  const autoGenerateStudyGuide = async () => {
    if (struggleTopics.length === 0) return;
    
    setGeneratingContent(true);
    let fullGuide = "# Automated Study Guide\n\n## Topics to Review\n\n";
    
    for (const topic of struggleTopics.slice(0, 3)) {
      try {
        const lesson = await fetchLesson(topic.lesson_id);
        fullGuide += `### ${topic.title}\n`;
        fullGuide += `- Attempts: ${topic.attempts}, Stars: ${topic.stars}\n`;
        fullGuide += `- Key: ${lesson.concept?.slice(0, 200) || "Review lesson"}\n\n`;
      } catch {
        fullGuide += `### ${topic.title}\n- (Could not load details)\n\n`;
      }
    }
    
    fullGuide += "\n## Recommendations\n";
    fullGuide += "- Focus on weak areas above\n";
    fullGuide += "- Review code solutions in lessons\n";
    fullGuide += "- Practice similar challenges\n";
    
    setContent(prev => prev + "\n\n" + fullGuide);
    setGeneratingContent(false);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 h-[calc(100vh-4rem)] flex gap-4">
      {/* Main Editor */}
      <div className="flex-1 flex flex-col gap-4 min-w-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText size={18} className="text-[var(--color-accent-light)]" />
            <h1 className="text-xl font-bold text-white">Smart Notebook</h1>
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
              {saving ? <Loader2 size={12} className="animate-spin" /> : saved ? <Check size={12} /> : <Save size={12} />}
              {saving ? "Saving..." : saved ? "Saved" : "Save"}
            </button>
          </div>
        </div>

        <p className="text-xs text-gray-400">
          Auto-saves every 2 seconds. Your struggles are tracked below - click to generate study guides!
        </p>

        <textarea
          value={content}
          onChange={(e) => { setContent(e.target.value); setSaved(false); }}
          placeholder={`# My Study Notes\n\nStart writing...`}
          className="flex-1 bg-[#0f0f1a] border border-white/10 rounded-xl p-4 text-sm text-white font-mono placeholder-gray-600 resize-none outline-none focus:border-[var(--color-accent)] transition-all leading-relaxed"
        />
      </div>

      {/* Sidebar - Struggle Topics */}
      <div className="w-80 shrink-0 space-y-4">
        {/* Auto-generate button */}
        <button
          onClick={autoGenerateStudyGuide}
          disabled={generatingContent || struggleTopics.length === 0}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-hover)] rounded-xl text-white text-sm font-semibold hover:shadow-lg hover:shadow-[var(--color-accent)]/20 transition-all disabled:opacity-50"
        >
          {generatingContent ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <Wand2 size={16} />
          )}
          Generate from My Struggles
        </button>

        {/* Struggle topics */}
        <div className="bg-[#0f0f1a] border border-white/10 rounded-xl p-4 space-y-3">
          <div className="flex items-center gap-2">
            <AlertTriangle size={14} className="text-yellow-500" />
            <h2 className="text-sm font-semibold text-white">Areas to Review</h2>
          </div>
          
          {loadingStruggles ? (
            <div className="flex items-center gap-2 text-gray-400 text-sm">
              <Loader2 size={14} className="animate-spin" />
              Analyzing your progress...
            </div>
          ) : struggleTopics.length === 0 ? (
            <p className="text-xs text-gray-400">
              No struggles yet! Keep learning.
            </p>
          ) : (
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {struggleTopics.map((topic) => (
                <button
                  key={topic.lesson_id}
                  onClick={() => generateStudyGuide(topic)}
                  className="w-full text-left p-3 rounded-lg bg-[#1a1a2e] border border-white/5 hover:border-[var(--color-accent)]/30 transition-all group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="text-xs font-medium text-white truncate">{topic.title}</p>
                      <p className="text-[10px] text-gray-400 mt-1">
                        {topic.attempts} attempts · {topic.stars}/3 stars
                      </p>
                    </div>
                    <Lightbulb size={14} className="text-yellow-500 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Generated content preview */}
        {selectedTopic && (
          <div className="bg-[#0f0f1a] border border-[var(--color-accent)]/30 rounded-xl p-4 space-y-3">
            <div className="flex items-center gap-2">
              <BookOpen size={14} className="text-[var(--color-accent-light)]" />
              <h2 className="text-sm font-semibold text-white">Study Guide Preview</h2>
            </div>
            
            {generatingContent ? (
              <div className="flex items-center gap-2 text-gray-400 text-sm">
                <Loader2 size={14} className="animate-spin" />
                Generating...
              </div>
            ) : (
              <>
                <div className="text-xs text-gray-300 max-h-64 overflow-y-auto whitespace-pre-wrap">
                  {topicContent.slice(0, 500)}...
                </div>
                <button
                  onClick={insertStruggleNote}
                  className="w-full py-2 bg-[var(--color-accent)]/20 border border-[var(--color-accent)]/50 text-[var(--color-accent-light)] rounded-lg text-xs font-medium hover:bg-[var(--color-accent)]/30 transition-all"
                >
                  Insert into Notebook
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}