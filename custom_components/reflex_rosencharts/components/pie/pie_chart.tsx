import React from "react";
import { pie, arc, PieArcDatum } from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

type DataItem = {
  name: string;
  value: number;
};

// Default dataset = the original rosencharts example.
const DEFAULT_DATA: DataItem[] = [
  { name: "Rent", value: 731 },
  { name: "Food", value: 631 },
  { name: "Household", value: 331 },
  { name: "Transportation", value: 232 },
  { name: "Entertainment", value: 101 },
  { name: "Other", value: 42 },
];

// Slice colors, cycled so any number of data points renders.
const COLORS = ["#F5A5DB", "#B89DFB", "#758bcf", "#33C2EA", "#FFC182", "#73DC5A", "#2999F5", "#EC8E7B"];

export function PieChart({ data = DEFAULT_DATA }: { data?: DataItem[] }) {
  if (!data || data.length === 0) {
    return <div className="overflow-visible" />;
  }

  // Chart dimensions
  const radius = Math.PI * 100;
  const gap = 0.02; // Gap between slices

  // Pie layout and arc generator
  const pieLayout = pie<DataItem>()
    .value((d) => d.value)
    .padAngle(gap);

  const arcGenerator = arc<PieArcDatum<DataItem>>()
    .innerRadius(20)
    .outerRadius(radius)
    .cornerRadius(8);

  const labelRadius = radius * 0.8;
  const arcLabel = arc<PieArcDatum<DataItem>>().innerRadius(labelRadius).outerRadius(labelRadius);

  const arcs = pieLayout(data);

  // Calculate the angle for each slice
  const computeAngle = (d: PieArcDatum<DataItem>) => {
    return ((d.endAngle - d.startAngle) * 180) / Math.PI;
  };

  // Minimum angle to display text
  const minAngle = 20;

  return (
    <div className="overflow-visible">
      <div className="relative max-w-[16rem] mx-auto">
        <svg viewBox={`-${radius} -${radius} ${radius * 2} ${radius * 2}`}>
          {/* Sectors */}
          {arcs.map((d: PieArcDatum<DataItem>, i) => (
            <ClientTooltip key={i}>
              <TooltipTrigger>
                <path key={i} fill={COLORS[i % COLORS.length]} d={arcGenerator(d)!} />
              </TooltipTrigger>
              <TooltipContent>
                <div className="flex gap-2.5 items-center">
                  <div
                    className="w-1 h-8 rounded-full"
                    style={{ backgroundColor: COLORS[i % COLORS.length] }}
                  ></div>
                  <div>
                    <div>{d.data.name}</div>
                    <div className="text-gray-500 text-sm/5">{d.data.value.toLocaleString("en-US")}</div>
                  </div>
                </div>
              </TooltipContent>
            </ClientTooltip>
          ))}
        </svg>
        {/* Labels as absolutely positioned divs */}
        {arcs.map((d: PieArcDatum<DataItem>, i) => {
          const angle = computeAngle(d);
          if (angle <= minAngle) return null;

          let centroid = arcLabel.centroid(d);
          const leftLogo = `${50 + (centroid[0] / radius) * 40}%`;
          const topLogo = `${50 + (centroid[1] / radius) * 40}%`;

          return (
            <div key={i}>
              <div
                className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-none size-10 text-white text-md font-extrabold"
                style={{ left: leftLogo, top: topLogo }}
              >
                {d.data.value}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
