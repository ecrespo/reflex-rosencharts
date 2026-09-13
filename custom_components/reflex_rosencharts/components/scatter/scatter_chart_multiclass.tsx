import { CSSProperties } from "react";
import {
  axisMarginLeft,
  buildAxis,
  cssLength,
  insetRange,
  labelShift,
  pxValue,
  responsiveTickCount,
  useElementWidth,
  type ScaleKind,
} from "$/public/external/reflex_rosencharts/components/helpers/chart_axis/ChartAxis.tsx";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

type ScatterPoint = { revenue: number; value: number; company?: string; category?: string };

// Default dataset = the original rosencharts example (two classes merged via `category`).
const DEFAULT_DATA: ScatterPoint[] = [
  { revenue: 10, value: 102.8, company: "Green A", category: "Green" },
  { revenue: 20, value: 101.9, company: "Green B", category: "Green" },
  { revenue: 30, value: 101.5, company: "Green C", category: "Green" },
  { revenue: 40, value: 100.8, company: "Green D", category: "Green" },
  { revenue: 50, value: 99.7, company: "Green E", category: "Green" },
  { revenue: 60, value: 98.5, company: "Green F", category: "Green" },
  { revenue: 10, value: 98.3, company: "Blue A", category: "Blue" },
  { revenue: 20, value: 102.7, company: "Blue B", category: "Blue" },
  { revenue: 30, value: 97.4, company: "Blue C", category: "Blue" },
  { revenue: 40, value: 99.2, company: "Blue D", category: "Blue" },
  { revenue: 50, value: 103.8, company: "Blue E", category: "Blue" },
  { revenue: 60, value: 96.5, company: "Blue F", category: "Blue" },
];

// Class colors, cycled by category so any number of classes renders.
const CLASS_COLORS = [
  "text-lime-500",
  "text-sky-500",
  "text-fuchsia-500",
  "text-violet-500",
  "text-orange-500",
  "text-emerald-500",
];

const MARGIN_TOP = 0;
const MARGIN_RIGHT = 0;
const MARGIN_BOTTOM = 25;
const PLOT_HEIGHT = 288 - MARGIN_TOP - MARGIN_BOTTOM; // h-72 minus the x-axis strip
const MARK_RADIUS = 10; // half of the 20px hover stroke, so no dot is ever cut
const Y_TICK_COUNT = 5;

export function ScatterChartMulticlass({
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

  // Both axes span every class, so the classes stay comparable.
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

  // Distinct categories (preserve first-seen order), used to pick a class color.
  const categories = Array.from(new Set(points.map((d) => d.category ?? "")));
  const colorFor = (d: ScatterPoint) =>
    CLASS_COLORS[categories.indexOf(d.category ?? "") % CLASS_COLORS.length];

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
            className="absolute text-xs tabular-nums -translate-y-1/2 text-gray-500 w-full text-right pr-2"
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
                    strokeWidth="15"
                    strokeLinecap="round"
                    fill="none"
                    stroke="currentColor"
                    className={`${colorFor(d)} group-hover/tooltip:stroke-[20px] transition-all duration-300`}
                  />
                  <path // Invisible bigger circle that triggers the tooltip
                    d={`M ${x.scale(d.revenue)} ${y.scale(d.value)} l 0.0001 0`}
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
