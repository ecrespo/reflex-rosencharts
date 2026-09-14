/**
 * Axis regression check for the scatter charts (0.2.2).
 *
 * Server-renders every scatter/line chart touched by the axis rewrite with the
 * clustered, unsorted, extreme-valued data that used to break them, and asserts
 * the properties the axes are supposed to guarantee: regular tick labels that
 * line up with the grid, nothing clipped at the edges, a y reference at or
 * beyond the extremes, a gutter that fits its labels, and a chart that does not
 * depend on the order the data arrives in.
 *
 * Usage:  node scripts/check_scatter_axes.mjs
 * Needs the frontend dependencies Reflex installs on the first `reflex run`
 * (.web/node_modules). Exits non-zero on the first failed assertion.
 */
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const WEB = join(ROOT, ".web", "node_modules");
const COMPONENTS = join(ROOT, "custom_components", "reflex_rosencharts", "components");

if (!existsSync(WEB)) {
  console.error("Missing .web/node_modules — run `reflex run` once so Reflex installs the frontend deps.");
  process.exit(2);
}

const REPOS = [
  { company: "omagnome", revenue: 1, value: 53 },
  { company: "reflex-mapcn", revenue: 1, value: 38 },
  { company: "mcp-joke-server", revenue: 1, value: 34 },
  { company: "fastapi_todos", revenue: 16, value: 43 },
  { company: "vigia-eew", revenue: 19, value: 46 },
  { company: "quiz", revenue: 28, value: 47 },
  { company: "prismal", revenue: 143, value: 440 },
  { company: "python-android_sms", revenue: 229, value: 138 },
  { company: "ecrespo-localpaquetes", revenue: 273, value: 46 },
  { company: "reflex_resume", revenue: 287, value: 50 },
  { company: "python-autoaccesibilidad", revenue: 403, value: 49 },
  { company: "tutorial_fastAPI", revenue: 1409, value: 45 },
  { company: "pysms-send", revenue: 2345, value: 29 },
];
const OUTLIER = { company: "ecrespo.github.io", revenue: 2609, value: 1451 };

const work = mkdtempSync(join(tmpdir(), "rosencharts-axes-"));
const entry = join(work, "entry.tsx");
const bundle = join(work, "out.cjs");

writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { ScatterChart } from ${JSON.stringify(join(COMPONENTS, "scatter/scatter_chart.tsx"))};
import { ScatterChartInteractive } from ${JSON.stringify(join(COMPONENTS, "scatter/scatter_chart_interactive.tsx"))};
import { ScatterChartMulticlass } from ${JSON.stringify(join(COMPONENTS, "scatter/scatter_chart_multiclass.tsx"))};
import { ScatterChartStocks } from ${JSON.stringify(join(COMPONENTS, "scatter/scatter_chart_stocks.tsx"))};
import { LineChart } from ${JSON.stringify(join(COMPONENTS, "line/line_chart.tsx"))};

const REPOS = ${JSON.stringify(REPOS)};
const SHUFFLED = ${JSON.stringify([...REPOS].reverse())};
const BIG = ${JSON.stringify([...REPOS, OUTLIER])};

const cases = {
  scatter_default: <ScatterChart />,
  scatter_repos: <ScatterChart data={REPOS} />,
  scatter_shuffled: <ScatterChart data={SHUFFLED} />,
  scatter_outlier: <ScatterChart data={BIG} />,
  scatter_log: <ScatterChart data={REPOS} xScale="log" />,
  scatter_log_narrow: <ScatterChart data={[40, 45, 50, 55, 60].map((v, i) => ({ company: "n" + i, revenue: i + 1, value: v }))} yScale="log" />,
  scatter_log_wide_decade: <ScatterChart data={[200, 400, 900].map((v, i) => ({ company: "w" + i, revenue: i + 1, value: v }))} yScale="log" />,
  scatter_symlog: <ScatterChart data={[-1e6, 0, 1e6].map((v, i) => ({ company: "s" + i, revenue: i + 1, value: v }))} yScale="symlog" />,
  scatter_margin: <ScatterChart data={REPOS} marginLeft="60px" />,
  scatter_empty: <ScatterChart data={[]} />,
  scatter_single: <ScatterChart data={[{ company: "solo", revenue: 42, value: 7 }]} />,
  interactive: <ScatterChartInteractive data={REPOS} />,
  multiclass: <ScatterChartMulticlass data={REPOS.map((d, i) => ({ ...d, category: i % 2 ? "A" : "B" }))} />,
  stocks: <ScatterChartStocks data={REPOS} />,
  line_big: <LineChart data={[{ date: "2023-05-01", value: 1200 }, { date: "2023-05-02", value: 400 }]} />,
  line_margin: <LineChart data={[{ date: "2023-05-01", value: 1200 }]} marginLeft={70} />,
};

const out = {};
for (const [name, element] of Object.entries(cases)) {
  try { out[name] = renderToStaticMarkup(element); }
  catch (error) { out[name] = "ERROR: " + (error && error.message ? error.message : String(error)); }
}
console.log(JSON.stringify(out));
`);

const esbuild = await import(join(WEB, "esbuild", "lib", "main.js"));
await (esbuild.default ?? esbuild).build({
  entryPoints: [entry],
  bundle: true,
  outfile: bundle,
  format: "cjs",
  platform: "node",
  target: "node20",
  jsx: "automatic",
  logLevel: "warning",
  nodePaths: [WEB],
  define: { "process.env.NODE_ENV": '"production"' },
  plugins: [{
    name: "reflex-public-alias",
    setup(build) {
      // "$/public/external/reflex_rosencharts/components/<family>/<module>/<File>.tsx"
      // is the symlink Reflex creates for "<family>/<File>.tsx" in the source tree.
      build.onResolve({ filter: /^\$\/public\/external\/reflex_rosencharts\/components\// }, (args) => {
        const parts = args.path.split("/components/")[1].split("/");
        const file = parts.pop();
        parts.pop();
        return { path: join(COMPONENTS, ...parts, file) };
      });
      // Resolve every bare package (react, d3, ...) from .web/node_modules only.
      // Otherwise esbuild walks up from the source tree and may pick a stray
      // node_modules in a parent directory, bundling two copies of React.
      build.onResolve({ filter: /^[^./$]/ }, (args) => {
        if (args.pluginData?.fromWeb) return undefined;
        return build.resolve(args.path, { kind: args.kind, resolveDir: WEB, pluginData: { fromWeb: true } });
      });
    },
  }],
});

const rendered = JSON.parse(execFileSync(process.execPath, [bundle], { encoding: "utf8", maxBuffer: 32 << 20 }));
rmSync(work, { recursive: true, force: true });

let failures = 0;
const check = (name, ok, detail = "") => {
  if (!ok) failures++;
  console.log(`${ok ? "  PASS" : "  FAIL"}  ${name}${detail ? "  -> " + detail : ""}`);
};
const xLabels = (html) => [...html.matchAll(/class="text-xs tabular-nums absolute"[^>]*>([^<]*)</g)].map((m) => m[1]);
const yLabels = (html) => [...html.matchAll(/class="absolute text-xs tabular-nums[^"]*"[^>]*>([^<]*)</g)].map((m) => m[1]);
const marks = (html) => [...html.matchAll(/d="M ([-\d.e]+) ([-\d.e]+) l 0\.0001 0"/g)].map((m) => [+m[1], +m[2]]);
// `scatter_chart_stocks` places its logos as absolutely positioned divs.
const divMarks = (html) => [...html.matchAll(/top:([-\d.e]+)%;left:([-\d.e]+)%;transform:translate\(-50%, -50%\)/g)].map((m) => [+m[2], +m[1]]);
const gutter = (html) => (html.match(/--marginLeft:([^;"]+)/) || [])[1];
const gridX = (html) => [...html.matchAll(/transform="translate\(([-\d.e]+),0\)"/g)].map((m) => +m[1]);
const gridY = (html) => [...html.matchAll(/transform="translate\(0,([-\d.e]+)\)"/g)].map((m) => +m[1]);
const labelX = (html) => [...html.matchAll(/left:([-\d.e]+)%;top:100%/g)].map((m) => +m[1]);
const labelY = (html) => [...html.matchAll(/top:([-\d.e]+)%;left:0%/g)].map((m) => +m[1]);

for (const [name, html] of Object.entries(rendered)) {
  const ok = !html.startsWith("ERROR") && !html.includes("NaN");
  check(`${name} renders`, ok, ok ? "" : html.slice(0, 200));
}

const repos = rendered.scatter_repos;
const xs = xLabels(repos).map(Number);
const steps = xs.slice(1).map((v, i) => v - xs[i]);
check("x labels are regular ticks", steps.length > 2 && steps.every((s) => Math.abs(s - steps[0]) < 1e-9), xLabels(repos).join(" | "));
check("x grid lines match the x labels", JSON.stringify(gridX(repos)) === JSON.stringify(labelX(repos)));
check("y grid lines match the y labels", JSON.stringify(gridY(repos)) === JSON.stringify(labelY(repos)));

const ys = yLabels(repos).map(Number);
check("a y tick at or above the maximum", Math.max(...ys) >= Math.max(...REPOS.map((d) => d.value)), yLabels(repos).join(" | "));
check("a y tick at or below the minimum", Math.min(...ys) <= Math.min(...REPOS.map((d) => d.value)));

check("shuffling changes nothing", JSON.stringify(xLabels(rendered.scatter_shuffled)) === JSON.stringify(xLabels(repos))
  && JSON.stringify(marks(rendered.scatter_shuffled).sort()) === JSON.stringify(marks(repos).sort()));

for (const name of ["scatter_default", "scatter_repos", "scatter_outlier", "scatter_single", "interactive", "multiclass", "stocks"]) {
  const points = name === "stocks" ? divMarks(rendered[name]) : marks(rendered[name]);
  const tightest = Math.min(...points.map(([x, y]) => Math.min(x, 100 - x, y, 100 - y)));
  check(`${name}: no mark clipped at the edges`, points.length > 0 && tightest >= 3.9, `tightest ${tightest.toFixed(2)}%`);
}

const widths = [...repos.matchAll(/width="([-\d.e]+)" height="100"/g)].map((m) => +m[1]);
check("no tooltip band with a negative width", widths.length > 0 && widths.every((w) => w >= 0));
check("every point carries its own dot trigger", (repos.match(/stroke-width="18"/g) || []).length === REPOS.length);

check("gutter fits 3-digit labels", gutter(repos) === "36px", gutter(repos));
check("gutter grows for 4-digit labels", gutter(rendered.scatter_outlier) === "44px", gutter(rendered.scatter_outlier));
check("margin_left overrides it (scatter)", gutter(rendered.scatter_margin) === "60px");
check("margin_left overrides it (line)", gutter(rendered.line_margin) === "70px");
check("line gutter fits a 4-digit label", gutter(rendered.line_big) === "44px", gutter(rendered.line_big));
for (const [name, html] of Object.entries(rendered)) {
  const classes = [...html.matchAll(/class="(absolute text-xs tabular-nums[^"]*)"/g)].map((m) => m[1]);
  if (classes.length) check(`${name}: y labels never wrap`, classes.every((c) => c.includes("whitespace-nowrap")));
}
check("empty data renders an empty container", rendered.scatter_empty === '<div class="relative h-72 w-full"></div>');
const numbers = (labels) => labels.map((l) => Number(l.replace(/,/g, "")));
check("narrow log y axis keeps several labels", yLabels(rendered.scatter_log_narrow).length >= 3, yLabels(rendered.scatter_log_narrow).join(" | "));
check("narrow log y axis labels its maximum", Math.max(...numbers(yLabels(rendered.scatter_log_wide_decade))) >= 900, yLabels(rendered.scatter_log_wide_decade).join(" | "));
check("symlog y axis labels its extremes", Math.max(...numbers(yLabels(rendered.scatter_symlog))) >= 1e6 && Math.min(...numbers(yLabels(rendered.scatter_symlog))) <= -1e6, yLabels(rendered.scatter_symlog).join(" | "));
check("log scale is labelled", xLabels(rendered.scatter_log).filter(Boolean).length >= 3, xLabels(rendered.scatter_log).join(" | "));

console.log(`\n${failures === 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED"}`);
process.exit(failures === 0 ? 0 : 1);
