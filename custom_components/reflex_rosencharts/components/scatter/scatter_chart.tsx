import { CSSProperties } from "react";
import {
  axisMarginLeft,
  buildAxis,
  cssLength,
  insetRange,
  labelShift,
  pxValue,
  responsiveTickCount,
  tooltipBands,
  useElementWidth,
  type ScaleKind,
} from "$/public/external/reflex_rosencharts/components/helpers/chart_axis/ChartAxis.tsx";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

type ScatterPoint = { revenue: number; value: number; company?: string };

// Default dataset = the original rosencharts example.
const DEFAULT_DATA: ScatterPoint[] = [
  { revenue: 10, value: 102.8, company: "Company A" },
  { revenue: 20, value: 101.9, company: "Company B" },
  { revenue: 30, value: 101.5, company: "Company C" },
  { revenue: 40, value: 100.2, company: "Company D" },
  { revenue: 50, value: 100.8, company: "Company E" },
  { revenue: 60, value: 99.7, company: "Company F" },
  { revenue: 70, value: 99.9, company: "Company G" },
  { revenue: 80, value: 98.5, company: "Company H" },
  { revenue: 90, value: 98.9, company: "Company I" },
  { revenue: 100, value: 97.8, company: "Company J" },
  { revenue: 110, value: 98.2, company: "Company K" },
  { revenue: 120, value: 96.8, company: "Company L" },
  { revenue: 130, value: 96.9, company: "Company M" },
  { revenue: 140, value: 95.5, company: "Company N" },
  { revenue: 150, value: 95.9, company: "Company O" },
  { revenue: 160, value: 94.5, company: "Company P" },
  { revenue: 170, value: 94.8, company: "Company Q" },
  { revenue: 180, value: 93.9, company: "Company R" },
  { revenue: 190, value: 94.3, company: "Company S" },
  { revenue: 200, value: 93.5, company: "Company T" },
];

const MARGIN_TOP = 0;
const MARGIN_RIGHT = 0;
const MARGIN_BOTTOM = 25;
const PLOT_HEIGHT = 288 - MARGIN_TOP - MARGIN_BOTTOM; // h-72 minus the x-axis strip
const MARK_RADIUS = 10; // half of the 20px hover stroke, so no dot is ever cut
const Y_TICK_COUNT = 5;

export function ScatterChart({
  data = DEFAULT_DATA,
  xScale: xKind = "linear",
  yScale: yKind = "linear",
  marginLeft: marginLeftProp,
}: {
  data?: ScatterPoint[];
  xScale?: ScaleKind;
  yScale?: ScaleKind;
  marginLeft?: number | string;
}) {
  // Width drives how many x labels fit; measured, so it also works on mobile.
  const [containerRef, containerWidth] = useElementWidth<HTMLDivElement>();
  const points = Array.isArray(data) ? data : [];

  const y = buildAxis(points.map((d) => d.value), insetRange(PLOT_HEIGHT, MARK_RADIUS, true), {
    kind: yKind,
    tickCount: Y_TICK_COUNT,
    lengthPx: PLOT_HEIGHT,
  });
  // Left gutter follows the longest y label, so "1000" never wraps onto two lines.
  const marginLeft = cssLength(marginLeftProp, axisMarginLeft(y.ticks.map((tick) => tick.label)));
  const plotWidth = Math.max(0, containerWidth - pxValue(marginLeft, 25) - MARGIN_RIGHT);
  const xTickCount = responsiveTickCount(plotWidth);
  const x = buildAxis(points.map((d) => d.revenue), insetRange(plotWidth, MARK_RADIUS), {
    kind: xKind,
    tickCount: xTickCount,
    lengthPx: plotWidth,
  });
  // Tooltip bands come from a sorted copy: the input order never matters.
  const bands = tooltipBands(points.map((d) => d.revenue), x.scale, points.map((d) => d.value));

  if (points.length === 0) {
    return <div ref={containerRef} className="relative h-72 w-full" />;
  }

  return (
    <div
      ref={containerRef}
      className="relative h-72 w-full"
      style={
        {
          "--marginTop": `${MARGIN_TOP}px`,
          "--marginRight": `${MARGIN_RIGHT}px`,
          "--marginBottom": `${MARGIN_BOTTOM}px`,
          "--marginLeft": marginLeft,
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
        {y.ticks.map((tick, i) => (
          <div
            key={i}
            style={{
              top: `${tick.position}%`,
              left: "0%",
            }}
            className="absolute text-xs tabular-nums whitespace-nowrap -translate-y-1/2 text-gray-500 w-full text-right pr-2"
          >
            {tick.label}
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
          {/* Horizontal grid lines (same ticks as the labels, so they line up) */}
          {y.ticks.map((tick, i) => (
            <g
              transform={`translate(0,${tick.position})`}
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
          {x.ticks.map((tick, i) => (
            <g
              transform={`translate(${tick.position},0)`}
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
          {points.map((d, index) => (
            <ClientTooltip key={index}>
              <TooltipTrigger>
                <g className="group/tooltip">
                  <path // Real Circle
                    key={index}
                    d={`M ${x.scale(d.revenue)} ${y.scale(d.value)} l 0.0001 0`}
                    vectorEffect="non-scaling-stroke"
                    strokeWidth="10"
                    strokeLinecap="round"
                    fill="none"
                    stroke="currentColor"
                    className="text-violet-400 group-hover/tooltip:stroke-[20px] transition-all duration-300"
                  />
                  <line // Tooltip Line
                    x1={x.scale(d.revenue)}
                    y1={0}
                    x2={x.scale(d.revenue)}
                    y2={100}
                    stroke="currentColor"
                    strokeWidth={1}
                    className="opacity-0 group-hover/tooltip:opacity-100 text-zinc-300 dark:text-zinc-700 transition-opacity"
                    vectorEffect="non-scaling-stroke"
                    style={{ pointerEvents: "none" }}
                  />
                  {/* Invisible area closest to a specific point for the tooltip trigger */}
                  <rect
                    x={bands[index].x}
                    y={0}
                    width={bands[index].width}
                    height={100}
                    fill="transparent"
                    className="cursor-pointer"
                  />
                  {/* …and the dot itself, so clustered points stay reachable */}
                  <path
                    d={`M ${x.scale(d.revenue)} ${y.scale(d.value)} l 0.0001 0`}
                    vectorEffect="non-scaling-stroke"
                    strokeWidth="18"
                    strokeLinecap="round"
                    fill="none"
                    stroke="currentColor"
                    className="text-transparent cursor-pointer"
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
          {x.ticks.map((tick, i) => (
            <div key={i} className="overflow-visible text-zinc-500">
              <div
                style={{
                  left: `${tick.position}%`,
                  top: "100%",
                  // Keep a label sitting exactly on an edge inside the chart area.
                  transform: `translateX(${labelShift(tick.position)})`,
                }}
                className="text-xs tabular-nums absolute"
              >
                {tick.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
