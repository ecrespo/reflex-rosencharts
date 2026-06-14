import React, { CSSProperties } from "react";

/* Ported from rosencharts (MIT, Filsommer): other-charts/5_FunnelChart.tsx.
 * Render technique: centered, gradient-filled <div> bars stacked top-to-bottom,
 * sorted by descending value. Data ({name, value}) is now a prop; per-stage
 * gradient classes come from the `colors` palette (indexed after sorting). */

type FunnelStage = { name: string; value: number };

const defaultData: FunnelStage[] = [
  { name: "Gross Revenue", value: 47.1 },
  { name: "Net Revenue", value: 32.3 },
  { name: "EBITDA", value: 27.1 },
  { name: "Gross Profit", value: 17.5 },
  { name: "Net Profit", value: 12.7 },
];

const defaultColors = [
  "from-pink-300 to-pink-400 dark:from-pink-500 dark:to-pink-700",
  "from-purple-400 to-purple-500 dark:from-purple-500 dark:to-purple-700",
  "from-indigo-400 to-indigo-500 dark:from-indigo-500 dark:to-indigo-700",
  "from-sky-400 to-sky-500 dark:from-sky-500 dark:to-sky-700",
  "from-orange-300 to-orange-400 dark:from-amber-500 dark:to-amber-700",
];

export function FunnelChart({
  data = defaultData,
  colors = defaultColors,
}: {
  data?: FunnelStage[];
  colors?: string[];
}) {
  if (data.length === 0) {
    return <div className="relative h-72 w-full" />;
  }

  const sorted = [...data].sort((a, b) => b.value - a.value);

  const gap = 0.3; // gap between bars
  const maxFrequency = Math.max(...sorted.map((d) => d.value));
  const barHeight = 54;
  let cumulativeHeight = 0;

  return (
    <div
      className="relative mt-4 h-72"
      style={
        {
          "--marginTop": "8px",
          "--marginRight": "0px",
          "--marginBottom": "0px",
          "--marginLeft": "0px",
          "--height": `${barHeight * sorted.length + gap * (sorted.length - 1)}px`,
        } as CSSProperties
      }
    >
      {/* Bars with Gradient Fill and Lighter Stroke for 3D Effect */}
      {sorted.map((d, index) => {
        const barWidth = (d.value / maxFrequency) * 100;
        const yPosition = cumulativeHeight;
        cumulativeHeight += barHeight + gap + 2;
        const colorClass = colors[index % colors.length];

        return (
          <div
            key={index}
            className={`relative bg-gradient-to-b ${colorClass} rounded-md`}
            style={{
              position: "absolute",
              top: `${yPosition}px`,
              left: `${(100 - barWidth) / 2}%`,
              width: `${barWidth}%`,
              height: `${barHeight}px`,
            }}
          >
            <div
              style={{
                position: "absolute",
                top: `${barHeight / 6}px`,
                width: "100%",
                textAlign: "center",
                color: "white",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              {d.name}
            </div>
            <div
              style={{
                position: "absolute",
                top: `${barHeight / 2}px`,
                width: "100%",
                textAlign: "center",
                color: "white",
                fontSize: "12px",
                fontWeight: "bold",
                fontFamily: "monospace",
              }}
            >
              {d.value}
            </div>
          </div>
        );
      })}
    </div>
  );
}
