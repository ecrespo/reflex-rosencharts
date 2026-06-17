import { pie, arc, PieArcDatum } from "d3";

/* Ported from rosencharts (MIT, Filsommer). Fill value (0-100) is now a prop. No tooltip. */

type Item = { name: string; value: number };

export function DonutChartFillableHalf({
  value = 31,
  label = "Goal",
}: {
  value?: number;
  label?: string;
}) {
  const radius = 420;
  const lightStrokeEffect = 10;

  const filled = Math.max(0, Math.min(100, value));
  const data: Item[] = [
    { name: "Filled", value: filled },
    { name: "Empty", value: 100 - filled },
  ];

  const pieLayout = pie<Item>()
    .value((d) => d.value)
    .startAngle(-Math.PI / 2)
    .endAngle(Math.PI / 2)
    .sort((a, b) => a.value - b.value)
    .padAngle(0.0);

  const innerRadius = radius / 1.625;
  const arcGenerator = arc<PieArcDatum<Item>>().innerRadius(innerRadius).outerRadius(radius);

  const arcClip =
    arc<PieArcDatum<Item>>()
      .innerRadius(innerRadius + lightStrokeEffect / 2)
      .outerRadius(radius)
      .cornerRadius(lightStrokeEffect + 2) || undefined;

  const arcs = pieLayout(data);

  const colors = {
    gray: "fill-[#e0e0e0] dark:fill-zinc-700",
    purple: "fill-violet-600 dark:fill-violet-500",
  };

  return (
    <div className="relative">
      <svg
        viewBox={`-${radius} -${radius} ${radius * 2} ${radius}`}
        className="max-w-[16rem] mx-auto overflow-visible"
      >
        <defs>
          {arcs.map((d, i) => (
            <clipPath key={`fillable-half-donut-clip-${i}`} id={`fillable-half-donut-clip-${i}`}>
              <path d={arcClip(d) || undefined} />
            </clipPath>
          ))}
        </defs>
        <g>
          {arcs.map((d, i) => (
            <g key={i} clipPath={`url(#fillable-half-donut-clip-${i})`}>
              <path
                className={`stroke-white/30 dark:stroke-zinc-400/10 ${
                  i === 1 ? colors.gray : colors.purple
                }`}
                strokeWidth={lightStrokeEffect}
                d={arcGenerator(d) || undefined}
              />
            </g>
          ))}
        </g>
        <text
          transform={`translate(0, ${-radius / 4})`}
          textAnchor="middle"
          fontSize={48}
          fontWeight="bold"
          fill="currentColor"
          className="text-zinc-700 dark:text-zinc-100"
        >
          {label}
        </text>{" "}
        <text
          transform={`translate(0, ${-radius / 12})`}
          textAnchor="middle"
          fontSize={64}
          fontWeight="bold"
          fill="currentColor"
          className="text-zinc-800 dark:text-zinc-300"
        >
          {filled}%
        </text>
      </svg>
    </div>
  );
}
