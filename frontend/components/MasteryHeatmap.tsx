import { MasteryData } from "@/lib/api";

interface Props { data: MasteryData; }

export default function MasteryHeatmap({ data }: Props) {
  const getColors = (mastery: number) => {
    if (mastery >= 80) return { bg: "bg-green-500/80 border-green-500/40", text: "text-green-100" };
    if (mastery >= 60) return { bg: "bg-yellow-500/80 border-yellow-500/40", text: "text-yellow-100" };
    return { bg: "bg-red-500/80 border-red-500/40", text: "text-red-100" };
  };

  if (data.heatmap_data.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-sm text-[#9a8c80]">Complete some lessons to see your mastery map.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-4 text-xs text-[#9a8c80]">
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-green-500/80 inline-block" />≥80% Mastered
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-yellow-500/80 inline-block" />60–79% Developing
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-red-500/80 inline-block" />&lt;60% Focus Area
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {data.heatmap_data.map((item) => {
          const { bg, text } = getColors(item.mastery);
          return (
            <div
              key={item.tag}
              title={`${item.tag}: ${item.mastery}% mastery (${item.attempts} attempts)`}
              className={`rounded-lg border px-3 py-2 ${bg}`}
            >
              <p className={`text-xs font-medium ${text}`}>{item.tag.replace(/_/g, " ")}</p>
              <p className={`text-xs ${text} opacity-80`}>{item.mastery}%</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
