import { DecisionContextBlock as BlockType } from "@/lib/api";
import { Building2, AlertTriangle, Users } from "lucide-react";

interface Props { block: BlockType; }

export default function DecisionContextBlock({ block }: Props) {
  return (
    <div className="space-y-4">
      <div className="bg-[#f8eaec] border border-[#a01c2c]/30 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-2">
          <Building2 size={14} className="text-[#a01c2c]" />
          <span className="text-xs font-semibold text-[#a01c2c] uppercase tracking-wider">{block.company}</span>
        </div>
        <p className="text-sm font-medium text-[#1c1410]">Your Role: {block.role}</p>
      </div>

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <h3 className="text-xs font-semibold text-[#5c4f45] uppercase tracking-wider mb-2">Scenario</h3>
        <p className="text-sm text-[#1c1410] leading-relaxed">{block.scenario}</p>
      </div>

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <AlertTriangle size={14} className="text-yellow-500" />
          <h3 className="text-xs font-semibold text-yellow-500 uppercase tracking-wider">Hard Constraints</h3>
        </div>
        <ul className="space-y-1.5">
          {block.constraints.map((c, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-[#1c1410]">
              <span className="text-yellow-500 mt-0.5 shrink-0">→</span>
              {c}
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <Users size={14} className="text-[#b8822a]" />
          <h3 className="text-xs font-semibold text-[#b8822a] uppercase tracking-wider">Stakeholder Pressures</h3>
        </div>
        <div className="space-y-2">
          {block.stakeholder_pressures.map((sp, i) => (
            <div key={i} className="flex gap-3">
              <span className="text-xs font-semibold text-[#1c1410] shrink-0 w-28">{sp.stakeholder}:</span>
              <span className="text-xs text-[#5c4f45] italic">"{sp.pressure}"</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
