import React from "react";
import * as d3 from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

// Default dataset = the original rosencharts example, preserved as the nested
// hierarchy ({ name: "root", children: [...] }) that feeds d3.hierarchy.
const DEFAULT_DATA = {
  name: "root",
  children: [
    {
      name: "Tech",
      children: [
        { name: "Windows", value: 100 },
        { name: "MacOS", value: 120 },
        { name: "Linux", value: 110 },
      ],
    },
    {
      name: "Financials",
      children: [
        { name: "Loans", value: 60 },
        { name: "Bonds", value: 80 },
        { name: "PPRs", value: 20 },
      ],
    },
    {
      name: "Energy",
      children: [
        { name: "Petrol", value: 70 },
        { name: "Diesel", value: 50 },
        { name: "Hydrogen", value: 20 },
      ],
    },
  ],
};

const colors = [
  "bg-violet-500 dark:bg-violet-500",
  "bg-pink-400 dark:bg-pink-400",
  "bg-orange-400 dark:bg-orange-400",
];

export function TreemapChart({ data = DEFAULT_DATA }: { data?: any }) {
  if (!data || !data.children || data.children.length === 0) {
    return <div className="relative w-full h-[250px]" />;
  }

  // Create root node
  const root = d3
    .hierarchy(data)
    .sum((d: any) => d.value)
    .sort((a: any, b: any) => (b.value ?? 0) - (a.value ?? 0));

  // Compute the treemap layout
  d3
    .treemap()
    .size([100, 100])
    .paddingInner(0.75) // Padding between subtopics
    .paddingOuter(1) // Padding between topics
    .round(false)(root as d3.HierarchyNode<unknown>);

  // Color scale
  const color = d3
    .scaleOrdinal()
    .domain(data.children.map((d: any) => d.name))
    .range(colors);

  return (
    <div className="relative w-full h-[250px]">
      {root.leaves().map((leaf: any, i) => {
        const leafWidth = leaf.x1 - leaf.x0;
        const leafHeight = leaf.y1 - leaf.y0;
        const VISIBLE_TEXT_WIDTH = 15;
        const VISIBLE_TEXT_HEIGHT = 15;
        return (
          <ClientTooltip key={i}>
            <TooltipTrigger>
              <div
                key={i}
                className={color(leaf.parent.data.name) as string}
                style={{
                  position: "absolute",
                  left: `${leaf.x0}%`,
                  top: `${leaf.y0}%`,
                  width: `${leafWidth}%`,
                  height: `${leafHeight}%`,
                  borderRadius: "6px",
                  border: "1px solid #ffffff44",
                  color: "white",
                  padding: "6px",
                  boxSizing: "border-box",
                }}
                title={`${leaf.data.name}\n${d3.format(",d")(leaf.value)}`}
              >
                {leafWidth > VISIBLE_TEXT_WIDTH && leafHeight > VISIBLE_TEXT_HEIGHT && (
                  <div className="text-base leading-5 truncate">{leaf.data.name}</div>
                )}
                {leafWidth > VISIBLE_TEXT_WIDTH && leafHeight > VISIBLE_TEXT_HEIGHT && (
                  <div className="text-gray-100 text-sm leading-5">{leaf.value}</div>
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
