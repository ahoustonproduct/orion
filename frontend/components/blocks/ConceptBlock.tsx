"use client";

import dynamic from "next/dynamic";
import { ConceptBlock as ConceptBlockType } from "@/lib/api";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

interface Props { block: ConceptBlockType; }

export default function ConceptBlock({ block }: Props) {
  const lineCount = block.code_example.code.split("\n").length;
  const editorHeight = Math.min(520, Math.max(160, lineCount * 20 + 40));

  return (
    <div className="space-y-5">
      <div className="border-l-2 border-[#a01c2c] pl-4 py-1">
        <p className="text-sm text-[#c97a84] italic">{block.fintech_hook}</p>
      </div>

      <div className="space-y-3">
        {block.explanation.split("\n\n").map((para, i) => (
          <p key={i} className="text-sm text-[#5c4f45] leading-relaxed">{para}</p>
        ))}
      </div>

      <div className="rounded-xl overflow-hidden border border-[#e5ddd4]">
        <div className="bg-[#ffffff] px-4 py-2 border-b border-[#e5ddd4] flex items-center justify-between">
          <span className="text-xs text-[#9a8c80] font-mono">{block.code_example.language}</span>
          <span className="text-xs text-[#9a8c80]">Example</span>
        </div>
        <div style={{ height: editorHeight }}>
          <MonacoEditor
            value={block.code_example.code}
            language={block.code_example.language}
            theme="vs-dark"
            options={{
              readOnly: true,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              fontSize: 13,
              lineNumbers: "on",
              padding: { top: 12, bottom: 12 },
              wordWrap: "off",
              scrollbar: { horizontal: "auto" },
            }}
          />
        </div>
        {block.code_example.output && (
          <div className="bg-[#14110f] border-t border-[#e5ddd4] px-4 py-3">
            <p className="text-xs text-[#9a8c80] mb-1">Output:</p>
            <pre className="text-xs text-[#4ade80] font-mono whitespace-pre-wrap">{block.code_example.output}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
