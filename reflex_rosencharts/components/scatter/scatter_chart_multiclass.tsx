import { CSSProperties } from "react";
import { scaleLinear, max, min } from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "../../helpers/client_tooltip/ClientTooltip";

/* Ported from rosencharts (MIT, Filsommer). The two hardcoded series are now a single
 * `data` array, each point carrying a `class` field used to pick its color from
 * `classColors`. */

type ScatterPoint = { revenue: number; value: number; company: string; class: string };

const defaultData: ScatterPoint[] = [
  { revenue: 10, value: 102.8, company: "Green A", class: "green" },
  { revenue: 20, value: 101.9, company: "Green B", class: "green" },
  { revenue: 30, value: 101.5, company: "Green C", class: "green" },
  { revenue: 40, value: 100.8, company: "Green D", class: "green" },
  { revenue: 50, value: 99.7, company: "Green E", class: "green" },
  { revenue: 60, value: 98.5, company: "Green F", class: "green" },
  { revenue: 10, value: 98.3, company: "Blue A", class: "blue" },
  { revenue: 20, value: 102.7, company: "Blue B", class: "blue" },
  { revenue: 30, value: 97.4, company: "Blue C", class: "blue" },
  { revenue: 40, value: 99.2, company: "Blue D", class: "blue" },
  { revenue: 50, value: 103.8, company: "Blue E", class: "blue" },
  { revenue: 60, value: 96.5, company: "Blue F", class: "blue" },
];

const defaultClassColors: Record<string, string> = {
  green: "text-lime-500",
  blue: "text-sky-500",
};

export function ScatterChartMulticlass({
  data = defaultData,
  classColors = defaultClassColors,
}: {
  data?: ScatterPoint[];
  classColors?: Record<string, string>;
}) {
  if (data.length === 0) {
    return <div className="relative h-72 w-full" />;
  }

  const revenues = data.map((d) => d.revenue);
  let xScale = scaleLinear()
    .domain([min(revenues) ?? 0, max(revenues) ?? 0])
    .range([0, 100]);
  let yScale = scaleLinear()
    .domain([(min(data.map((d) => d.value)) ?? 0) - 1, (max(data.map((d) => d.value)) ?? 0) + 1])
    .range([100, 0]);

  return (
    <div
      className="relative h-72 w-full"
      style={
        {
          "--marginTop": "0px",
          "--marginRight": "0px",
          "--marginBottom": "25px",
          "--marginLeft": "25px",
        } as CSSProperties
      }
    >
      {/* Y axis */}
      <div
        className="absolute inset-0
          h-[calc(100%-var(--marginTop)-var(--marginBottom))]
          w-[var(--marginLeft)]
          translate-y-[var(--marginTop)]
          overflow-visible
        "
      >
        {yScale
          .ticks(3)
          .map(yScale.tickFormat(3, "d"))
          .map((value, i) => (
            <div
              key={i}
              style={{
                top: `${yScale(+value)}%`,
                left: "0%",
              }}
              className="absolute text-xs tabular-nums -translate-y-1/2 text-gray-500 w-full text-right pr-2"
            >
              {value}
            </div>
          ))}
      </div>

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
          {/* Horizontal grid lines */}
          {yScale
            .ticks(8)
            .map(yScale.tickFormat(8, "d"))
            .map((active, i) => (
              <g
                transform={`translate(0,${yScale(+active)})`}
                className="text-zinc-500/20 dark:text-zinc-700/50"
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

          {/* Vertical grid lines */}
          {xScale.ticks(8).map((active, i) => (
            <g
              transform={`translate(${xScale(active)},0)`}
              className="text-zinc-500/20 dark:text-zinc-700/50"
              key={i}
            >
              <line
                y1={0}
                y2={100}
                stroke="currentColor"
                strokeDasharray="6,5"
                strokeWidth={0.5}
                vectorEffect="non-scaling-stroke"
              />
            </g>
          ))}

          {/* Circles and Tooltips */}
          {data.map((d, index) => (
            <ClientTooltip key={index}>
              <TooltipTrigger>
                <g className="group/tooltip">
                  <path // Real Circle
                    key={index}
                    d={`M ${xScale(d.revenue)} ${yScale(d.value)} l 0.0001 0`}
                    vectorEffect="non-scaling-stroke"
                    strokeWidth="15"
                    strokeLinecap="round"
                    fill="none"
                    stroke="currentColor"
                    className={`${
                      classColors[d.class] ?? "text-violet-400"
                    } group-hover/tooltip:stroke-[20px] transition-all duration-300`}
                  />
                  <path // Invisible bigger circle that triggers the tooltip
                    d={`M ${xScale(d.revenue)} ${yScale(d.value)} l 0.0001 0`}
                    vectorEffect="non-scaling-stroke"
                    strokeWidth="25"
                    strokeLinecap="round"
                    fill="none"
                    stroke="currentColor"
                    className="text-transparent"
                  />
                </g>
              </TooltipTrigger>
              <TooltipContent>
                <div>{d.company}</div>
                <div className="text-gray-500 text-sm">
                  {d.value} / {d.revenue}
                </div>
              </TooltipContent>
            </ClientTooltip>
          ))}
        </svg>
        {/* X Axis */}
        <div className="translate-y-1">
          {data.map((d, i) => {
            const isFirst = i === 0;
            const isLast = i === data.length - 1;
            if (!isFirst && !isLast && i % 5 !== 0) return null;
            return (
              <div key={i} className="overflow-visible text-zinc-500">
                <div
                  style={{
                    left: `${xScale(d.revenue)}%`,
                    top: "100%",
                    transform: `translateX(${
                      i === 0 ? "0%" : i === data.length - 1 ? "-100%" : "-50%"
                    })`,
                  }}
                  className="text-xs absolute"
                >
                  {d.revenue}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
