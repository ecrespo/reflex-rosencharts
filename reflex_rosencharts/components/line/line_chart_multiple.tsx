import { CSSProperties } from "react";
import { scaleTime, scaleLinear, max, line as d3_line, curveMonotoneX } from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "../../helpers/client_tooltip/ClientTooltip";

/* Ported from rosencharts (MIT, Filsommer). Both series are now props. */

type LinePoint = { date: string; value: number };

const defaultData: LinePoint[] = [
  { date: "2023-04-30", value: 4 },
  { date: "2023-05-01", value: 6 },
  { date: "2023-05-02", value: 8 },
  { date: "2023-05-03", value: 7 },
  { date: "2023-05-04", value: 10 },
  { date: "2023-05-05", value: 12 },
  { date: "2023-05-06", value: 11 },
  { date: "2023-05-07", value: 8 },
  { date: "2023-05-08", value: 7 },
  { date: "2023-05-09", value: 9 },
];
const defaultData2: LinePoint[] = [
  { date: "2023-04-30", value: 3 },
  { date: "2023-05-01", value: 3.5 },
  { date: "2023-05-02", value: 4 },
  { date: "2023-05-03", value: 3.5 },
  { date: "2023-05-04", value: 5 },
  { date: "2023-05-05", value: 5 },
  { date: "2023-05-06", value: 6 },
  { date: "2023-05-07", value: 5.5 },
  { date: "2023-05-08", value: 4 },
  { date: "2023-05-09", value: 5 },
];

export function LineChartMultiple({
  data = defaultData,
  data2 = defaultData2,
  color = "stroke-violet-400",
  color2 = "stroke-fuchsia-400",
}: {
  data?: LinePoint[];
  data2?: LinePoint[];
  color?: string;
  color2?: string;
}) {
  if (data.length === 0) {
    return <div className="relative h-72 w-full" />;
  }
  const parsed = data.map((d) => ({ ...d, date: new Date(d.date) }));
  const parsed2 = data2.map((d) => ({ ...d, date: new Date(d.date) }));

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
  let d2 = line(parsed2);

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
          .ticks(8)
          .map(yScale.tickFormat(8, "d"))
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
          className="overflow-visible w-full h-full"
          preserveAspectRatio="none"
        >
          {/* Grid lines */}
          {yScale
            .ticks(8)
            .map(yScale.tickFormat(8, "d"))
            .map((active, i) => (
              <g
                transform={`translate(0,${yScale(+active)})`}
                className="text-zinc-300 dark:text-zinc-700"
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
            strokeWidth="2"
            vectorEffect="non-scaling-stroke"
          />

          {/* Line 2 */}
          {d2 && (
            <path
              d={d2}
              fill="none"
              className={color2}
              strokeWidth="2"
              vectorEffect="non-scaling-stroke"
            />
          )}

          {/* Circles 1 and Tooltips */}
          {parsed.map((d, index) => (
            <ClientTooltip key={index}>
              <TooltipTrigger>
                <path
                  key={index}
                  d={`M ${xScale(d.date)} ${yScale(d.value)} l 0.0001 0`}
                  vectorEffect="non-scaling-stroke"
                  strokeWidth="7"
                  strokeLinecap="round"
                  fill="none"
                  stroke="currentColor"
                  className="text-violet-300"
                />
                <g className="group/tooltip">
                  {/* Tooltip Line */}
                  <line
                    x1={xScale(d.date)}
                    y1={0}
                    x2={xScale(d.date)}
                    y2={100}
                    stroke="currentColor"
                    strokeWidth={1}
                    className="opacity-0 group-hover/tooltip:opacity-100 text-zinc-300 dark:text-zinc-700 transition-opacity"
                    vectorEffect="non-scaling-stroke"
                    style={{ pointerEvents: "none" }}
                  />
                  {/* Invisible area closest to a specific point for the tooltip trigger */}
                  <rect
                    x={(() => {
                      const prevX = index > 0 ? xScale(parsed[index - 1].date) : xScale(d.date);
                      return (prevX + xScale(d.date)) / 2;
                    })()}
                    y={0}
                    width={(() => {
                      const prevX = index > 0 ? xScale(parsed[index - 1].date) : xScale(d.date);
                      const nextX =
                        index < parsed.length - 1 ? xScale(parsed[index + 1].date) : xScale(d.date);
                      const leftBound = (prevX + xScale(d.date)) / 2;
                      const rightBound = (xScale(d.date) + nextX) / 2;
                      return rightBound - leftBound;
                    })()}
                    height={100}
                    fill="transparent"
                    className="cursor-pointer"
                  />
                </g>
              </TooltipTrigger>
              <TooltipContent>
                <div>
                  {d.date.toLocaleDateString("en-US", {
                    month: "short",
                    day: "2-digit",
                  })}
                </div>
                <div className="text-gray-500 text-sm">{d.value.toLocaleString("en-US")}</div>
              </TooltipContent>
            </ClientTooltip>
          ))}
          {/* Circles 2 */}
          {parsed2.map((d, index) => (
            <path
              key={index}
              d={`M ${xScale(d.date)} ${yScale(d.value)} l 0.0001 0`}
              vectorEffect="non-scaling-stroke"
              strokeWidth="7"
              strokeLinecap="round"
              fill="none"
              stroke="currentColor"
              className="text-fuchsia-300"
            />
          ))}
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
                    transform: `translateX(${
                      i === 0 ? "0%" : i === parsed.length - 1 ? "-100%" : "-50%"
                    })`,
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
    </div>
  );
}
