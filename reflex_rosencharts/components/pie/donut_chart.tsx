import { pie, arc, PieArcDatum } from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "../../helpers/client_tooltip/ClientTooltip";

/* Ported from rosencharts (MIT, Filsommer). Data and palette are now props. */

type Item = { name: string; value: number };

const defaultData: Item[] = [
  { name: "AAPL", value: 30 },
  { name: "BTC", value: 22 },
  { name: "GOLD", value: 11 },
  { name: "PLTR", value: 9 },
  { name: "ADA", value: 7 },
  { name: "MSFT", value: 3 },
];

const defaultColors = ["#7e4cfe", "#895cfc", "#956bff", "#a37fff", "#b291fd", "#b597ff"];

export function DonutChart({
  data = defaultData,
  colors = defaultColors,
}: {
  data?: Item[];
  colors?: string[];
}) {
  if (data.length === 0) return <div className="relative h-72 w-full" />;

  const radius = 420;
  const gap = 0.01;
  const lightStrokeEffect = 10;

  const pieLayout = pie<Item>()
    .value((d) => d.value)
    .padAngle(gap);

  const innerRadius = radius / 1.625;
  const arcGenerator = arc<PieArcDatum<Item>>()
    .innerRadius(innerRadius)
    .outerRadius(radius)
    .cornerRadius(lightStrokeEffect + 2);

  const arcClip =
    arc<PieArcDatum<Item>>()
      .innerRadius(innerRadius + lightStrokeEffect / 2)
      .outerRadius(radius)
      .cornerRadius(lightStrokeEffect + 2) || undefined;

  const labelRadius = radius * 0.825;
  const arcLabel = arc<PieArcDatum<Item>>().innerRadius(labelRadius).outerRadius(labelRadius);

  const arcs = pieLayout(data);

  function computeAngle(d: PieArcDatum<Item>) {
    return ((d.endAngle - d.startAngle) * 180) / Math.PI;
  }

  const minAngle = 20;

  return (
    <div className="relative">
      <svg
        viewBox={`-${radius} -${radius} ${radius * 2} ${radius * 2}`}
        className="max-w-[16rem] mx-auto overflow-visible"
      >
        <defs>
          {arcs.map((d, i) => (
            <clipPath key={`donut-c0-clip-${i}`} id={`donut-c0-clip-${i}`}>
              <path d={arcClip(d) || undefined} />
              <linearGradient key={i} id={`donut-c0-gradient-${i}`}>
                <stop offset="55%" stopColor={colors[i % colors.length]} stopOpacity={0.95} />
              </linearGradient>
            </clipPath>
          ))}
        </defs>

        {arcs.map((d, i) => {
          const angle = computeAngle(d);
          let centroid = arcLabel.centroid(d);
          if (d.endAngle > Math.PI) {
            centroid[0] += 10;
            centroid[1] += 10;
          } else {
            centroid[0] -= 10;
            centroid[1] -= 0;
          }
          return (
            <ClientTooltip key={i}>
              <TooltipTrigger>
                <g key={i}>
                  <g clipPath={`url(#donut-c0-clip-${i})`}>
                    <path
                      fill={`url(#donut-c0-gradient-${i})`}
                      stroke="#ffffff33"
                      strokeWidth={lightStrokeEffect}
                      d={arcGenerator(d) || undefined}
                    />
                  </g>
                  <g opacity={angle > minAngle ? 1 : 0}>
                    <text transform={`translate(${centroid})`} textAnchor="middle" fontSize={38}>
                      <tspan y="-0.4em" fontWeight="600" fill={"#eee"}>
                        {d.data.name}
                      </tspan>
                      {angle > minAngle && (
                        <tspan x={0} y="0.7em" fillOpacity={0.7} fill={"#eee"}>
                          {d.data.value.toLocaleString("en-US")}%
                        </tspan>
                      )}
                    </text>
                  </g>
                </g>
              </TooltipTrigger>
              <TooltipContent>
                <div>{d.data.name}</div>
                <div className="text-gray-500 text-sm">{d.data.value.toLocaleString("en-US")}</div>
              </TooltipContent>
            </ClientTooltip>
          );
        })}
      </svg>
    </div>
  );
}
