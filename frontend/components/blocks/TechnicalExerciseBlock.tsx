"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { TechnicalExerciseBlock as BlockType, executePython, executeSQL, ExecuteResult, SQLResult } from "@/lib/api";
import { Play, Lightbulb, Trophy } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

interface Props { block: BlockType; }

export default function TechnicalExerciseBlock({ block }: Props) {
  const [mode, setMode] = useState<"standard" | "challenge">("standard");
  const exercise = mode === "standard" ? block.standard : block.challenge;

  const [code, setCode] = useState(exercise.starter_code);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<ExecuteResult | SQLResult | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  const switchMode = (m: "standard" | "challenge") => {
    setMode(m);
    const ex = m === "standard" ? block.standard : block.challenge;
    setCode(ex.starter_code);
    setResult(null);
    setShowHint(false);
    setShowSolution(false);
  };

  const handleRun = async () => {
    setRunning(true);
    setResult(null);
    try {
      if (block.language === "python") {
        setResult(await executePython(code));
      } else {
        setResult(await executeSQL(code));
      }
    } catch (err) {
      setResult({ output: "", error: String(err), duration_ms: 0 });
    } finally {
      setRunning(false);
    }
  };

  const isSQLResult = (r: unknown): r is SQLResult =>
    typeof r === "object" && r !== null && "columns" in r;

  const solutionLines = exercise.solution.split("\n").length;
  const solutionHeight = Math.min(300, Math.max(100, solutionLines * 19 + 30));

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        {(["standard", "challenge"] as const).map((m) => (
          <button
            key={m}
            onClick={() => switchMode(m)}
            className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
              mode === m
                ? "bg-[#a01c2c] text-white"
                : "bg-[#ffffff] border border-[#e5ddd4] text-[#5c4f45] hover:text-[#1c1410]"
            }`}
          >
            {m === "challenge" ? "⚡ Challenge" : "Standard"}
          </button>
        ))}
      </div>

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <p className="text-sm text-[#1c1410] leading-relaxed">{exercise.instructions}</p>
      </div>

      <div className="rounded-xl overflow-hidden border border-[#e5ddd4]">
        <div className="bg-[#ffffff] px-4 py-2 border-b border-[#e5ddd4] flex items-center justify-between">
          <span className="text-xs text-[#9a8c80] font-mono">{block.language}</span>
          <button
            onClick={handleRun}
            disabled={running}
            className="flex items-center gap-1.5 px-3 py-1 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-lg text-xs font-medium transition-all"
          >
            <Play size={11} />
            {running ? "Running..." : "Run"}
          </button>
        </div>
        <div style={{ height: 260 }}>
          <MonacoEditor
            value={code}
            language={block.language}
            theme="vs-dark"
            onChange={(v) => setCode(v ?? "")}
            options={{
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              fontSize: 13,
              lineNumbers: "on",
              padding: { top: 12, bottom: 12 },
            }}
          />
        </div>
      </div>

      {result && (
        <div className="rounded-xl border border-[#e5ddd4] overflow-hidden">
          <div className="bg-[#14110f] px-4 py-2 border-b border-[#e5ddd4] flex items-center justify-between">
            <span className="text-xs text-[#9a8c80]">Output ({result.duration_ms}ms)</span>
            {isSQLResult(result) && result.error && <span className="text-xs text-red-400">Error</span>}
            {!isSQLResult(result) && (result as ExecuteResult).error && <span className="text-xs text-red-400">Error</span>}
          </div>
          {isSQLResult(result) ? (
            result.error ? (
              <div className="px-4 py-3 bg-red-500/5">
                <pre className="text-xs text-red-400">{result.error}</pre>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-[#ffffff]">
                      {result.columns.map((col) => (
                        <th key={col} className="px-3 py-2 text-left text-[#9a8c80] font-medium whitespace-nowrap">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.rows.slice(0, 20).map((row, i) => (
                      <tr key={i} className={i % 2 === 0 ? "bg-[#faf7f3]" : "bg-[#ffffff]"}>
                        {(row as unknown[]).map((cell, j) => (
                          <td key={j} className="px-3 py-1.5 text-[#1c1410] whitespace-nowrap">{String(cell)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {result.row_count > 20 && (
                  <p className="text-xs text-[#9a8c80] px-3 py-2">Showing 20 of {result.row_count} rows</p>
                )}
              </div>
            )
          ) : (
            <div className="bg-[#14110f] px-4 py-3">
              {(result as ExecuteResult).error ? (
                <pre className="text-xs text-red-400 whitespace-pre-wrap">{(result as ExecuteResult).error}</pre>
              ) : (
                <pre className="text-xs text-[#4ade80] font-mono whitespace-pre-wrap">
                  {(result as ExecuteResult).output || "(no output)"}
                </pre>
              )}
            </div>
          )}
        </div>
      )}

      <button
        onClick={() => setShowHint(!showHint)}
        className="flex items-center gap-2 text-xs text-[#9a8c80] hover:text-[#5c4f45] transition-colors"
      >
        <Lightbulb size={13} className="text-yellow-500" />
        {showHint ? "Hide hint" : "Show hint"}
      </button>
      {showHint && (
        <div className="bg-yellow-500/5 border border-yellow-500/20 rounded-xl px-4 py-3">
          <p className="text-xs text-yellow-200">{exercise.hint}</p>
        </div>
      )}

      <button
        onClick={() => setShowSolution(!showSolution)}
        className="flex items-center gap-2 text-xs text-[#9a8c80] hover:text-[#5c4f45] transition-colors"
      >
        <Trophy size={13} className="text-[#a01c2c]" />
        {showSolution ? "Hide solution" : "Show solution"}
      </button>
      {showSolution && (
        <div className="rounded-xl overflow-hidden border border-[#a01c2c]/30">
          <div className="bg-[#f8eaec] px-4 py-2 border-b border-[#a01c2c]/20">
            <span className="text-xs text-[#a01c2c]">Solution</span>
          </div>
          <div style={{ height: solutionHeight }}>
            <MonacoEditor
              value={exercise.solution}
              language={block.language}
              theme="vs-dark"
              options={{
                readOnly: true,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                fontSize: 12,
                lineNumbers: "on",
                padding: { top: 8, bottom: 8 },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
