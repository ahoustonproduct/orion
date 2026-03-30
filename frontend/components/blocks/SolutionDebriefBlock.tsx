import { SolutionDebriefBlock as BlockType } from "@/lib/api";
import { CheckCircle, MessageSquare, Lightbulb } from "lucide-react";

interface Props { block: BlockType; }

export default function SolutionDebriefBlock({ block }: Props) {
  return (
    <div className="space-y-5">
      <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-2">
          <CheckCircle size={14} className="text-green-400" />
          <span className="text-xs font-semibold text-green-400 uppercase tracking-wider">Optimal Decision</span>
        </div>
        <p className="text-sm font-medium text-[#1c1410]">{block.optimal_decision}</p>
        <p className="text-xs text-[#5c4f45] mt-1">{block.decision_rationale}</p>
      </div>

      {block.pl_comparison && block.pl_comparison.length > 0 && (
        <div className="rounded-xl border border-[#e5ddd4] overflow-hidden">
          <div className="bg-[#ffffff] px-4 py-2 border-b border-[#e5ddd4]">
            <p className="text-xs font-semibold text-[#5c4f45] uppercase tracking-wider">Outcome Comparison</p>
          </div>
          <div className="divide-y divide-[#e5ddd4]">
            {block.pl_comparison.map((row, i) => (
              <div key={i} className={`px-4 py-3 ${i === 1 ? "bg-green-500/5" : ""}`}>
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-sm font-medium ${i === 1 ? "text-green-400" : "text-[#1c1410]"}`}>
                    {row.label}
                  </span>
                  {row.monthly_profit && (
                    <span className={`text-sm font-bold ${i === 1 ? "text-green-400" : "text-[#5c4f45]"}`}>
                      {row.monthly_profit}/mo
                    </span>
                  )}
                </div>
                <div className="flex gap-4 text-xs text-[#9a8c80]">
                  {row.approval_rate && <span>Approval: {row.approval_rate}</span>}
                  {row.default_rate && <span>Default: {row.default_rate}</span>}
                </div>
                <p className="text-xs text-[#9a8c80] mt-1 italic">{row.verdict}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <div className="flex items-center gap-2 mb-2">
          <MessageSquare size={14} className="text-[#b8822a]" />
          <span className="text-xs font-semibold text-[#b8822a] uppercase tracking-wider">Stakeholder Communication</span>
        </div>
        <p className="text-sm text-[#5c4f45] leading-relaxed italic">
          &ldquo;{block.stakeholder_communication}&rdquo;
        </p>
      </div>

      <div className="bg-[#f8eaec] border border-[#a01c2c]/30 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-2">
          <Lightbulb size={14} className="text-yellow-400" />
          <span className="text-xs font-semibold text-yellow-400 uppercase tracking-wider">Key Takeaway</span>
        </div>
        <p className="text-sm font-medium text-[#1c1410]">{block.key_takeaway}</p>
      </div>
    </div>
  );
}
