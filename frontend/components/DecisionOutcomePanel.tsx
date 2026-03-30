import { DecisionEvaluateResponse } from "@/lib/api";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface Props {
  outcome: DecisionEvaluateResponse;
  userValue: unknown;
  decisionType: string;
}

export default function DecisionOutcomePanel({ outcome, userValue, decisionType }: Props) {
  const score = Math.round(outcome.score * 100);
  const isNearOptimal = score >= 80;
  const delta = outcome.user_outcome - outcome.optimal_outcome;

  const fmt = (n: number) => {
    if (Math.abs(n) >= 1000) return `$${Math.round(n).toLocaleString()}`;
    return n.toFixed(2);
  };

  const scoreColor = score >= 80 ? "text-green-400" : score >= 60 ? "text-yellow-400" : "text-red-400";
  const barColor = score >= 80 ? "bg-green-500" : score >= 60 ? "bg-yellow-500" : "bg-red-500";
  const borderColor = score >= 80 ? "border-green-500/30 bg-green-500/5" : score >= 60 ? "border-yellow-500/30 bg-yellow-500/5" : "border-red-500/30 bg-red-500/5";

  return (
    <div className="space-y-4 mt-4">
      <div className={`rounded-xl p-4 border ${borderColor}`}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-semibold text-[#1c1410]">Decision Score</span>
          <span className={`text-2xl font-bold ${scoreColor}`}>{score}/100</span>
        </div>
        <div className="h-2 bg-[#f5f0ea] rounded-full overflow-hidden">
          <div className={`h-full rounded-full transition-all ${barColor}`} style={{ width: `${score}%` }} />
        </div>
      </div>

      <div className="rounded-xl border border-[#e5ddd4] overflow-hidden">
        <div className="bg-[#ffffff] px-4 py-2 border-b border-[#e5ddd4]">
          <p className="text-xs font-semibold text-[#5c4f45] uppercase tracking-wider">Outcome Comparison</p>
        </div>
        <div className="divide-y divide-[#e5ddd4]">
          {[
            { label: "Your Decision", value: outcome.user_outcome, highlight: false, icon: delta >= -100 ? <Minus size={14} /> : <TrendingDown size={14} />, color: isNearOptimal ? "text-green-400" : "text-yellow-400" },
            { label: "Optimal Decision", value: outcome.optimal_outcome, highlight: true, icon: <TrendingUp size={14} />, color: "text-green-400" },
            { label: "Worst Case", value: outcome.worst_outcome, highlight: false, icon: <TrendingDown size={14} />, color: "text-red-400" },
          ].map((row) => (
            <div key={row.label} className={`flex items-center justify-between px-4 py-3 ${row.highlight ? "bg-green-500/5" : ""}`}>
              <div className="flex items-center gap-2">
                <span className={row.color}>{row.icon}</span>
                <span className="text-sm text-[#5c4f45]">{row.label}</span>
              </div>
              <span className={`text-sm font-semibold ${row.color}`}>{fmt(row.value)}/mo</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-[#faf7f3] border border-[#e5ddd4] rounded-xl px-4 py-3">
        <p className="text-sm text-[#5c4f45]">
          {Math.abs(delta) < 100
            ? "You matched the optimal decision closely."
            : delta < 0
            ? `Your decision costs ${fmt(Math.abs(delta))}/month vs. the optimal policy.`
            : `Your decision exceeded optimal by ${fmt(delta)}/month — may indicate excess risk.`}
        </p>
      </div>

      {outcome.explanation && (
        <div className="bg-[#f8eaec] border border-[#a01c2c]/20 rounded-xl px-4 py-3">
          <p className="text-xs text-[#821624]">{outcome.explanation}</p>
        </div>
      )}
    </div>
  );
}
