import React from "react";
import * as d3 from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "../../helpers/client_tooltip/ClientTooltip";

/* Ported from rosencharts (MIT, Filsommer): treemap-charts/1_TreemapChart_DIV.tsx.
 * Render technique: absolutely-positioned <div> cells (the original "_DIV" variant).
 * Data is now a prop: list of { topic, subtopics: [{ <name>: <value>, ... }] }. */

type TreemapNode = { topic: string; subtopics: Record<string, number>[] };

const defaultData: TreemapNode[] = [
  { topic: "Tech", subtopics: [{ Windows: 100, MacOS: 120, Linux: 110 }] },
  { topic: "Financials", subtopics: [{ Loans: 60, Bonds: 80, PPRs: 20 }] },
  { topic: "Energy", subtopics: [{ Petrol: 70, Diesel: 50, Hydrogen: 20 }] },
];

const defaultColors = [
  "bg-violet-500 dark:bg-violet-500",
  "bg-pink-400 dark:bg-pink-400",
  "bg-orange-400 dark:bg-orange-400",
];

export function TreemapChart({
  data = defaultData,
  colors = defaultColors,
}: {
  data?: TreemapNode[];
  colors?: string[];
}) {
  if (data.length === 0) {
    return <div className="relative h-72 w-full" />;
  }

  // Transform the raw data into a hierarchical structure
  const hierarchyData = {
    name: "root",
    children: data.map((topic) => ({
      name: topic.topic,
      children: Object.entries(topic.subtopics[0]).map(([name, value]) => ({
        name,
        value,
      })),
    })),
  };

  // Create root node
  const root = d3
    .hierarchy(hierarchyData)
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
    .domain(data.map((d) => d.topic))
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
