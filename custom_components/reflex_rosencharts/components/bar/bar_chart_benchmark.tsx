import React from "react";
import { ClientTooltip, TooltipContent, TooltipTrigger } from "$/public/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx";

type Item = { key: string; value: number };

// Default dataset = the original rosencharts example.
const DEFAULT_DATA: Item[] = [
  { key: "Model 0", value: 85.8 },
  { key: "Model A", value: 34.3 },
  { key: "Model B", value: 27.1 },
  { key: "Model C", value: 22.5 },
];

export function BarChartBenchmark({ data = DEFAULT_DATA }: { data?: Item[] }) {
  if (!data || data.length === 0) {
    return <div className="w-full h-full grid gap-4 py-4" />;
  }
  const maxValue = Math.max(...data.map((d) => d.value));
  return (
    <div className="w-full h-full grid gap-4 py-4">
      {/* Bars */}
      {data.map((d, index) => {
        return (
          <ClientTooltip key={index}>
            <TooltipTrigger>
              <>
                <div
                  className={`text-sm whitespace-nowrap ${
                    index === 0
                      ? "bg-pink-500 dark:bg-[#00F2FF] text-transparent bg-clip-text"
                      : "text-gray-500 dark:text-zinc-400"
                  }`}
                >
                  {d.key}
                </div>
                <div className="flex items-center gap-2.5">
                  <div
                    key={index}
                    className="relative rounded-sm h-3 bg-gray-200 dark:bg-zinc-800 overflow-hidden w-full"
                  >
                    <div
                      className={`absolute inset-0 rounded-r-sm bg-gradient-to-r ${
                        index === 0
                          ? "from-pink-300 to-purple-300 dark:from-[#00F2FF] dark:to-[#7AED5C]"
                          : "from-zinc-400 to-gray-400 dark:from-zinc-500 dark:to-zinc-400"
                      }`}
                      style={{
                        width: `${(d.value / maxValue) * 100}%`,
                      }}
                    />
                  </div>
                  <div
                    className={`text-sm whitespace-nowrap ${
                      index === 0
                        ? "bg-purple-400 dark:bg-[#7AED5C] text-transparent bg-clip-text"
                        : "text-gray-500 dark:text-zinc-400"
                    } tabular-nums`}
                  >
                    {d.value}
                  </div>
                </div>
              </>
            </TooltipTrigger>
            <TooltipContent>
              <div>{d.key}</div>
              <div className="text-gray-500 dark:text-zinc-400 text-sm">{d.value}</div>
            </TooltipContent>
          </ClientTooltip>
        );
      })}
    </div>
  );
}
