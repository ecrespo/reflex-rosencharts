# reflex-rosencharts — Data Model (chart data schemas)

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-14 |
| **Tech Design** | [../technical/architecture.md](../technical/architecture.md) |
| **API Spec** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

> **SDD adaptation note:** There is no database. The "data model" of this library is made up of the
> **input schemas** of each chart: the shape of the `data` that the developer passes from
> `rx.State`. They are defined as `TypedDict` (direct interop with the JS structure that the TSX expects).
> Where Reflex must convert to camelCase, `rx.PropsBase` will be used.

## 1. Principles

- **Fidelity to the original:** field names replicate those of the rosencharts TSX (e.g.
  bar uses `key`, pie/donut use `name`, scatter uses `revenue`/`value`/`company`).
- **Dates as ISO strings:** time series receive `date: "YYYY-MM-DD"`; the TSX converts them
  with `new Date(...)` (as the original does), avoiding Python↔JS serialization problems.
- **Numbers as `float`/`int`:** no `Decimal` (this is not transactional financial data, only visual).
- **Defaults = dataset from the original example** (see Tech Design DD-002).

## 2. Base schemas

```python
from typing import TypedDict

# Time series (line, area)
class TimePoint(TypedDict):
    date: str      # 'YYYY-MM-DD'
    value: float

# Category/value (pie, donut)
class CategoryValue(TypedDict):
    name: str
    value: float

# Bar (bar charts) — the original uses the `key` key
class BarItem(TypedDict):
    key: str
    value: float

# Scatter point (scatter) — names from the original
class ScatterPoint(TypedDict):
    revenue: float     # X axis
    value: float       # Y axis
    company: str       # label

# Radar
class RadarPoint(TypedDict):
    topic: str
    value: float

# Embudo (funnel)
class FunnelStage(TypedDict):
    name: str
    value: float

# Treemap (estructura anidada del original)
class TreemapNode(TypedDict):
    topic: str
    subtopics: list[dict]   # p.ej. [{"Windows": 100, "MacOS": 120, "Linux": 110}]
```

## 3. Chart → schema mapping

| Family | Charts | `data` schema | Notes |
|---|---|---|---|
| Area | area_chart, area_chart_full, area_chart_gradient, area_chart_semi_filled | `list[TimePoint]` | Same as line |
| Line (simple) | line_chart, line_chart_curved, line_chart_labels_curved, line_chart_step, line_chart_pulse, line_chart_full | `list[TimePoint]` | — |
| Line (stocks) | line_chart_stocks_curved | `list[TimePoint]` | Stock-style axis format |
| Line (multiple) | line_chart_multiple | `list[list[TimePoint]]` or `data`, `data2` props | Several series (the original uses `sales`, `sales2`) |
| Bar (DIV/SVG) | the 12 bar_* | `list[BarItem]` | `key`+`value`; breakdown/benchmark add extra fields (see §4) |
| Pie/Donut | pie_*, donut_* | `list[CategoryValue]` | `name`+`value`; palette via `colors` |
| Scatter | scatter_chart, scatter_chart_stocks | `list[ScatterPoint]` | `revenue`(x), `value`(y), `company` |
| Scatter multiclass | scatter_chart_multiclass | `list[ScatterPoint]` + `class` | Class field for color |
| Scatter interactive | scatter_chart_interactive | `list[ScatterPoint]` | Emits `on_point_click` |
| Treemap | treemap_chart, treemap_chart_images, treemap_chart_gradient | `list[TreemapNode]` | Nested; images adds `img` per node |
| Radar | radar_chart, radar_chart_rounded | `list[RadarPoint]` | `topic`+`value` |
| Other | bubble_chart | `list[ScatterPoint]` + `size` | Bubble = scatter with radius |
| Other | funnel_chart | `list[FunnelStage]` | Ordered stages |

## 4. Variants with additional fields

Some charts extend the base schema. They will be documented precisely when ported; expected:

| Chart | Extra fields (expected) |
|---|---|
| bar_chart_breakdown / bar_chart_thin_breakdown | stacked series: `value` per segment or list of segments |
| bar_chart_benchmark | `value` + `benchmark` (reference line) |
| bar_chart_line | `value` (bar) + `line` (overlaid series) |
| bar_chart_horizontal_logo / *_flags_* | `key`, `value` + `logo`/`flag` (image URL) |
| treemap_chart_images | nodes with `img` (URL) |
| donut_chart_center_text | `data` + `center_text` prop |
| donut_chart_fillable / *_half | `value` (0–100) for fill |

> Rule: each variant defines its own `TypedDict` (extending the base one) in the chart's module,
> and the corresponding API Spec references it.

## 5. Examples per schema (original defaults)

```python
# TimePoint (line/area)
[{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

# BarItem (bar)
[{"key": "Technology", "value": 38.1}, {"key": "Financials", "value": 25.3}]

# CategoryValue (pie/donut)
[{"name": "AAPL", "value": 30}, {"name": "BTC", "value": 22}]

# ScatterPoint (scatter)
[{"revenue": 10, "value": 102.8, "company": "Company A"}]

# RadarPoint (radar)
[{"topic": "Tech", "value": 330}, {"topic": "Energy", "value": 140}]

# TreemapNode (treemap)
[{"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120, "Linux": 110}]}]
```

## 6. Validation

| Rule | How it is applied |
|---|---|
| Field types | Static typing with `TypedDict` + `rx.Var[list[Schema]]` (Reflex compilation) |
| Empty list | Allowed → empty-state render |
| Unknown keys | Ignored by the TSX (it only reads the ones it uses) |
| Dates | ISO string; conversion to `Date` on the client |

---

## Change History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Base schemas and mapping of the 43 charts |
