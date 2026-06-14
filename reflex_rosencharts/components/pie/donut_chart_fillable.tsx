import { pie, arc, PieArcDatum } from "d3";

/* Ported from rosencharts (MIT, Filsommer). Fill value (0-100) is now a prop. No tooltip. */

type Item = { name: string; value: number };

export function DonutChartFillable({
  value = 31,
  label = "Filled",
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
    .startAngle(0)
    .endAngle(2 * Math.PI)
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
    purple: "fill-violet-600 dark:fill-violet-500",
    gray: "fill-[#e0e0e0] dark:fill-zinc-700",
  };

  return (
    <div className="relative">
      <svg
        viewBox={`-${radius} -${radius} ${radius * 2} ${radius * 2}`}
        className="max-w-[16rem] mx-auto overflow-visible"
      >
        <defs>
          {arcs.map((d, i) => (
            <clipPath key={`fillable-donut-clip-${i}`} id={`fillable-donut-clip-${i}`}>
              <path d={arcClip(d) || undefined} />
            </clipPath>
          ))}
        </defs>
        <g>
          {arcs.map((d, i) => (
            <g key={i} clipPath={`url(#fillable-donut-clip-${i})`}>
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
      </svg>
      {/* Centered value display */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-lg font-semibold leading-5">{label}</span>
        <div className="text-xl font-bold">
          <span className="text-violet-600 dark:text-violet-400">{filled}</span>
          <span className="text-zinc-400 dark:text-zinc-600"> / 100</span>
        </div>
      </div>
    </div>
  );
}
