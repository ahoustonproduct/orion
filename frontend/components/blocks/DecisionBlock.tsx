"use client";

import { useState } from "react";
import { DecisionBlock as BlockType, DecisionEvaluateResponse, evaluateDecision } from "@/lib/api";
import DecisionOutcomePanel from "@/components/DecisionOutcomePanel";
import { Target } from "lucide-react";

interface Props { block: BlockType; lessonId: string; }

export default function DecisionBlock({ block, lessonId }: Props) {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [outcome, setOutcome] = useState<DecisionEvaluateResponse | null>(null);

  const [sliderValue, setSliderValue] = useState(block.default_value ?? block.slider_min ?? 640);
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [budget, setBudget] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    const cats = block.categories ?? [];
    const total = block.budget_total ?? 100000;
    cats.forEach((c) => { initial[c.id] = Math.floor(total / cats.length); });
    return initial;
  });
  const [matrix, setMatrix] = useState<Record<string, string>>(() => {
    const m: Record<string, string> = {};
    (block.segments ?? []).forEach((s) => { m[s.id] = (block.options_per_segment ?? ["standard"])[1] ?? "standard"; });
    return m;
  });
  const [justification, setJustification] = useState("");

  const getUserValue = () => {
    switch (block.decision_type) {
      case "numeric_threshold": return sliderValue;
      case "policy_choice": return selectedOption;
      case "budget_allocation": return budget;
      case "approval_matrix": return matrix;
      case "written_justification": return justification;
      default: return null;
    }
  };

  const canSubmit = () => {
    if (block.decision_type === "policy_choice") return !!selectedOption;
    if (block.decision_type === "written_justification") return justification.trim().length >= 20;
    return true;
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const result = await evaluateDecision(lessonId, "decision_block", block.decision_type, getUserValue());
      setOutcome(result);
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Target size={16} className="text-[#a01c2c]" />
        <h3 className="text-sm font-semibold text-[#1c1410]">Your Decision</h3>
      </div>

      <p className="text-sm text-[#5c4f45]">{block.prompt}</p>

      {/* Numeric Threshold */}
      {block.decision_type === "numeric_threshold" && (
        <div className="space-y-3 bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-[#9a8c80]">{block.slider_min}</span>
            <span className="text-2xl font-bold text-[#a01c2c]">{sliderValue}</span>
            <span className="text-xs text-[#9a8c80]">{block.slider_max}</span>
          </div>
          <input
            type="range"
            min={block.slider_min} max={block.slider_max} step={block.slider_step ?? 5}
            value={sliderValue}
            onChange={(e) => setSliderValue(Number(e.target.value))}
            disabled={submitted}
            className="w-full accent-[#a01c2c]"
          />
        </div>
      )}

      {/* Policy Choice */}
      {block.decision_type === "policy_choice" && block.options && (
        <div className="space-y-2">
          {block.options.map((opt) => (
            <button
              key={opt.id}
              onClick={() => !submitted && setSelectedOption(opt.id)}
              disabled={submitted}
              className={`w-full text-left p-4 rounded-xl border transition-all ${
                selectedOption === opt.id
                  ? "border-[#a01c2c] bg-[#a01c2c]/10"
                  : "border-[#e5ddd4] bg-[#ffffff] hover:border-[#a01c2c]/50"
              }`}
            >
              <p className="text-sm font-medium text-[#1c1410]">{opt.label}</p>
              <p className="text-xs text-[#9a8c80] mt-1">{opt.description}</p>
              {opt.risk_level && (
                <span className={`mt-2 inline-block text-xs px-2 py-0.5 rounded-full ${
                  opt.risk_level === "low" ? "bg-green-500/20 text-green-400" :
                  opt.risk_level === "high" ? "bg-red-500/20 text-red-400" :
                  "bg-yellow-500/20 text-yellow-400"
                }`}>{opt.risk_level} risk</span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* Budget Allocation */}
      {block.decision_type === "budget_allocation" && block.categories && (
        <div className="space-y-3 bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-4">
          <div className="flex justify-between text-xs">
            <span className="text-[#9a8c80]">Total: ${(block.budget_total ?? 100000).toLocaleString()}</span>
            <span className={
              Object.values(budget).reduce((a, b) => a + b, 0) === (block.budget_total ?? 100000)
                ? "text-green-400" : "text-red-400"
            }>Allocated: ${Object.values(budget).reduce((a, b) => a + b, 0).toLocaleString()}</span>
          </div>
          {block.categories.map((cat) => (
            <div key={cat.id} className="space-y-1">
              <div className="flex justify-between">
                <span className="text-xs font-medium text-[#1c1410]">{cat.label}</span>
                <span className="text-xs text-[#a01c2c]">${(budget[cat.id] ?? 0).toLocaleString()}</span>
              </div>
              <p className="text-xs text-[#9a8c80]">{cat.description}</p>
              <input
                type="range" min={0} max={block.budget_total ?? 100000} step={1000}
                value={budget[cat.id] ?? 0}
                onChange={(e) => setBudget((prev) => ({ ...prev, [cat.id]: Number(e.target.value) }))}
                disabled={submitted}
                className="w-full accent-[#a01c2c]"
              />
            </div>
          ))}
        </div>
      )}

      {/* Approval Matrix */}
      {block.decision_type === "approval_matrix" && block.segments && (
        <div className="space-y-2">
          {block.segments.map((seg) => (
            <div key={seg.id} className="bg-[#ffffff] border border-[#e5ddd4] rounded-xl p-3 flex items-center justify-between gap-3">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-[#1c1410]">{seg.label}</p>
                {seg.fraud_rate && (
                  <p className="text-xs text-[#9a8c80]">Fraud: {seg.fraud_rate} · Avg: ${seg.avg_amount}</p>
                )}
              </div>
              <div className="flex gap-1 shrink-0">
                {(block.options_per_segment ?? ["strict", "standard", "lenient"]).map((opt) => (
                  <button
                    key={opt}
                    onClick={() => !submitted && setMatrix((prev) => ({ ...prev, [seg.id]: opt }))}
                    disabled={submitted}
                    className={`px-2 py-1 rounded-lg text-xs capitalize transition-all ${
                      matrix[seg.id] === opt
                        ? opt === "strict" ? "bg-red-500/20 text-red-400 border border-red-500/50"
                          : opt === "lenient" ? "bg-green-500/20 text-green-400 border border-green-500/50"
                          : "bg-[#a01c2c]/20 text-[#a01c2c] border border-[#a01c2c]/50"
                        : "bg-[#faf7f3] text-[#9a8c80] border border-[#e5ddd4] hover:border-[#a01c2c]/30"
                    }`}
                  >{opt}</button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Written Justification */}
      {block.decision_type === "written_justification" && (
        <div className="space-y-2">
          <textarea
            value={justification}
            onChange={(e) => setJustification(e.target.value)}
            disabled={submitted}
            placeholder="Write your recommendation in 2-3 sentences. Be specific about which data supports your decision and what business outcome you expect..."
            rows={5}
            className="w-full bg-[#ffffff] border border-[#e5ddd4] rounded-xl px-4 py-3 text-sm text-[#1c1410] placeholder-[#9a8c80] outline-none focus:border-[#a01c2c] transition-all resize-none"
          />
          <p className="text-xs text-[#9a8c80]">{justification.length} characters</p>
          {block.key_concepts_required && block.key_concepts_required.length > 0 && (
            <p className="text-xs text-[#9a8c80]">
              Key concepts to address: {block.key_concepts_required.join(", ")}
            </p>
          )}
        </div>
      )}

      {!submitted && (
        <button
          onClick={handleSubmit}
          disabled={loading || !canSubmit()}
          className="w-full py-3 bg-[#a01c2c] hover:bg-[#821624] disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition-all"
        >
          {loading ? "Evaluating..." : "Lock In Decision →"}
        </button>
      )}

      {submitted && outcome && (
        <DecisionOutcomePanel
          outcome={outcome}
          userValue={getUserValue()}
          decisionType={block.decision_type}
        />
      )}
    </div>
  );
}
