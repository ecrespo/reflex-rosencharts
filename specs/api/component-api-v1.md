# reflex-rosencharts — API Specification (Public Python API)

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **API Version** | v1.0 |
| **Date** | 2026-06-14 |
| **Related PRD** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **Package** | `reflex_rosencharts` (suggested alias `rxc`) |

---

> **SDD adaptation note:** This is not an HTTP API. The "contract" of this library is its
> **public Python API**: the component functions, their props, types, and event handlers.
> The auth/rate-limit/webhooks sections from the original template do not apply and are omitted.

## 1. Overview

The library exposes one function per chart that returns an `rx.Component`. The consumer imports the
package and composes the charts in their Reflex pages, feeding them with data from `rx.State`.

```python
import reflex as rx
import reflex_rosencharts as rxc

class State(rx.State):
    sales: list[dict] = [{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

def index() -> rx.Component:
    return rxc.line_chart(data=State.sales, height="18rem")
```

## 2. API Conventions

### 2.1 Naming
- One public function per chart, in `snake_case`, derived from the original name:
  `1_LineChart.tsx` → `line_chart`, `5_DonutChartCenterText.tsx` → `donut_chart_center_text`.
- Re-exported from `reflex_rosencharts/__init__.py`.
- "_DIV" variants (based on `<div>` instead of SVG) keep the semantic name without the
  `_DIV` suffix (e.g. `bar_chart_horizontal`), documenting the render technique internally.

### 2.2 Common props (all charts)

| Prop | Type | Default | Description |
|---|---|---|---|
| `data` | `rx.Var[list[dict]]` | `[]` | Series dataset. Schema depends on the type (see Data Model). |
| `height` | `rx.Var[str]` | `"18rem"` (`h-72`) | Container height (CSS). |
| `width` | `rx.Var[str]` | `"100%"` | Container width. |
| `class_name` | `rx.Var[str]` | `""` | Extra Tailwind classes for the root container. |

### 2.3 Color / palette props (where applicable)

| Prop | Type | Default | Description |
|---|---|---|---|
| `color` | `rx.Var[str]` | original class | Primary color (Tailwind class or CSS value). |
| `colors` | `rx.Var[list[str]]` | original palette | Palette for multiple series (pie, multiline, multibar, scatter multiclass). |
| `gradient` | `rx.Var[bool]` | depends on variant | Enables gradient fill (gradient variants). |

### 2.4 Event Handlers (interactive charts)

| Handler | Spec | Charts |
|---|---|---|
| `on_point_hover` | `rx.EventHandler[rx.event.passthrough_event_spec(dict)]` | The 29 with `ClientTooltip` |
| `on_point_click` | `rx.EventHandler[rx.event.passthrough_event_spec(dict)]` | `scatter_chart_interactive`, charts with selection |

### 2.5 Data typing
- The schema of each chart is defined with `TypedDict` (direct interop with the JS structure) or
  `rx.PropsBase` when automatic conversion to camelCase is required. Details in the Data Model.
- Type errors are detected at Reflex compile time (not at HTTP runtime).

## 3. Component catalog (43)

Default status: `☐ Pending` (updated as each one is ported).

### 3.1 Area (`reflex_rosencharts.components.area`)

| Function | Source | Data | Tooltip | Status |
|---|---|---|---|---|
| `area_chart` | area-charts/1_AreaChart.tsx | time series | yes | ☐ |
| `area_chart_full` | area-charts/2_AreaChartFull.tsx | time series | yes | ☐ |
| `area_chart_gradient` | area-charts/3_AreaChartGradient.tsx | time series | yes | ☐ |
| `area_chart_semi_filled` | area-charts/4_AreaChartSemiFilled.tsx | time series | yes | ☐ |

### 3.2 Bar (`reflex_rosencharts.components.bar`)

| Function | Source | Technique | Status |
|---|---|---|---|
| `bar_chart_horizontal` | bar-charts/1_BarChartHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_horizontal_logo` | bar-charts/2_BarChartHorizontalLogo_DIV.tsx | DIV | ☐ |
| `bar_chart_gradient` | bar-charts/3_BarChartGradient_DIV.tsx | DIV | ☐ |
| `bar_chart_breakdown` | bar-charts/4_BarChartBreakdown.tsx | SVG | ☐ |
| `bar_chart_thin_breakdown` | bar-charts/5_BarChartThinBreakdown.tsx | SVG | ☐ |
| `bar_chart_thin_horizontal` | bar-charts/6_BarChartThinHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_flags_horizontal` | bar-charts/7_BarChartFlagsHorizontal.tsx | SVG | ☐ |
| `bar_chart_vertical` | bar-charts/9_BarChartVertical_DIV.tsx | DIV | ☐ |
| `bar_chart_multi_vertical` | bar-charts/11_BarChartMultiVertical_DIV.tsx | DIV | ☐ |
| `bar_chart_triple_flags_horizontal` | bar-charts/12_BarChartTripleFlagsHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_line` | bar-charts/14_BarChartLine.tsx | SVG | ☐ |
| `bar_chart_benchmark` | bar-charts/15_BarChartBenchmark.tsx | SVG | ☐ |

### 3.3 Line (`reflex_rosencharts.components.line`)

| Function | Source | Status |
|---|---|---|
| `line_chart` | line-charts/1_LineChart.tsx | ☐ |
| `line_chart_curved` | line-charts/2_LineChartCurved.tsx | ☐ |
| `line_chart_multiple` | line-charts/3_LineChartMultiple.tsx | ☐ |
| `line_chart_labels_curved` | line-charts/4_LineChartLabelsCurved.tsx | ☐ |
| `line_chart_stocks_curved` | line-charts/5_LineChartStocksCurved.tsx | ☐ |
| `line_chart_step` | line-charts/6_LineChartStep.tsx | ☐ |
| `line_chart_pulse` | line-charts/7_LineChartPulse.tsx | ☐ |
| `line_chart_full` | line-charts/8_LineChartFull.tsx | ☐ |

### 3.4 Pie / Donut (`reflex_rosencharts.components.pie`)

| Function | Source | Status |
|---|---|---|
| `pie_chart` | pie-charts/1_PieChart.tsx | ☐ |
| `pie_chart_stocks` | pie-charts/2_PieChartStocks.tsx | ☐ |
| `pie_chart_labels` | pie-charts/3_PieChartLabels.tsx | ☐ |
| `donut_chart` | pie-charts/4_DonutChart.tsx | ☐ |
| `donut_chart_center_text` | pie-charts/5_DonutChartCenterText.tsx | ☐ |
| `donut_chart_half` | pie-charts/6_DonutChartHalf.tsx | ☐ |
| `donut_chart_fillable_half` | pie-charts/7_DonutChartFillableHalf.tsx | ☐ |
| `donut_chart_fillable` | pie-charts/8_DonutChartFillable.tsx | ☐ |

### 3.5 Scatter (`reflex_rosencharts.components.scatter`)

| Function | Source | Interactive | Status |
|---|---|---|---|
| `scatter_chart` | scatter-charts/1_ScatterChart.tsx | no | ☐ |
| `scatter_chart_interactive` | scatter-charts/2_ScatterChartInteractive.tsx | yes | ☐ |
| `scatter_chart_multiclass` | scatter-charts/5_ScatterChartMulticlass.tsx | no | ☐ |
| `scatter_chart_stocks` | scatter-charts/6_ScatterChartStocks.tsx | no | ☐ |

### 3.6 Treemap (`reflex_rosencharts.components.treemap`)

| Function | Source | Status |
|---|---|---|
| `treemap_chart` | treemap-charts/1_TreemapChart_DIV.tsx | ☐ |
| `treemap_chart_images` | treemap-charts/2_TreemapChartImages_DIV.tsx | ☐ |
| `treemap_chart_gradient` | treemap-charts/3_TreemapChartGradient_DIV.tsx | ☐ |

### 3.7 Radar (`reflex_rosencharts.components.radar`)

| Function | Source | Status |
|---|---|---|
| `radar_chart` | radar-charts/6_RadarChart.tsx | ☐ |
| `radar_chart_rounded` | radar-charts/8_RadarChartRounded.tsx | ☐ |

### 3.8 Other (`reflex_rosencharts.components.other`)

| Function | Source | Status |
|---|---|---|
| `bubble_chart` | other-charts/4_BubbleChart_DIV.tsx | ☐ |
| `funnel_chart` | other-charts/5_FunnelChart.tsx | ☐ |

## 4. Detailed specification (representative examples)

### 4.1 `line_chart(data, *, height, width, color, class_name, on_point_hover)`

**Description:** Line chart over a time series with a per-point tooltip.

**Props:**

| Prop | Type | Required | Rule | Default |
|---|---|---|---|---|
| `data` | `list[LinePoint]` | Yes | non-empty list of `{date, value}` | `[]` |
| `color` | `str` | No | Tailwind class (`stroke-*`) or color | `"stroke-fuchsia-400"` |
| `height` | `str` | No | valid CSS | `"18rem"` |
| `on_point_hover` | EventHandler | No | receives `{date, value}` | — |

**Data type (`LinePoint`):**
```python
class LinePoint(TypedDict):
    date: str    # ISO date 'YYYY-MM-DD'
    value: float
```

**Usage example:**
```python
rxc.line_chart(
    data=State.sales,            # [{"date": "2023-05-01", "value": 6}, ...]
    color="stroke-indigo-500",
    height="20rem",
    on_point_hover=State.handle_hover,
)
```

### 4.2 `donut_chart(data, *, height, colors, class_name)`

**Data type (`CategoryValue`):**
```python
class CategoryValue(TypedDict):
    name: str
    value: float
```

**Example:**
```python
rxc.donut_chart(
    data=[{"name": "AAPL", "value": 38}, {"name": "MSFT", "value": 22}],
    colors=["#6366f1", "#22c55e", "#f59e0b"],
)
```

### 4.3 `scatter_chart_interactive(data, *, on_point_click, ...)`

**Data type (`ScatterPoint`):**
```python
class ScatterPoint(TypedDict):
    x: float
    y: float
    label: str  # optional depending on the chart
```

**Event handler:** `on_point_click` receives the point `{x, y, label}` on click.

## 5. Errors and validation

| Situation | Expected behavior |
|---|---|
| empty `data` | Empty-state render (no error); the chart does not draw series. |
| Incorrect data schema | Type error at Reflex compile time / console log. |
| Invalid color prop | Applied as-is to the class/style; visual degradation, no crash. |

## 6. Versioning

- Semantic versioning of the package (`MAJOR.MINOR.PATCH`).
- v1.x: stable API for the listed functions. Breaking changes → v2.

---

## Change History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-14 | Initial catalog of the 43 functions and common props |
