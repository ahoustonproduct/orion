"use client";

import dynamic from "next/dynamic";
import { GuidedAnalysisBlock as BlockType } from "@/lib/api";
import { Database } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

interface Props { block: BlockType; }

export default function GuidedAnalysisBlock({ block }: Props) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-xs text-[#9a8c80]">
        <Database size={12} />
        <span>Dataset: <code className="text-[#b8822a]">{block.dataset_table}</code></span>
      </div>

      {block.intro && <p className="text-sm text-[#5c4f45]">{block.intro}</p>}

      <div className="space-y-6">
        {block.steps.map((step) => {
          const lineCount = step.code.split("\n").length;
          const height = Math.min(300, Math.max(80, lineCount * 20 + 30));
          return (
            <div key={step.step} className="space-y-2">
              <div className="flex items-center gap-3">
                <div className="w-6 h-6 rounded-full bg-[#a01c2c]/20 text-[#a01c2c] text-xs font-bold flex items-center justify-center shrink-0">
                  {step.step}
                </div>
                <p className="text-sm font-medium text-[#1c1410]">{step.instruction}</p>
              </div>

              <div className="rounded-xl overflow-hidden border border-[#e5ddd4] ml-9">
                <div style={{ height }}>
                  <MonacoEditor
                    value={step.code}
                    language="python"
                    theme="vs-dark"
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      scrollBeyondLastLine: false,
                      fontSize: 12,
                      lineNumbers: "off",
                      padding: { top: 8, bottom: 8 },
                      wordWrap: "off",
                      scrollbar: { horizontal: "auto" },
                    }}
                  />
                </div>
                {step.output && (
                  <div className="bg-[#14110f] border-t border-[#e5ddd4] px-3 py-2">
                    <pre className="text-xs text-[#4ade80] font-mono whitespace-pre-wrap">{step.output}</pre>
                  </div>
                )}
              </div>

              <div className="ml-9 bg-[#f8eaec] border border-[#a01c2c]/20 rounded-lg px-3 py-2">
                <p className="text-xs text-[#821624]">
                  <span className="font-semibold">Business insight: </span>
                  {step.business_implication}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
