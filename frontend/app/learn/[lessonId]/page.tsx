"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  fetchFinTechLesson, saveProgress,
  type FinTechLesson, type LessonBlock,
} from "@/lib/api";
import { getUserKey } from "@/lib/user";
import {
  ArrowLeft, ChevronLeft, ChevronRight, Clock,
  BookOpen, Lightbulb, Target, Code, HelpCircle, Trophy, Lock,
} from "lucide-react";

import ConceptBlock from "@/components/blocks/ConceptBlock";
import DecisionContextBlock from "@/components/blocks/DecisionContextBlock";
import GuidedAnalysisBlock from "@/components/blocks/GuidedAnalysisBlock";
import DecisionBlock from "@/components/blocks/DecisionBlock";
import TechnicalExerciseBlock from "@/components/blocks/TechnicalExerciseBlock";
import QuizBlock from "@/components/blocks/QuizBlock";
import SolutionDebriefBlock from "@/components/blocks/SolutionDebriefBlock";
import FollowAlongPanel from "@/components/FollowAlongPanel";

const BLOCK_META = [
  { label: "Concept", icon: Lightbulb },
  { label: "Context", icon: BookOpen },
  { label: "Analysis", icon: Code },
  { label: "Decision", icon: Target },
  { label: "Exercise", icon: Code },
  { label: "Quiz", icon: HelpCircle },
  { label: "Debrief", icon: Trophy },
];

const BLOCK_TYPE_ORDER = [
  "concept_block",
  "decision_context_block",
  "guided_analysis_block",
  "decision_block",
  "technical_exercise_block",
  "quiz_block",
  "solution_debrief_block",
];

function renderBlock(block: LessonBlock, lessonId: string) {
  switch (block.type) {
    case "concept_block": return <ConceptBlock block={block} />;
    case "decision_context_block": return <DecisionContextBlock block={block} />;
    case "guided_analysis_block": return <GuidedAnalysisBlock block={block} />;
    case "decision_block": return <DecisionBlock block={block} lessonId={lessonId} />;
    case "technical_exercise_block": return <TechnicalExerciseBlock block={block} />;
    case "quiz_block": return <QuizBlock block={block} lessonId={lessonId} />;
    case "solution_debrief_block": return <SolutionDebriefBlock block={block} />;
    default: return null;
  }
}

export default function LessonPage() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const userKey = getUserKey();

  const [lesson, setLesson] = useState<FinTechLesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [blockIndex, setBlockIndex] = useState(0);
  const [startTime] = useState(Date.now());
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    fetchFinTechLesson(lessonId)
      .then((l) => { setLesson(l); setLoading(false); })
      .catch(() => setLoading(false));
  }, [lessonId]);

  const coreBlocks: LessonBlock[] = lesson
    ? (BLOCK_TYPE_ORDER
        .map((t) => lesson.blocks.find((b) => b.type === t))
        .filter(Boolean) as LessonBlock[])
    : [];

  const isStub = lesson?.status === "coming_soon";
  const stubNotice = lesson?.blocks.find((b) => b.type === "stub_notice");
  const currentBlock = coreBlocks[blockIndex];
  const isFirst = blockIndex === 0;
  const isLast = blockIndex === coreBlocks.length - 1;

  const handleNext = async () => {
    if (isLast) {
      const timeSpent = (Date.now() - startTime) / 60000;
      try {
        await saveProgress(userKey, {
          lesson_id: lessonId, stars: 4, attempts: 1,
          hints_used: 0, completed: true, time_spent_minutes: timeSpent,
        });
      } catch {}
      setCompleted(true);
    } else {
      setBlockIndex((i) => i + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handlePrev = () => {
    if (!isFirst) { setBlockIndex((i) => i - 1); window.scrollTo({ top: 0, behavior: "smooth" }); }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#a01c2c] to-[#b8822a] mx-auto flex items-center justify-center animate-pulse">
            <span className="text-white font-bold">O</span>
          </div>
          <p className="text-sm text-[#9a8c80]">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-[#5c4f45] mb-4">Lesson not found.</p>
        <Link href="/curriculum" className="text-[#a01c2c] text-sm hover:underline">← Back to Curriculum</Link>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center space-y-6">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-400 to-green-600 mx-auto flex items-center justify-center shadow-lg">
          <Trophy size={28} className="text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-[#1c1410] mb-2">Lesson Complete</h1>
          <p className="text-[#5c4f45]">{lesson.title}</p>
        </div>
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4 text-sm text-[#5c4f45]">
          Time spent: {Math.round((Date.now() - startTime) / 60000)} minutes
        </div>
        <div className="flex gap-3">
          <Link
            href={`/curriculum/${lesson.module_id}`}
            className="flex-1 py-3 bg-[#ffffff] border border-[#e5ddd4] hover:border-[#a01c2c] text-[#1c1410] rounded-xl text-sm font-medium transition-all text-center"
          >
            Back to Module
          </Link>
          <Link
            href="/"
            className="flex-1 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all text-center"
          >
            Dashboard
          </Link>
        </div>
      </div>
    );
  }

  if (isStub) {
    const conceptBlock = lesson.blocks.find((b) => b.type === "concept_block");
    return (
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
        <div className="flex items-center gap-3">
          <Link href={`/curriculum/${lesson.module_id}`} className="text-[#9a8c80] hover:text-[#5c4f45]">
            <ArrowLeft size={18} />
          </Link>
          <div className="min-w-0">
            <p className="text-xs text-[#9a8c80]">{lesson.module_id.toUpperCase()}</p>
            <h1 className="text-lg font-bold text-[#1c1410] truncate">{lesson.title}</h1>
          </div>
        </div>
        {conceptBlock && conceptBlock.type === "concept_block" && <ConceptBlock block={conceptBlock} />}
        <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-6 text-center space-y-3">
          <Lock size={24} className="text-[#9a8c80] mx-auto" />
          <p className="text-sm font-medium text-[#1c1410]">Full lesson coming soon</p>
          {stubNotice && stubNotice.type === "stub_notice" && (
            <p className="text-xs text-[#9a8c80]">{stubNotice.message} · Available {stubNotice.available_date}</p>
          )}
        </div>
      </div>
    );
  }

  const blockMeta = BLOCK_META[blockIndex] ?? BLOCK_META[0];
  const BlockIcon = blockMeta.icon;

  return (
    <div className="w-full px-4 py-6">
      <div className="grid grid-cols-[1fr_460px] gap-6 items-start">

        {/* ── Left column: lesson content ── */}
        <div className="space-y-5 min-w-0">
          {/* Header */}
          <div className="flex items-center gap-3">
            <Link href={`/curriculum/${lesson.module_id}`} className="text-[#9a8c80] hover:text-[#5c4f45] shrink-0">
              <ArrowLeft size={18} />
            </Link>
            <div className="flex-1 min-w-0">
              <p className="text-xs text-[#9a8c80]">{lesson.module_id.toUpperCase()}</p>
              <h1 className="text-base font-bold text-[#1c1410] truncate">{lesson.title}</h1>
            </div>
            <div className="flex items-center gap-1 text-xs text-[#9a8c80] shrink-0">
              <Clock size={12} />{lesson.duration_min}m
            </div>
          </div>

          {/* Block progress */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-1.5">
                <BlockIcon size={13} className="text-[#a01c2c]" />
                <span className="text-[#1c1410] font-medium">{blockMeta.label}</span>
              </div>
              <span className="text-[#9a8c80]">Block {blockIndex + 1} of {coreBlocks.length}</span>
            </div>
            <div className="flex gap-1">
              {coreBlocks.map((_, i) => (
                <div
                  key={i}
                  className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                    i < blockIndex ? "bg-[#a01c2c]" : i === blockIndex ? "bg-[#c97a84]" : "bg-[#e5ddd4]"
                  }`}
                />
              ))}
            </div>
          </div>

          {/* Block content */}
          <div className="min-h-[300px]">
            {currentBlock && renderBlock(currentBlock, lessonId)}
          </div>

          {/* Navigation */}
          <div className="flex gap-3 pt-2 pb-4">
            <button
              onClick={handlePrev}
              disabled={isFirst}
              className="flex items-center gap-2 px-4 py-3 bg-[#ffffff] border border-[#e5ddd4] disabled:opacity-30 text-[#5c4f45] rounded-xl text-sm transition-all hover:enabled:border-[#a01c2c]"
            >
              <ChevronLeft size={16} />Back
            </button>
            <button
              onClick={handleNext}
              className="flex-1 flex items-center justify-center gap-2 py-3 bg-[#a01c2c] hover:bg-[#821624] text-white rounded-xl text-sm font-semibold transition-all"
            >
              {isLast ? "Complete Lesson" : "Continue"}
              <ChevronRight size={16} />
            </button>
          </div>
        </div>

        {/* ── Right column: follow-along panel ── */}
        <div className="sticky top-4" style={{ height: "calc(100vh - 2rem)" }}>
          <FollowAlongPanel currentBlock={currentBlock} blockIndex={blockIndex} />
        </div>

      </div>
    </div>
  );
}
