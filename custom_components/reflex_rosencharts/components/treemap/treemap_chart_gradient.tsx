import React from "react";
import * as d3 from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

interface ExtendedHierarchyNode<T> extends d3.HierarchyNode<T> {
  x0: number;
  x1: number;
  y0: number;
  y1: number;
}

type HierarchyData = {
  name: string;
  value: number;
  children: {
    name: string;
    children: { name: string; value: number }[];
  }[];
};

// Default dataset = the original rosencharts example, preserved as the nested
// hierarchy ({ name: "root", children: [...] }) that feeds d3.hierarchy.
const DEFAULT_DATA: HierarchyData = {
  name: "root",
  value: 0,
  children: [
    {
      name: "Tech",
      children: [
        { name: "Apple", value: 100 },
        { name: "Mercedes", value: 120 },
        { name: "Palantir", value: 110 },
      ],
    },
    {
      name: "Financials",
      children: [
        { name: "Tesla", value: 60 },
        { name: "Meta", value: 70 },
        { name: "Google", value: 20 },
      ],
    },
    {
      name: "Energy",
      children: [
        { name: "Apple", value: 70 },
        { name: "Mercedes", value: 50 },
        { name: "Palantir", value: 20 },
        { name: "Google", value: 100 },
      ],
    },
  ],
};

const colors = [
  "bg-gradient-to-b from-purple-400 to-purple-500 text-white dark:from-purple-500 dark:to-purple-700 dark:text-purple-100",
  "bg-gradient-to-b from-pink-300 to-pink-400 text-white dark:from-pink-500 dark:to-pink-600 dark:text-pink-100",
  "bg-gradient-to-b from-orange-300 to-orange-400 text-white dark:from-amber-500 dark:to-amber-600 dark:text-amber-100",
];

const VISIBLE_TEXT_WIDTH = 20;
const VISIBLE_TEXT_HEIGHT = 23;

export function TreemapChartGradient({ data = DEFAULT_DATA }: { data?: any }) {
  if (!data || !data.children || data.children.length === 0) {
    return <div className="relative w-full h-[250px]" />;
  }

  // Create root node
  const root = d3
    .hierarchy<HierarchyData>(data)
    .sum((d) => d.value)
    .sort((a, b) => b.value! - a.value!);

  // Compute the treemap layout
  d3
    .treemap<HierarchyData>()
    .size([100, 100])
    .paddingInner(0.75) // Padding between subtopics
    .paddingOuter(1) // Padding between topics
    .round(false)(root);

  const leaves = root.leaves() as ExtendedHierarchyNode<HierarchyData>[];

  // Color scale
  const color = d3
    .scaleOrdinal()
    .domain(data.children.map((d: any) => d.name))
    .range(colors);

  return (
    <div className="relative w-full h-[250px]">
      {leaves.map((leaf, i) => {
        const leafWidth = leaf.x1 - leaf.x0;
        const leafHeight = leaf.y1 - leaf.y0;

        return (
          <ClientTooltip key={i}>
            <TooltipTrigger>
              <div
                key={i}
                className={color(leaf.parent!.data.name) as string}
                style={{
                  position: "absolute",
                  left: `${leaf.x0}%`,
                  top: `${leaf.y0}%`,
                  width: `${leafWidth}%`,
                  height: `${leafHeight}%`,
                  borderRadius: "6px",
                  padding: "6px",
                  boxSizing: "border-box",
                }}
                title={`${leaf.data.name}\n${d3.format(",d")(leaf.value!)}`}
              >
                {leafWidth > VISIBLE_TEXT_WIDTH && leafHeight > VISIBLE_TEXT_HEIGHT && (
                  <div className="text-base leading-5 truncate">{leaf.data.name}</div>
                )}
                {leafWidth > VISIBLE_TEXT_WIDTH && leafHeight > VISIBLE_TEXT_HEIGHT && (
                  <div className="text-lg leading-5">{leaf.value}</div>
                )}
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <div>{leaf.data.name}</div>
              <div className="text-gray-500 text-sm">{leaf.value}</div>
            </TooltipContent>
          </ClientTooltip>
        );
      })}
    </div>
  );
}
