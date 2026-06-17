import { pie, arc, PieArcDatum } from "d3";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "../../helpers/client_tooltip/ClientTooltip";

/* Ported from rosencharts (MIT, Filsommer). Data and palette are now props. */

type DataItem = { name: string; value: number };

const defaultData: DataItem[] = [
  { name: "Rent", value: 731 },
  { name: "Food", value: 631 },
  { name: "Household", value: 331 },
  { name: "Transportation", value: 232 },
  { name: "Entertainment", value: 101 },
  { name: "Other", value: 42 },
];

const defaultColors = ["#F5A5DB", "#B89DFB", "#758bcf", "#33C2EA", "#FFC182", "#73DC5A"];

export function PieChart({
  data = defaultData,
  colors = defaultColors,
}: {
  data?: DataItem[];
  colors?: string[];
}) {
  if (data.length === 0) return <div className="relative h-72 w-full" />;

  const radius = Math.PI * 100;
  const gap = 0.02;

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

  const computeAngle = (d: PieArcDatum<DataItem>) => {
    return ((d.endAngle - d.startAngle) * 180) / Math.PI;
  };

  const minAngle = 20;

  return (
    <div className="overflow-visible">
      <div className="relative max-w-[16rem] mx-auto">
        <svg viewBox={`-${radius} -${radius} ${radius * 2} ${radius * 2}`}>
          {arcs.map((d: PieArcDatum<DataItem>, i) => (
            <ClientTooltip key={i}>
              <TooltipTrigger>
                <path key={i} fill={colors[i % colors.length]} d={arcGenerator(d)!} />
              </TooltipTrigger>
              <TooltipContent>
                <div>{d.data.name}</div>
              </TooltipContent>
            </ClientTooltip>
          ))}
        </svg>
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
