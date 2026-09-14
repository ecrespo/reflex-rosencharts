/**
 * Shared axis helpers for the rosencharts chart wrappers.
 *
 * The original rosencharts components derive their axes from the data points
 * themselves: the first and last element become the domain and every n-th point
 * becomes a label. That breaks on clustered or unsorted real-world data —
 * labels land at irregular positions and overlap, the extreme points get cut in
 * half, and the chart silently depends on the caller sorting the data.
 *
 * These helpers replace that with:
 *   - a domain built from the *extent* of the values, snapped outwards to a
 *     round tick step in a single pass (d3's `nice()` iterates and can inflate
 *     a domain by 20% or more, which wastes the plotting area);
 *   - ticks generated from that same step, so the grid lines and the axis
 *     labels are the same list and always line up;
 *   - a margin expressed in the *range* instead of the domain, so a mark is
 *     kept fully inside the plot area no matter what the domain ends up being;
 *   - tooltip bands computed on a sorted copy, so the result does not depend on
 *     the order the data arrives in.
 */
import { useEffect, useRef, useState } from "react";
import { scaleLinear, scaleLog, scaleSymlog, tickStep } from "d3";

/** Scale types a chart can be asked for. */
export type ScaleKind = "linear" | "log" | "symlog";

/** The slice of the d3 continuous-scale API the charts actually use. */
export type NumericScale = {
  (value: number): number;
  domain(): number[];
  ticks(count?: number): number[];
  tickFormat(count?: number, specifier?: string): (value: number) => string;
};

/** A tick: its value, its label and its position in the scale's range (0-100). */
export type AxisTick = { value: number; label: string; position: number };

/** A scale plus the ticks that both the grid and the axis labels are drawn from. */
export type Axis = { scale: NumericScale; ticks: AxisTick[] };

/** Ticks requested when the available width is unknown. */
export const DEFAULT_TICK_COUNT = 5;

/** Range margin (% of the plot area) used before the size has been measured. */
export const DEFAULT_INSET = 4;

/** Never eat more than this share of the plot area with the range margin. */
const MAX_INSET = 25;

/** Hard stop for the tick loop; a sane axis never comes close. */
const MAX_TICKS = 60;

/** Approximate width in px of one `text-xs` character. */
const CHAR_WIDTH = 7;

/** `pr-2` on the y-axis label + a little breathing room. */
const LABEL_PADDING = 10;

function minMax(values: number[]): [number, number] | null {
  let lo = Infinity;
  let hi = -Infinity;
  for (const value of values) {
    if (!Number.isFinite(value)) continue;
    if (value < lo) lo = value;
    if (value > hi) hi = value;
  }
  return lo === Infinity ? null : [lo, hi];
}

/** Widen a zero-width extent so the scale cannot return NaN. */
function widen([lo, hi]: [number, number]): [number, number] {
  if (lo !== hi) return [lo, hi];
  const pad = Math.abs(lo) * 0.05 || 1;
  return [lo - pad, hi + pad];
}

function formatTick(value: number, decimals: number): string {
  const text = value.toFixed(decimals);
  return /^-0(\.0+)?$/.test(text) ? text.slice(1) : text;
}

/**
 * A range that keeps a mark of `markRadius` px fully inside the plot area:
 * the data is mapped to [inset, 100 - inset] instead of [0, 100], so the
 * margin is exact in pixels and survives any domain rounding.
 *
 * `lengthPx` is the plot area's size along the axis; pass `reverse` for the y
 * axis, whose range runs from the bottom up.
 */
export function insetRange(
  lengthPx: number,
  markRadius: number,
  reverse: boolean = false,
): [number, number] {
  const inset =
    Number.isFinite(lengthPx) && lengthPx > 0
      ? Math.min(MAX_INSET, (markRadius / lengthPx) * 100)
      : DEFAULT_INSET;
  return reverse ? [100 - inset, inset] : [inset, 100 - inset];
}

/**
 * Build an axis: a scale over the extent of `values` plus the regular ticks to
 * label it with. The linear domain is snapped outwards to whole tick steps, so
 * the first tick is at or below the minimum and the last at or above the
 * maximum — a value never sits past the outermost labelled reference.
 *
 * `kind: "log"` falls back to `"symlog"` when any value is <= 0, because a log
 * domain has to be strictly positive. A log axis spanning a decade or more
 * keeps d3's powers of ten; a narrower log axis and symlog use the same snapped
 * steps as linear, placed non-linearly. Both drop labels that would collide
 * with their neighbour.
 */
export function buildAxis(
  values: number[],
  range: [number, number],
  options: { kind?: ScaleKind; tickCount?: number; lengthPx?: number } = {},
): Axis {
  const kind = options.kind ?? "linear";
  const tickCount = Math.max(2, options.tickCount ?? DEFAULT_TICK_COUNT);
  const [lo, hi] = widen(minMax(values) ?? [0, 1]);
  const effective: ScaleKind = kind === "log" && lo <= 0 ? "symlog" : kind;

  // A log axis spanning a decade or more is labelled with d3's powers of ten.
  if (effective === "log" && Math.log10(hi / lo) >= 1) {
    const scale = scaleLog().domain([lo, hi]).range(range) as unknown as NumericScale;
    const format = scale.tickFormat(tickCount);
    const candidates = scale
      .ticks(tickCount)
      .map((value) => ({ value, label: format(value), position: scale(value) }))
      .filter((tick) => tick.label !== "" && Number.isFinite(tick.position));
    return { scale, ticks: thin(candidates, options.lengthPx) };
  }

  // Everything else gets regular steps snapped outwards. Under a narrow log
  // axis d3 would blank most labels, and symlog ticks are linear values anyway;
  // those two only place the steps non-linearly and drop colliding labels.
  const step = tickStep(lo, hi, tickCount);
  if (!Number.isFinite(step) || step <= 0) {
    const scale = scaleLinear().domain([lo, hi]).range(range) as unknown as NumericScale;
    return { scale, ticks: [] };
  }
  let first = Math.floor(lo / step) * step;
  const last = Math.ceil(hi / step) * step;
  let start = first;
  // A log domain has to stay strictly positive: keep the minimum as the edge
  // and start labelling at the first whole step above it.
  if (effective === "log" && first <= 0) {
    first = lo;
    start = Math.ceil(lo / step) * step;
  }
  const base =
    effective === "log" ? scaleLog() : effective === "symlog" ? scaleSymlog() : scaleLinear();
  const scale = base.domain([first, last]).range(range) as unknown as NumericScale;

  const decimals = Math.max(0, -Math.floor(Math.log10(step)));
  const ticks: AxisTick[] = [];
  const count = Math.min(MAX_TICKS, Math.round((last - start) / step) + 1);
  for (let i = 0; i < count; i++) {
    const value = start + i * step;
    ticks.push({ value, label: formatTick(value, decimals), position: scale(value) });
  }
  return { scale, ticks: effective === "linear" ? ticks : thin(ticks, options.lengthPx) };
}

/**
 * Drop ticks whose labels would run into their neighbour's. The outermost
 * ticks always survive, so both ends of the axis stay labelled.
 */
function thin(ticks: AxisTick[], lengthPx?: number): AxisTick[] {
  if (ticks.length < 2) return ticks;
  const widest = ticks.reduce((n, tick) => Math.max(n, tick.label.length), 0);
  const minGap =
    Number.isFinite(lengthPx) && (lengthPx as number) > 0
      ? ((widest * CHAR_WIDTH + 6) / (lengthPx as number)) * 100
      : 6;
  const kept: AxisTick[] = [];
  for (const tick of ticks) {
    const previous = kept[kept.length - 1];
    if (!previous || Math.abs(tick.position - previous.position) >= minGap) kept.push(tick);
  }
  const lastTick = ticks[ticks.length - 1];
  if (kept[kept.length - 1] !== lastTick) {
    if (kept.length >= 2) kept[kept.length - 1] = lastTick;
    else kept.push(lastTick);
  }
  return kept.length >= 2 ? kept : ticks.slice(0, 2);
}

/** How many x ticks fit in `width` px without the labels running into each other. */
export function responsiveTickCount(
  width: number,
  options: { perTick?: number; min?: number; max?: number; fallback?: number } = {},
): number {
  const perTick = options.perTick ?? 72;
  const min = options.min ?? 2;
  const max = options.max ?? 8;
  const fallback = options.fallback ?? DEFAULT_TICK_COUNT;
  if (!Number.isFinite(width) || width <= 0) return fallback;
  return Math.max(min, Math.min(max, Math.floor(width / perTick)));
}

/** `translateX` that keeps a label sitting exactly on an edge inside the area. */
export function labelShift(position: number): string {
  if (position <= 0.5) return "0%";
  if (position >= 99.5) return "-100%";
  return "-50%";
}

/** Left gutter wide enough for the longest y label, so it never wraps. */
export function axisMarginLeft(labels: string[], minimum: number = 25): string {
  let longest = 0;
  for (const label of labels) longest = Math.max(longest, label.length);
  return `${Math.max(minimum, Math.ceil(longest * CHAR_WIDTH) + LABEL_PADDING)}px`;
}

/** Normalize a margin prop: a number means px, a string is used as-is. */
export function cssLength(value: number | string | undefined | null, fallback: string): string {
  if (value === undefined || value === null || value === "") return fallback;
  return typeof value === "number" ? `${value}px` : value;
}

/** Numeric px value of a CSS length, or `fallback` for any other unit. */
export function pxValue(value: string, fallback: number = 0): number {
  const match = /^\s*(-?[\d.]+)px\s*$/.exec(value);
  return match ? Number.parseFloat(match[1]) : fallback;
}

/**
 * Invisible bands that trigger each point's tooltip, reaching half-way to the
 * neighbours *along the x axis*. Computed on a sorted copy (the input is never
 * mutated), so unsorted data yields the same bands and never a negative width.
 * Points that share an x value are ordered by `tiebreak` so the result depends
 * only on the data, not on the order it arrived in. Aligned with `values`.
 */
export function tooltipBands(
  values: number[],
  toX: (value: number) => number,
  tiebreak?: number[],
): { x: number; width: number }[] {
  const order = values.map((_, index) => index).sort((a, b) => {
    const delta = values[a] - values[b];
    if (delta !== 0) return delta;
    return tiebreak ? tiebreak[a] - tiebreak[b] : 0;
  });
  const rank = new Array<number>(values.length);
  order.forEach((original, position) => {
    rank[original] = position;
  });
  const positions = values.map(toX);
  return values.map((_, index) => {
    const position = rank[index];
    const current = positions[index];
    const previous = position > 0 ? positions[order[position - 1]] : current;
    const next = position < order.length - 1 ? positions[order[position + 1]] : current;
    const left = (previous + current) / 2;
    const right = (current + next) / 2;
    return { x: left, width: Math.max(0, right - left) };
  });
}

/** Track an element's width so the tick count can adapt to the viewport. */
export function useElementWidth<T extends HTMLElement>() {
  const ref = useRef<T | null>(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    setWidth(element.getBoundingClientRect().width);
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) setWidth(entry.contentRect.width);
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return [ref, width] as const;
}
