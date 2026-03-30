"use client";

import { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import { executePython, executeSQL, type LessonBlock, type ExecuteResult, type SQLResult } from "@/lib/api";
import { Play, RotateCcw, CheckCircle, XCircle, AlertCircle, ChevronDown, ChevronUp } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

// ── Error explanation parser ──────────────────────────────────────────────────

function explainError(errorText: string): string {
  const e = errorText.toLowerCase();
  if (e.includes("nameerror")) {
    const match = errorText.match(/name '(\w+)' is not defined/);
    const varName = match?.[1] ?? "variable";
    return `"${varName}" hasn't been defined yet. Check your spelling or make sure you assigned a value to it before using it.`;
  }
  if (e.includes("syntaxerror")) {
    if (e.includes("invalid syntax")) return "Python can't parse this line. Common causes: missing colon after if/for/def, mismatched parentheses, or an unclosed string.";
    if (e.includes("unexpected indent")) return "This line is indented but shouldn't be — it's outside any block.";
    if (e.includes("expected an indented block")) return "The line after a colon (if/for/def) must be indented.";
    return "Syntax error — Python can't read this line. Check for missing colons, parentheses, or quotes.";
  }
  if (e.includes("indentationerror")) return "Indentation problem. Make sure you're using consistent spaces (not tabs mixed with spaces).";
  if (e.includes("typeerror")) {
    if (e.includes("unsupported operand")) return "You're trying to use an operator (like + or *) on incompatible types — e.g. adding a string to a number.";
    if (e.includes("not callable")) return "You're calling something as a function that isn't one — check if you added () where they don't belong.";
    return "Type mismatch — the operation doesn't work on this data type.";
  }
  if (e.includes("valueerror")) return "The value is the right type but an unexpected value — e.g. converting a non-numeric string to int().";
  if (e.includes("keyerror")) {
    const match = errorText.match(/KeyError: (.+)/);
    return `Key ${match?.[1] ?? ""} doesn't exist in the dictionary. Check the key name or use .get() to avoid this error.`;
  }
  if (e.includes("indexerror")) return "List index out of range — you're trying to access a position that doesn't exist in the list.";
  if (e.includes("attributeerror")) {
    const match = errorText.match(/has no attribute '(\w+)'/);
    return `This object doesn't have a "${match?.[1] ?? "property"}" attribute. Check the variable type or spelling.`;
  }
  if (e.includes("zerodivisionerror")) return "Division by zero. Add a check before dividing: `if denominator != 0`.";
  if (e.includes("importerror") || e.includes("modulenotfounderror")) return "This module isn't available in the sandbox. Use only standard Python — pandas and math are available.";
  if (e.includes("filenotfounderror")) return "File access isn't allowed in the sandbox. Use the SQL editor to query the bundled datasets instead.";
  return "An error occurred. Read the message carefully — it usually tells you the line number and what went wrong.";
}

// ── Diff comparison ───────────────────────────────────────────────────────────

interface DiffLine {
  expected: string;
  actual: string;
  match: boolean;
}

function diffOutputs(expected: string, actual: string): { lines: DiffLine[]; accuracy: number } {
  const expLines = expected.trim().split("\n");
  const actLines = actual.trim().split("\n");
  const len = Math.max(expLines.length, actLines.length);
  const lines: DiffLine[] = [];
  let matches = 0;
  for (let i = 0; i < len; i++) {
    const exp = expLines[i]?.trim() ?? "";
    const act = actLines[i]?.trim() ?? "";
    const match = exp === act;
    if (match) matches++;
    lines.push({ expected: exp, actual: act, match });
  }
  return { lines, accuracy: len > 0 ? Math.round((matches / len) * 100) : 100 };
}

// ── Derive initial code from current block ───────────────────────────────────

function getInitialCode(block: LessonBlock | undefined): { code: string; language: "python" | "sql"; expectedOutput?: string } {
  if (!block) return { code: "# Start typing your code here\n", language: "python" };

  switch (block.type) {
    case "concept_block":
      return {
        code: block.code_example.code,
        language: (block.code_example.language === "sql" ? "sql" : "python"),
        expectedOutput: block.code_example.output,
      };
    case "guided_analysis_block":
      return {
        code: block.steps[0]?.code ?? "# Follow along with the analysis steps\n",
        language: "python",
        expectedOutput: block.steps[0]?.output,
      };
    case "technical_exercise_block":
      return {
        code: block.standard.starter_code,
        language: block.language,
        expectedOutput: block.standard.expected_output,
      };
    default:
      return { code: "# Type your code here to follow along\n", language: "python" };
  }
}

// ── Main component ────────────────────────────────────────────────────────────

interface Props {
  currentBlock: LessonBlock | undefined;
  blockIndex: number;
}

export default function FollowAlongPanel({ currentBlock, blockIndex }: Props) {
  const { code: initCode, language: initLang, expectedOutput: initExpected } = getInitialCode(currentBlock);

  const [code, setCode] = useState(initCode);
  const [language, setLanguage] = useState<"python" | "sql">(initLang);
  const [expectedOutput, setExpectedOutput] = useState<string | undefined>(initExpected);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<ExecuteResult | SQLResult | null>(null);
  const [expandedError, setExpandedError] = useState<string | null>(null);
  const [showDiff, setShowDiff] = useState(false);
  const prevBlockIndex = useRef(blockIndex);

  // Pre-populate when block changes
  useEffect(() => {
    if (blockIndex !== prevBlockIndex.current) {
      prevBlockIndex.current = blockIndex;
      const { code: c, language: l, expectedOutput: e } = getInitialCode(currentBlock);
      setCode(c);
      setLanguage(l);
      setExpectedOutput(e);
      setResult(null);
      setExpandedError(null);
      setShowDiff(false);
    }
  }, [blockIndex, currentBlock]);

  const handleRun = async () => {
    setRunning(true);
    setResult(null);
    setExpandedError(null);
    try {
      if (language === "python") {
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

  const handleReset = () => {
    const { code: c, language: l, expectedOutput: e } = getInitialCode(currentBlock);
    setCode(c);
    setLanguage(l);
    setExpectedOutput(e);
    setResult(null);
    setExpandedError(null);
    setShowDiff(false);
  };

  const isSQLResult = (r: unknown): r is SQLResult =>
    typeof r === "object" && r !== null && "columns" in r;

  const pyResult = result && !isSQLResult(result) ? (result as ExecuteResult) : null;
  const sqlResult = result && isSQLResult(result) ? (result as SQLResult) : null;

  const hasOutput = pyResult
    ? !!(pyResult.output || pyResult.error)
    : sqlResult
    ? !!(sqlResult.columns.length || sqlResult.error)
    : false;

  const diffData =
    pyResult && pyResult.output && expectedOutput
      ? diffOutputs(expectedOutput, pyResult.output)
      : null;

  // Parse error lines from Python traceback for clickable highlights
  const errorLines: { line: string; explanation: string }[] = [];
  if (pyResult?.error) {
    const lines = pyResult.error.split("\n").filter(Boolean);
    lines.forEach((line) => {
      if (line.trim().startsWith("File") || line.includes("Error") || line.includes("Exception")) {
        errorLines.push({ line, explanation: explainError(pyResult.error ?? "") });
      }
    });
  }

  return (
    <div className="flex flex-col h-full bg-[#14110f] border border-[#2c2520] rounded-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-[#2c2520] bg-[#1e1a16] shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-[#a01c2c]" />
          <span className="text-xs font-semibold text-[#f0ece6]">Follow Along</span>
        </div>
        <div className="flex items-center gap-2">
          {/* Language toggle */}
          <div className="flex bg-[#14110f] rounded-lg p-0.5 border border-[#2c2520]">
            {(["python", "sql"] as const).map((l) => (
              <button
                key={l}
                onClick={() => setLanguage(l)}
                className={`px-2.5 py-1 rounded-md text-xs font-mono transition-all ${
                  language === l ? "bg-[#a01c2c] text-white" : "text-[#9a8c80] hover:text-[#9a8c80]"
                }`}
              >
                {l}
              </button>
            ))}
          </div>
          <button
            onClick={handleReset}
            title="Reset to starter code"
            className="p-1.5 rounded-lg text-[#9a8c80] hover:text-[#9a8c80] hover:bg-[#2c2520] transition-all"
          >
            <RotateCcw size={13} />
          </button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 min-h-0">
        <MonacoEditor
          value={code}
          language={language}
          theme="vs-dark"
          onChange={(v) => setCode(v ?? "")}
          options={{
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontSize: 13,
            lineNumbers: "on",
            padding: { top: 12, bottom: 12 },
            wordWrap: "off",
            scrollbar: { horizontal: "auto", vertical: "auto" },
            renderLineHighlight: "line",
            suggestOnTriggerCharacters: true,
          }}
        />
      </div>

      {/* Run bar */}
      <div className="flex items-center gap-2 px-3 py-2 border-t border-[#2c2520] bg-[#1e1a16] shrink-0">
        <button
          onClick={handleRun}
          disabled={running}
          className="flex items-center gap-1.5 px-4 py-1.5 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-lg text-xs font-semibold transition-all"
        >
          <Play size={11} />
          {running ? "Running..." : "Run"}
        </button>
        {hasOutput && result && (
          <span className="text-xs text-[#9a8c80]">
            {isSQLResult(result) ? `${result.row_count} rows` : ""} {result.duration_ms}ms
          </span>
        )}
        {diffData && (
          <button
            onClick={() => setShowDiff((s) => !s)}
            className={`ml-auto flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
              diffData.accuracy === 100
                ? "bg-green-500/20 text-green-400"
                : diffData.accuracy >= 70
                ? "bg-yellow-500/20 text-yellow-400"
                : "bg-red-500/20 text-red-400"
            }`}
          >
            {diffData.accuracy === 100 ? <CheckCircle size={11} /> : <XCircle size={11} />}
            {diffData.accuracy}% match
            {showDiff ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
          </button>
        )}
      </div>

      {/* Output section */}
      {hasOutput && (
        <div className="shrink-0 border-t border-[#2c2520] max-h-[280px] overflow-y-auto">
          {/* Diff view */}
          {showDiff && diffData && (
            <div className="p-3 border-b border-[#2c2520] space-y-1">
              <p className="text-xs font-semibold text-[#9a8c80] mb-2">Output comparison</p>
              {diffData.lines.map((line, i) => (
                <div key={i} className={`rounded px-2 py-0.5 text-xs font-mono ${
                  line.match ? "bg-green-500/10 text-green-300" : "bg-red-500/10"
                }`}>
                  {line.match ? (
                    <span>{line.actual}</span>
                  ) : (
                    <div className="space-y-0.5">
                      <div className="text-red-300">
                        <span className="text-red-500 mr-1">✗ yours:</span>{line.actual || "(empty)"}
                      </div>
                      <div className="text-green-300">
                        <span className="text-green-500 mr-1">✓ expected:</span>{line.expected || "(empty)"}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Python output */}
          {pyResult && (
            <div className="p-3">
              {pyResult.error ? (
                <div className="space-y-1">
                  <p className="text-xs text-red-400 font-semibold mb-1">Error</p>
                  {pyResult.error.split("\n").filter(Boolean).map((line, i) => {
                    const isClickable = line.trim().startsWith("File") || line.includes("Error") || line.includes("Exception");
                    const isExpanded = expandedError === line;
                    return (
                      <div key={i}>
                        <div
                          onClick={() => isClickable && setExpandedError(isExpanded ? null : line)}
                          className={`text-xs font-mono px-2 py-1 rounded transition-all ${
                            isClickable
                              ? "cursor-pointer text-red-300 bg-red-500/10 hover:bg-red-500/20"
                              : "text-[#9a8c80]"
                          }`}
                        >
                          {isClickable && (
                            <AlertCircle size={10} className="inline mr-1 text-red-400" />
                          )}
                          {line}
                        </div>
                        {isExpanded && (
                          <div className="mt-1 mb-1 mx-2 bg-[#1e1a16] border border-[#a01c2c]/30 rounded-lg px-3 py-2">
                            <p className="text-xs text-[#86efac] leading-relaxed">
                              {explainError(line)}
                            </p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <pre className="text-xs text-[#4ade80] font-mono whitespace-pre-wrap leading-relaxed">
                  {pyResult.output || "(no output)"}
                </pre>
              )}
            </div>
          )}

          {/* SQL output */}
          {sqlResult && (
            sqlResult.error ? (
              <div className="p-3">
                <p className="text-xs text-red-400 font-semibold mb-1">SQL Error</p>
                <div
                  onClick={() => setExpandedError(expandedError ? null : sqlResult.error!)}
                  className="text-xs font-mono text-red-300 bg-red-500/10 rounded px-2 py-1 cursor-pointer hover:bg-red-500/20"
                >
                  <AlertCircle size={10} className="inline mr-1" />
                  {sqlResult.error}
                </div>
                {expandedError && (
                  <div className="mt-2 bg-[#1e1a16] border border-[#a01c2c]/30 rounded-lg px-3 py-2">
                    <p className="text-xs text-[#86efac]">{explainError(sqlResult.error)}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-[#1e1a16]">
                      {sqlResult.columns.map((col) => (
                        <th key={col} className="px-3 py-2 text-left text-[#9a8c80] font-medium whitespace-nowrap border-b border-[#2c2520]">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {sqlResult.rows.slice(0, 25).map((row, i) => (
                      <tr key={i} className={i % 2 === 0 ? "bg-[#14110f]" : "bg-[#1e1a16]"}>
                        {(row as unknown[]).map((cell, j) => (
                          <td key={j} className="px-3 py-1.5 text-[#f0ece6] whitespace-nowrap">{String(cell)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {sqlResult.row_count > 25 && (
                  <p className="text-xs text-[#9a8c80] px-3 py-1.5">Showing 25 of {sqlResult.row_count} rows</p>
                )}
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}
