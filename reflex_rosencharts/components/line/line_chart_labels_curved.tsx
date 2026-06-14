import { CSSProperties } from "react";
import { scaleTime, scaleLinear, max, line as d3_line, curveMonotoneX } from "d3";

/* Ported from rosencharts (MIT, Filsommer). Data is now a prop. */

type LinePoint = { date: string; value: number };

const defaultData: LinePoint[] = [
  { date: "2023-04-30", value: 3 },
  { date: "2023-05-01", value: 6 },
  { date: "2023-05-02", value: 8 },
  { date: "2023-05-03", value: 6 },
  { date: "2023-05-04", value: 10 },
  { date: "2023-05-05", value: 12 },
  { date: "2023-05-06", value: 11 },
  { date: "2023-05-07", value: 8 },
  { date: "2023-05-08", value: 4 },
  { date: "2023-05-09", value: 9 },
  { date: "2023-05-10", value: 9 },
];

export function LineChartLabelsCurved({
  data = defaultData,
  color = "text-purple-300",
}: {
  data?: LinePoint[];
  color?: string;
}) {
  if (data.length === 0) {
    return <div className="relative h-72 w-full" />;
  }
  const parsed = data.map((d) => ({ ...d, date: new Date(d.date) }));

  let xScale = scaleTime()
    .domain([parsed[0].date, parsed[parsed.length - 1].date])
    .range([0, 100]);
  let yScale = scaleLinear()
    .domain([0, max(parsed.map((d) => d.value)) ?? 0])
    .range([100, 0]);

  let line = d3_line<(typeof parsed)[number]>()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.value))
    .curve(curveMonotoneX);

  let d = line(parsed);

  if (!d) {
    return null;
  }

  return (
    <div
      className="relative h-72 w-full"
      style={
        {
          "--marginTop": "0px",
          "--marginRight": "8px",
          "--marginBottom": "25px",
          "--marginLeft": "10px",
        } as CSSProperties
      }
    >
      {/* Chart area */}
      <div
        className="absolute inset-0
          h-[calc(100%-var(--marginTop)-var(--marginBottom))]
          w-[calc(100%-var(--marginLeft)-var(--marginRight))]
          translate-x-[var(--marginLeft)]
          translate-y-[var(--marginTop)]
          overflow-visible
        "
      >
        <svg
          viewBox="0 0 100 100"
          className="w-full h-full overflow-visible"
          preserveAspectRatio="none"
        >
          {/* Grid lines */}
          {yScale
            .ticks(8)
            .map(yScale.tickFormat(8, "d"))
            .map((active, i) => (
              <g
                transform={`translate(0,${yScale(+active)})`}
                className="text-zinc-200 dark:text-zinc-800"
                key={i}
              >
                <line
                  x1={0}
                  x2={100}
                  stroke="currentColor"
                  strokeDasharray="6,5"
                  strokeWidth={0.5}
                  vectorEffect="non-scaling-stroke"
                />
              </g>
            ))}

          {/* Line */}
          <path
            d={d}
            fill="none"
            className={color}
            stroke="currentColor"
            strokeWidth="2"
            vectorEffect="non-scaling-stroke"
          />
        </svg>
        <div className="translate-y-2">
          {/* X Axis */}
          {parsed.map((day, i) => {
            const isFirst = i === 0;
            const isLast = i === parsed.length - 1;
            const isMax = day.value === Math.max(...parsed.map((d) => d.value));
            if (!isFirst && !isLast && !isMax) return null;
            return (
              <div key={i} className="overflow-visible text-zinc-500">
                <div
                  style={{
                    left: `${xScale(day.date)}%`,
                    top: "100%",
                    transform: `translateX(${i === 0 ? "0%" : i === parsed.length - 1 ? "-100%" : "-50%"})`,
                  }}
                  className="text-xs absolute"
                >
                  {day.date.toLocaleDateString("en-US", {
                    month: "numeric",
                    day: "numeric",
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {/* Labels */}
      <div
        className="
        h-[calc(100%-var(--marginTop)-var(--marginBottom))]
        w-[calc(100%-var(--marginLeft)-var(--marginRight))]
        translate-x-[var(--marginLeft)]
        translate-y-[var(--marginTop)]
      "
      >
        {parsed.map((entry, i) => (
          <div
            key={i}
            style={{
              top: `${yScale(entry.value)}%`,
              left: `${xScale(entry.date)}%`,
              transform: "translate(-50%, -50%)",
            }}
            className="absolute bg-purple-50 dark:bg-zinc-900 border border-purple-300 rounded-full text-xs text-zinc-700 dark:text-zinc-200 size-5 flex items-center justify-center"
          >
            {entry.value}
          </div>
        ))}
      </div>
    </div>
  );
}
