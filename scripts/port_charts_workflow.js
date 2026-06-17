export const meta = {
  name: 'port-rosencharts-families',
  description: 'Port the remaining 42 rosencharts charts to Reflex, one agent per family (TDD)',
  phases: [
    { title: 'Port families', detail: 'one agent per family: TSX + wrapper + test + gallery' },
  ],
}

// Proven recipe (validated end-to-end with the line_chart pilot; compiles with `reflex export`).
const RECIPE = `
You are porting rosencharts D3/TSX charts to Reflex Python components, following a PROVEN recipe.

FIRST, read these files to understand the exact, working pattern (do not skip):
- CONTRIBUTING.md                                            (the proven recipe + asset layout rule)
- reflex_rosencharts/components/line/line_chart.py           (worked wrapper example)
- reflex_rosencharts/components/line/line_chart.tsx          (worked parametrized TSX example)
- reflex_rosencharts/components/line/gallery.py              (worked gallery entry example)
- reflex_rosencharts/components/line/__init__.py             (worked family __init__ example)
- reflex_rosencharts/gallery/registry.py                     (ChartEntry dataclass)
- specs/data-model/chart-data-schemas.md                     (data schemas)
- specs/api/component-api-v1.md                              (public API props)

KEY PROVEN FACTS (do not deviate):
- rx.asset("<name>.tsx", shared=True) is called from components/<family>/<name>.py and lands the TSX at
  external/reflex_rosencharts/components/<family>/<name>/<name>.tsx.
- If a chart's TSX imports the tooltip helper, the import MUST be exactly:
    import { ClientTooltip, TooltipTrigger, TooltipContent } from "../../helpers/client_tooltip/ClientTooltip";
  and the Python wrapper MUST call client_tooltip_asset() (imported from ..helpers.client_tooltip) before rx.asset(...),
  and the wrapper class MUST subclass rx.NoSSRComponent.
- If a chart does NOT use the tooltip, subclass rx.Component (not NoSSR) and skip client_tooltip_asset().
- If the TSX imports from "d3", set lib_dependencies: list[str] = ["d3"] on the wrapper class.
- The exported TSX function name MUST be a clean PascalCase tag (e.g. AreaChart, BarChartHorizontal); the
  Python wrapper's tag = "<ThatExactName>". Rename the original export (often "LiveN_Name") to the clean name.
- Parametrize: replace the hardcoded data array with a prop \`data\` whose default = the ORIGINAL example data
  (copy the original array verbatim as the default). Add color/colors props where the API spec lists them.
  Guard empty data: if (data.length === 0) return <div className="relative h-72 w-full" />;
- Names: snake_case Python function per chart; drop any "_DIV" suffix (it is a render technique, note it in the docstring).

TDD (MANDATORY, per chart):
1. Write/extend tests/test_<family>.py with, for each chart: a test that the function is exported from
   reflex_rosencharts, builds an rx.Component via fn(data=[...one sample row...]), and that fn() (no args)
   has non-empty default data. Run the test FIRST and see it FAIL.
2. Implement the TSX + wrapper to make it pass.
3. Run: \`.venv/bin/python -m pytest tests/test_<family>.py -v\` and confirm GREEN.

DELIVERABLES for your family (and ONLY your family's files):
- reflex_rosencharts/components/<family>/<name>.tsx  (one per chart, parametrized)
- reflex_rosencharts/components/<family>/<name>.py   (one per chart, wrapper + public function)
- reflex_rosencharts/components/<family>/__init__.py (import every function; set __all__ = [all function names])
- reflex_rosencharts/components/<family>/gallery.py  (GALLERY_ENTRIES: list[ChartEntry], one per chart, with a
  short Python usage snippet; render=lambda bound correctly — beware late-binding, use default-arg capture)
- tests/test_<family>.py

HARD CONSTRAINTS:
- DO NOT edit reflex_rosencharts/__init__.py (it aggregates families dynamically).
- DO NOT edit any other family's files, or the helpers, or rxconfig.py, or the demo app.
- DO NOT run \`reflex export\` or \`reflex run\` (serial build is done later by the orchestrator). Verify with pytest only.
- Run python/pytest via \`.venv/bin/python\` (the venv's reflex script shebang is stale; \`.venv/bin/python -m pytest ...\` works).
- Read each chart's reference TSX to get exact field names, tooltip usage, and extra props.

Return a concise summary: which charts you ported, the pytest result line, and any chart you could not fully port (with reason).
`;

const FAMILIES = {
  line: {
    note: 'line_chart is ALREADY DONE — DO NOT touch line_chart.py/.tsx. APPEND the 7 below to the existing __init__.py, gallery.py, and tests/test_line.py (preserve the existing line_chart entries).',
    charts: [
      ['line_chart_curved', 'reference/rosencharts/line-charts/2_LineChartCurved.tsx'],
      ['line_chart_multiple', 'reference/rosencharts/line-charts/3_LineChartMultiple.tsx'],
      ['line_chart_labels_curved', 'reference/rosencharts/line-charts/4_LineChartLabelsCurved.tsx'],
      ['line_chart_stocks_curved', 'reference/rosencharts/line-charts/5_LineChartStocksCurved.tsx'],
      ['line_chart_step', 'reference/rosencharts/line-charts/6_LineChartStep.tsx'],
      ['line_chart_pulse', 'reference/rosencharts/line-charts/7_LineChartPulse.tsx'],
      ['line_chart_full', 'reference/rosencharts/line-charts/8_LineChartFull.tsx'],
    ],
  },
  area: {
    note: 'New family. Same TimePoint schema as line ({date, value}).',
    charts: [
      ['area_chart', 'reference/rosencharts/area-charts/1_AreaChart.tsx'],
      ['area_chart_full', 'reference/rosencharts/area-charts/2_AreaChartFull.tsx'],
      ['area_chart_gradient', 'reference/rosencharts/area-charts/3_AreaChartGradient.tsx'],
      ['area_chart_semi_filled', 'reference/rosencharts/area-charts/4_AreaChartSemiFilled.tsx'],
    ],
  },
  bar: {
    note: 'New family. Base schema BarItem ({key, value}); some variants add fields (logo/flag URL, benchmark, line, stacked segments) — read each TSX and define a per-variant TypedDict. Several are DIV-based (no d3) — only add lib_dependencies=["d3"] if the TSX imports d3.',
    charts: [
      ['bar_chart_horizontal', 'reference/rosencharts/bar-charts/1_BarChartHorizontal_DIV.tsx'],
      ['bar_chart_horizontal_logo', 'reference/rosencharts/bar-charts/2_BarChartHorizontalLogo_DIV.tsx'],
      ['bar_chart_gradient', 'reference/rosencharts/bar-charts/3_BarChartGradient_DIV.tsx'],
      ['bar_chart_breakdown', 'reference/rosencharts/bar-charts/4_BarChartBreakdown.tsx'],
      ['bar_chart_thin_breakdown', 'reference/rosencharts/bar-charts/5_BarChartThinBreakdown.tsx'],
      ['bar_chart_thin_horizontal', 'reference/rosencharts/bar-charts/6_BarChartThinHorizontal_DIV.tsx'],
      ['bar_chart_flags_horizontal', 'reference/rosencharts/bar-charts/7_BarChartFlagsHorizontal.tsx'],
      ['bar_chart_vertical', 'reference/rosencharts/bar-charts/9_BarChartVertical_DIV.tsx'],
      ['bar_chart_multi_vertical', 'reference/rosencharts/bar-charts/11_BarChartMultiVertical_DIV.tsx'],
      ['bar_chart_triple_flags_horizontal', 'reference/rosencharts/bar-charts/12_BarChartTripleFlagsHorizontal_DIV.tsx'],
      ['bar_chart_line', 'reference/rosencharts/bar-charts/14_BarChartLine.tsx'],
      ['bar_chart_benchmark', 'reference/rosencharts/bar-charts/15_BarChartBenchmark.tsx'],
    ],
  },
  pie: {
    note: 'New family. Schema CategoryValue ({name, value}); palette via colors prop; donut_chart_center_text adds center_text prop; fillable variants take a value 0-100.',
    charts: [
      ['pie_chart', 'reference/rosencharts/pie-charts/1_PieChart.tsx'],
      ['pie_chart_stocks', 'reference/rosencharts/pie-charts/2_PieChartStocks.tsx'],
      ['pie_chart_labels', 'reference/rosencharts/pie-charts/3_PieChartLabels.tsx'],
      ['donut_chart', 'reference/rosencharts/pie-charts/4_DonutChart.tsx'],
      ['donut_chart_center_text', 'reference/rosencharts/pie-charts/5_DonutChartCenterText.tsx'],
      ['donut_chart_half', 'reference/rosencharts/pie-charts/6_DonutChartHalf.tsx'],
      ['donut_chart_fillable_half', 'reference/rosencharts/pie-charts/7_DonutChartFillableHalf.tsx'],
      ['donut_chart_fillable', 'reference/rosencharts/pie-charts/8_DonutChartFillable.tsx'],
    ],
  },
  scatter: {
    note: 'New family. Schema ScatterPoint ({revenue (x), value (y), company}). scatter_chart_interactive emits a click event: add on_point_click: rx.EventHandler[rx.event.passthrough_event_spec(dict)]. multiclass adds a class field for color.',
    charts: [
      ['scatter_chart', 'reference/rosencharts/scatter-charts/1_ScatterChart.tsx'],
      ['scatter_chart_interactive', 'reference/rosencharts/scatter-charts/2_ScatterChartInteractive.tsx'],
      ['scatter_chart_multiclass', 'reference/rosencharts/scatter-charts/5_ScatterChartMulticlass.tsx'],
      ['scatter_chart_stocks', 'reference/rosencharts/scatter-charts/6_ScatterChartStocks.tsx'],
    ],
  },
  treemap: {
    note: 'New family. Nested schema TreemapNode ({topic, subtopics: list[dict]}). DIV-based. images variant adds img URL per node.',
    charts: [
      ['treemap_chart', 'reference/rosencharts/treemap-charts/1_TreemapChart_DIV.tsx'],
      ['treemap_chart_images', 'reference/rosencharts/treemap-charts/2_TreemapChartImages_DIV.tsx'],
      ['treemap_chart_gradient', 'reference/rosencharts/treemap-charts/3_TreemapChartGradient_DIV.tsx'],
    ],
  },
  radar: {
    note: 'New family. Schema RadarPoint ({topic, value}).',
    charts: [
      ['radar_chart', 'reference/rosencharts/radar-charts/6_RadarChart.tsx'],
      ['radar_chart_rounded', 'reference/rosencharts/radar-charts/8_RadarChartRounded.tsx'],
    ],
  },
  other: {
    note: 'New family. bubble_chart = scatter with size (DIV-based). funnel_chart = ordered FunnelStage ({name, value}).',
    charts: [
      ['bubble_chart', 'reference/rosencharts/other-charts/4_BubbleChart_DIV.tsx'],
      ['funnel_chart', 'reference/rosencharts/other-charts/5_FunnelChart.tsx'],
    ],
  },
}

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['family', 'ported', 'pytest_result', 'failures'],
  properties: {
    family: { type: 'string' },
    ported: { type: 'array', items: { type: 'string' }, description: 'chart function names successfully ported + tested green' },
    pytest_result: { type: 'string', description: 'the final pytest summary line, e.g. "14 passed in 0.5s"' },
    failures: { type: 'array', items: { type: 'string' }, description: 'charts not fully ported, with reason' },
  },
}

phase('Port families')

const families = Object.entries(FAMILIES)
const results = await parallel(
  families.map(([family, spec]) => () => {
    const list = spec.charts.map(([name, ref]) => `  - ${name}  ←  ${ref}`).join('\n')
    const prompt = `${RECIPE}

========================================================================
YOUR FAMILY: "${family}"
NOTE: ${spec.note}

Charts to port (function_name ← reference TSX):
${list}

Work in: reflex_rosencharts/components/${family}/  and  tests/test_${family}.py
========================================================================`
    return agent(prompt, { label: `port:${family}`, phase: 'Port families', schema: SCHEMA })
  })
)

const ok = results.filter(Boolean)
log(`Families completed: ${ok.length}/${families.length}`)
return {
  families: ok,
  total_ported: ok.reduce((n, r) => n + (r.ported?.length || 0), 0),
}
